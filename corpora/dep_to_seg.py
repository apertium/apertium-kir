#!/usr/bin/env python3

import sys
import re

formRegex = re.compile("\"<(.*?)>\"")
lemmaRegex = re.compile("\"(.*?)\"")

def removeSpaceAfter(outline):
	return outline.replace("$", ">$")

def addSubToken(form, outline):
	return outline.replace("$", ">"+form+"$")

def write_sent(sent):
	outline=""
	for line in sent.split("\n"):
		if len(line)>0 and line[0]=="#":
			commentline = line #print(line)
			print(commentline)
		elif len(line)>0 and line[0]=="\"":
			form = formRegex.search(line)[1]
			if form in ".,;?!":
				outline = removeSpaceAfter(outline)
			if outline!="": print(outline)
			#print(line,form)
			outline = "^{}/{}$".format(form, form)
		elif len(line)>0 and line[0]=="	":
			#print(line)
			lemma = lemmaRegex.search(line)[1]
			numtabs = line.count('	')
			#print(numtabs)
			if numtabs > 1:
				outline = addSubToken(lemma, outline)
		elif line=="":
			pass
		else:
			outline += line
			print("WARNING", line)
	print(outline+"\n")

sent = ""
for line in sys.stdin:
	if line == "\n":
		write_sent(sent)
		sent = ""
	else:
		sent += line
