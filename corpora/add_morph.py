#!/usr/bin/env python3

import sys
from subprocess import Popen, PIPE
import re

disambig_process = Popen(["vislcg3", "-g", "../apertium-kir.kir.rlx"], stdin=PIPE, stdout=PIPE)
cgconv_process = Popen(["cg-conv", "-a", "-l"], stdin=PIPE, stdout=disambig_process.stdin)
transducer_process = Popen(["hfst-proc", "-w", "-z", "../kir.automorf.hfst"], stdin=PIPE, stdout=cgconv_process.stdin)

def get_disam(text):
	transducer_process.stdin.write(bytes('{}\n'.format(text), 'utf-8'))
	transducer_process.stdin.write(b'\0')
	transducer_process.stdin.flush()
	output = ""
	outline = disambig_process.stdout.readline().strip(b'\0').strip(b'\n').decode()
	while repr(outline) != repr('<STREAMCMD:FLUSH>'):
		output += "\n" + outline
		outline = disambig_process.stdout.readline().strip(b'\0').strip(b'\n').decode()
	return(output)

def get_analysis(text):
	#print(text)
	sent = []
	form = ""
	analyses = []
	lines = get_disam(text).split('\n')
	#print(lines)
	for line in lines:
		if re.match('"<.*>"', line):
			if form != "":
				token = (form, analyses)
				sent.append(token)
				form = ""
				analyses = []
			form = line
		elif re.search("^\t\"", line):
			analyses.append(line.strip("\t").split())
		elif re.search("^\t", line):
			#print(re.search("^\t", line)[0], line.split(), file=sys.stderr)
			#print(line.split(), file=sys.stderr)
			these_analyses = line.split()
			these_analyses.insert(0, re.search("^\t", line)[0]) # add extra tabs to beginning
			analyses.append(these_analyses)
	if form != "":
		#print(line, token)
		token = (form, analyses)
		#print(token)
		sent.append(token)
		#print(sent)
	else:
		print(line, token, file=sys.stderr)

	#print(sent)
	return sent

def write_sent(sent,analysis):
	#h = hash_line(sent)
	#print("["+h+"]\n"+sent+"[/"+h+"]")
	#idxs = [*range(0, len(sent))]
	#for line in zip(sent,analysis,idxs):
	file_idx = 0
	disam_idx = 0
	while file_idx < len(sent) and disam_idx < len(analysis):
		#(file_line, disam_line, idx) = (line[0], line[1], line[2])
		file_line = sent[file_idx]
		disam_line = analysis[disam_idx]
		file_idx += 1
		disam_idx += 1
		#print(file_line[0], disam_line[0], file=sys.stderr)
		#print("INFO: ", disam_line[1], file=sys.stderr)
		if file_line[0] != disam_line[0]:
			print("WARNING: mismatch: ", file_line, disam_line, file=sys.stderr)
			if(sent[file_idx][0] == disam_line[0]):
				print("NEXT FILE LINE MATCHES:", sent[file_idx][0], disam_line, file=sys.stderr)
				disam_idx -= 1
				print(file_line[0])
				print("	"+" TOKENISATIONERROR "+" ".join(file_line[1][-1][-2:]))
			elif(sent[file_idx+1][0] == disam_line[0]):
				print("NEXTNEXT FILE LINE MATCHES:", sent[file_idx+1][0], disam_line, file=sys.stderr)
				disam_idx -= 2
				print(file_line[0])
				print("	"+" TOKENISATIONERROR "+" ".join(file_line[1][-1][-2:]))
			elif(file_line[0] == analysis[disam_idx][0]):
				print("NEXT DISAM LINE MATCHES:", sent[file_idx][0], disam_line, file=sys.stderr)
				file_idx -= 1
			else:
				print(file_line[0])
				print("	"+" TOKENISATIONERROR "+" ".join(file_line[1][-1][-2:]))
		else:
			print(disam_line[0])
			#print(disam_line[1][0], file_line[1][-1][-2:], file=sys.stderr)
			print("	"+" ".join(disam_line[1][0])+" "+" ".join(file_line[1][-1][-2:]))
		if len(disam_line[1])>1 and '\t' in disam_line[1][1][0]:
			#print("INFO: ", disam_line[1], file=sys.stderr)
			print("\t"+" ".join(disam_line[1][1])+" #")
		
	print()

sent = []
form = ""
analyses = []
for line in sys.stdin:
	if re.search("^#", line):
		if re.search("^# text = ", line):
			analysis = get_analysis(line.replace("# text = ","").strip('\r\n" '))
			#print(analysis)
		print(line.strip('\r\n" '))
	elif line == "\n" or line == "\r\n":
		# add last token to sentence (doesn't add to last sentence)
		token = (form, analyses)
		sent.append(token)
		write_sent(sent, analysis)
		sent = []
		form = ""
		analyses = []
	else:
		strippedline = line.strip('\r\n')
		#print("HARGLE", strippedline,"BARGLE")
		if re.search("<.*>", strippedline):
			if form != "" and len(analyses) != 0:
				token = (form, analyses)
				#print(token)
				sent.append(token)
				form = ""
				analyses = []
			form = strippedline
		else:
			#print(strippedline.split())
			analyses.append(strippedline.split())
# add last token to last sentence
token = (form, analyses)
sent.append(token)
# write last sentence, after last line is read in
write_sent(sent, analysis)

for proc in disambig_process, cgconv_process, transducer_process:
	proc.kill()
