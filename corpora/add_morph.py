#!/usr/bin/env python3

import sys
from subprocess import Popen, PIPE

disambig_process = Popen(["vislcg3", "-g", "-z", "../apertium-kir.kir.rlx"], stdin=PIPE, stdout=PIPE)
cgconv_process = Popen(["cg-conv", "-a", "-l" "-z"], stdin=PIPE, stdout=disambig_process.stdin)
transducer_process = Popen(["hfst-proc", "-w", "-z", "../kir.automorf.hfst"], stdin=PIPE, stdout=cgconv_process.stdin)

def get_analysis(text):
	print(text)
	transducer_process.stdin.write(bytes('{}\n'.format(text), 'utf-8'))
	transducer_process.stdin.write(b'\0')
	transducer_process.stdin.flush()
	output = repr(disambig_process.stdout.readline().strip(b'\0').strip(b'\n').decode())
	print(output)

def write_sent(sent):
	#h = hash_line(sent)
	#print("["+h+"]\n"+sent+"[/"+h+"]")
	print(sent)

sent = ""
for line in sys.stdin:
	if "#" in line:
		if "# text = " in line:
			analysis = get_analysis(line.replace("# text = ","").strip('\r\n" '))
	elif line == "\n" or line == "\r\n":
		write_sent(sent)
		sent = ""
	else:
		sent += line
