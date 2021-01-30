"""
	This script creates a CoNLL-U file from three input files:
	1) UDX_FILE ... This is a tab separated file with tagset correspondences
	2) DEP_FILE ... This is a list of sentences in VISLCG3 format
	3) SEG_FILE ... This is a list of sentences in Apertium format

	TODO:
		- Maybe mark the POS/lemma/dep differently from other tags?
"""

###############################################################################
import sys, re

def get_surface_cg(line):
	return line[2:-2]

def get_lemma_cg(line):
	beg = line.find('"') + 1
	end = line.rfind('"')
	return line[beg:end]

def get_deps_cg(line):
	return [int(i) for i in line.split('#')[1].split('->')]

def get_func_cg(line):
	for i in line.strip().split(' '):
		if len(i) > 1 and i[0] == '@':
			#return i[1:]
			return i

def get_tags_cg(line):
	tags = []
	for i in line.strip().split(' '):
		if not i:
			print('[get_tags_cg] ERROR:', line, '|||', i, file=sys.stderr)
			return ''
		if i[0] not in ['@', '"', '#']:
			tags.append(i)
	return '|'.join(tags)

# forms = {}
# forms[0] = ("chawe", [(3, "_", "chi", "_", "_", "_", 4), (4, "_", "awe", "_", "_", "_", 2)])
def get_tokens(sent):
	tokens = {}
	counter = -1
	for line in sent.split('\n'):
		line = line.strip('\n ')
		if line == '': continue
		if line[0] == '"':
			counter += 1
			tokens[counter] = (get_surface_cg(line), [])
		elif line[0] == '\t':
			deps = get_deps_cg(line)
			tags = get_tags_cg(line)
			tokens[counter][1].append((deps[0], '_', get_lemma_cg(line), '_', tags, '_', deps[1], get_func_cg(line), '_', '_'))
		else:
			continue
	return tokens

# segs[0] = ("chawe", ["ch", "awe"])
def get_segmentations(sent):
	segmentations = {}
	counter = 0
	for line in sent.split('\n'):
		line = line.strip()
		if line == '': continue
		if line[0] != '^':
			continue
		if line.count('/') == 1:
			if line.count('*') > 0:
				print('ERROR: Empty segmentations: ', line, file=sys.stderr)
			(surface, segmentation) = line[1:-1].split('/')
			segmentations[counter] = (surface, segmentation.split('>'))
		elif line.count('/') > 1:
			print('WARNING: Multiple segmentations:\n  ', line, file=sys.stderr)
			return {}
		elif line.count('/') == 0:
			print('WARNING: No segmentations:\n  ', line, file=sys.stderr)
			return {}
		counter += 1
	return segmentations

def merge_segmentations(segs, n, direction='L'):
	if n == 2 and direction == 'L':
		return [segs[0], ''.join(segs[1:])]
	elif n == 2 and direction == 'R':
		return [''.join(segs[0:-1]), segs[-1]]
	return segs

def get_comments(sent):
	comments = []
	for line in sent.strip().split('\n'):
		if line[0] == '#':
			comments.append(line)
	return '\n'.join(comments)

def load_rules(f):
	rules = []
	for line in f:
		if line[0] == '#':
			continue
		row = line.strip().split('\t')
		if len(row) != 8:
			print('WARNING: Broken rule', file=sys.stderr)
			print(line, '||', row, file=sys.stderr)
			continue
		score = sum([i for (i, j) in enumerate(reversed(row[:4])) if j != '_'])
		morf = [i for i in row[2].split('|') if i != '_']
		deprel = ['@'+i for i in row[3:4] if i != '_']
		pattern = set([i for i in row[:2] if i != '_'] + morf + deprel)
		rule = (score, pattern, row[4:])
		#print('RULE:',rule)
		rules.append(rule)
	rules.sort()
	rules.reverse()

	return rules

