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
	for line in get_disam(text).split('\n'):
		#print(line)
		if re.match('"<.*>"', line):
			if form != "":
				token = (form, analyses)
				sent.append(token)
				form = ""
				analyses = []
			form = line
		elif re.search("^\t", line):
			analyses.append(line.strip("\t").split())
	#print(sent)
	return sent

def write_sent(sent,analysis):
	#h = hash_line(sent)
	#print("["+h+"]\n"+sent+"[/"+h+"]")
	idxs = [*range(0, len(sent))]
	for line in zip(sent,analysis,idxs):
		(file_line, disam_line, idx) = (line[0], line[1], line[2])
		print(file_line[0], disam_line[0])
		if file_line[0] != disam_line[0]:
			print("WARNING: mismatch: ", file_line, disam_line, file=sys.stderr)
			if(sent[idx+1][0] == disam_line[0]):
				print("NEXT LINE MATCHES:", sent[idx+1][0], disam_line, file=sys.stderr)
		else:
			pass

sent = []
form = ""
analyses = []
for line in sys.stdin:
	if re.search("^#", line):
		if re.search("^# text = ", line):
			analysis = get_analysis(line.replace("# text = ","").strip('\r\n" '))
	elif line == "\n" or line == "\r\n":
		write_sent(sent, analysis)
		sent = []
		form = ""
		analyses = []
	else:
		strippedline = line.strip('\r\n')
		if re.search("<.*>", strippedline):
			if form != "" and len(analyses) != 0:
				token = (form, analyses)
				sent.append(token)
				form = ""
				analyses = []
			form = strippedline
		else:
			analyses.append(strippedline.split())

for proc in disambig_process, cgconv_process, transducer_process:
	proc.kill()
