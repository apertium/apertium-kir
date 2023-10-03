#!/usr/bin/env python3

import sys
import base64, hashlib

def hash_line(s):
	return base64.b64encode(hashlib.sha256(s.encode('utf-8')).digest(), b'-_')[:12].decode('utf-8')

def write_sent(sent):
	h = hash_line(sent)
	print("["+h+"]\n"+sent+"[/"+h+"]")

sent = ""
for line in sys.stdin:
	if line == "\n":
		write_sent(sent)
		sent = ""
	else:
		sent += line