def apply_rules(rules, analysis):
	o = ['_', '_', [], '_']

	# (2, '_', 'kʼamanik', '_', 'v|iv|impf|s_sg3', '_', 1, 'x', '_', '_')
	msd = set([analysis[2], analysis[7]] + analysis[4].split('|'))

	remainder = msd
	for rule in rules:
		remainder = msd - rule[1]
		intersect = msd.intersection(rule[1])
		if intersect == rule[1]:
			for (i, j) in enumerate(rule[2]):
				if j == '_': continue
				if type(o[i]) == list:
					for k in j.split('|'):
						o[i].append(k)
				else:
					o[i] = j
			msd = remainder

	o[2] = list(set(o[2]))
	o[2].sort()
	o[2] = '|'.join(o[2])
	for i in range(0, len(o)):
		if o[i] == '':
			o[i] = '_'

	return (o, remainder)

def format_conllu_line(line):
	#       1   2   3   4   5   6   7   8   9   10
        return '%d\t%s\t%s\t%s\t%s\t%s\t%d\t%s\t%s\t%s' % line


###############################################################################

if len(sys.argv) != 4:
	print(sys.argv, file=sys.stderr)
	print('conllise.py UDX_FILE DEP_FILE SEG_FILE', file=sys.stderr)
	sys.exit(-1)

tag_rules = open(sys.argv[1]).readlines()
sents_dep = open(sys.argv[2]).read().split('\n\n')
sents_seg = open(sys.argv[3]).read().split('\n\n')

#if len(sents_dep) != len(sents_seg):
#	print('ERROR:', sys.argv, file=sys.stderr)
#	print('ERROR:', len(sents_dep), len(sents_seg), file=sys.stderr)
#	sys.exit(-1)
#
rules = load_rules(tag_rules)

sents_depseg = {}

#print(rules, file=sys.stderr)

# Loop through each of the sentences
for i in range(0, len(sents_dep)):
	sent_id_match = re.match('# sent_id = .*', sents_dep[i])
	if not sent_id_match:
		continue
	if len(re.findall('[0-9]->[0-9]', sents_dep[i])) != len(re.findall('\n\t', sents_dep[i])):
		print(sent_id_match[0], '| WARNING: Sentence annotation incomplete', file=sys.stderr)
		continue
	sent_id = sent_id_match[0]
	if sent_id not in sents_depseg:
		sents_depseg[sent_id] = {}
	sents_depseg[sent_id][0] = sents_dep[i]

for i in range(0, len(sents_seg)):
	sent_id_match = re.match('# sent_id = .*', sents_seg[i])
	if not sent_id_match:
		continue
	sent_id = sent_id_match[0]
	if sent_id not in sents_depseg:
		sents_depseg[sent_id] = {}
	sents_depseg[sent_id][1] = sents_seg[i]

mono_morphemes = ['pr', 'mark|fin', 'mark', 'part', 'foc', 'aux']

converted_sents = 0
converted_tokens = 0
converted_words = 0

missing_parses = 0
missing_segmentations = 0

for depseg in sents_depseg:
	#print('-->', depseg, file=sys.stderr)
	if len(sents_depseg[depseg]) != 2:
		if 0 not in sents_depseg[depseg]:
			print(depseg, '| WARNING: Empty parse', file=sys.stderr)
			missing_parses += 1
		if 1 not in sents_depseg[depseg]:
			print(depseg, '| WARNING: Empty segmentation', file=sys.stderr)
			missing_segmentations += 1
		continue

	parse = sents_depseg[depseg][0]
	comments = get_comments(parse)
	tokens = get_tokens(parse)
	segmentations = get_segmentations(sents_depseg[depseg][1])

#	print(tokens)

	current_sent_id = comments.split('\n')[0]

	if len(tokens) != len(segmentations):
		print('[tok_seg]',current_sent_id,'ERROR:',tokens, file=sys.stderr)
		print('[tok_seg]',current_sent_id,'ERROR:',segmentations, file=sys.stderr)
		continue

	print(comments)
	indices = []
	foundRoot = 0
	for j in range(0, len(tokens)):
		token = tokens[j]
		if len(token[1]) > 1: # This is a multi-token word
			# {2: ('chawe', [(3, '_', 'chi', '_', '_', '_', 4, '_', '_', '_'), (4, '_', 'awe', '_', '_', '_', 2, '_', '_', '_')])}
			segs = segmentations[j][1]
			if len(tokens[1]) != len(segmentations[j][1]):
				#print('!!!',segs,file=sys.stderr )
				# This is hacky :(
				if token[1][1][4] in mono_morphemes:
					segs = merge_segmentations(segmentations[j][1], len(token[1]), direction='R')
				else:
					segs = merge_segmentations(segmentations[j][1], len(token[1]))
			print('%d-%d\t%s\t_\t_\t_\t_\t_\t_\t_\t_' % (token[1][0][0], token[1][-1][0], token[0]))
			for (k, word) in enumerate(token[1]):
				(analysis, misc) = apply_rules(rules, word)
				#       1        2                       3        4            5    6            7        8        9    10
				line = (word[0], segs[k], word[2], analysis[1], '_', analysis[2], word[6], word[7][1:], '_', '_')
				print(format_conllu_line(line))
				indices.append(int(word[0]))
				if word[7] == '@root':
					foundRoot += 1
				if word[7] == '@root' and word[6] != 0:
					print('ERROR:',current_sent_id,' Root is not root', line, file=sys.stderr)
				if word[7] != '@root' and word[6] == 0:
					print('ERROR:',current_sent_id,' Node 0 is not root', line, file=sys.stderr)
				if segs[k] == '':
					print('ERROR:',current_sent_id,' Empty surface token', line, file=sys.stderr)
				if word[0] == word[6]:
					print('ERROR:',current_sent_id,' Cycle found', line, file=sys.stderr)
				if word[7] == '' or word[7] == None:
					print('ERROR:',current_sent_id,' Invalid deprel', line, file=sys.stderr)
	
			converted_words += len(token[1])
		else:
			# {0: ('Rajawaxik', [(1, '_', 'rajawaxik', '_', '_', '_', 0, '_', '_', '_')])}
			word = token[1][0]
			(analysis, misc) = apply_rules(rules, word)
			#       1        2         3        4            5    6            7        8        9    10
			line = (word[0], token[0], word[2], analysis[1], '_', analysis[2], word[6], word[7][1:], '_', '_')
			print(format_conllu_line(line))
			if word[7] == '@root' and word[6] != 0:
				print('ERROR:',current_sent_id,' Root is not root', line, file=sys.stderr)
			if word[7] != '@root' and word[6] == 0:
				print('ERROR:',current_sent_id,' Node 0 is not root', line, file=sys.stderr)
			if word[0] == word[6]:
				print('ERROR:',current_sent_id,' Cycle found', line, file=sys.stderr)
			if word[7] == '' or word[7] == None:
				print('ERROR:',current_sent_id,' Invalid deprel', line, file=sys.stderr)
			converted_words += 1
			indices.append(int(word[0]))

			if word[7] == '@root':
				foundRoot += 1 

	if foundRoot != 1:
		print('ERROR:',current_sent_id,' Root not found,', foundRoot, 'roots', file=sys.stderr)

	for (x, y) in enumerate(indices):
		if x+1 != y:
			print('ERROR:',current_sent_id,' Indices out of sync:', indices, file=sys.stderr)
			break

	print()
	converted_sents += 1
	converted_tokens += len(tokens)

###############################################################################

print('Converted %d sentences and %d tokens (%d words). Average length: %.2f. Missing %d parses and %d segmentations.' % (converted_sents, converted_tokens, converted_words ,converted_words/converted_sents,missing_parses, missing_segmentations), file=sys.stderr)
