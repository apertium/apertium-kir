#!/usr/bin/env python
# -*- coding: utf-8 -*-

# HfstTester.py 1.9999.1 - Copyright (c) 2011 
# Brendan Molloy <brendan@bbqsrc.net>
# Børre Gaup <boerre@skolelinux.no>
# Licensed under Creative Commons Zero (CC0)

# Taken from:
# http://apertium.svn.sourceforge.net/svnroot/apertium/incubator/apertium-tgl-ceb/dev/verbs/HfstTester.py@28665
# Copied into the GT svn instead of just referenced, since file externals don't work for
# foreign repositories.

import sys
try:
	import argparse
except:
	raise ImportError("argparse missing.\nPlease do `sudo easy_install argparse`.")

try:
	from collections import OrderedDict
except:
	try:
		from ordereddict import OrderedDict
	except:
		raise ImportError("OrderedDict missing.\nPlease do `sudo easy_install ordereddict`.")		
try:
	import yaml
except:
	raise ImportError("yaml missing.\nPlease do `sudo easy_install pyyaml`.")

from multiprocessing import Process, Manager
from subprocess import *
import os, traceback

def string_to_list(data):
	if isinstance(data, (str, unicode)): return [data]
	else: return data
	
def invert_dict(input):
		tmp = OrderedDict()
		for key, val in input.iteritems():
			for v in string_to_list(val):
				tmp.setdefault(v, set()).add(key)
		return tmp 

def colourise(string, opt=None):
	def red(s="", r="\033[m"):
		return "\033[1;31m%s%s" % (s, r) 
	def green(s="", r="\033[m"):
		return "\033[0;32m%s%s" % (s, r) 
	def orange(s="", r="\033[m"):
		return "\033[0;33m%s%s" % (s, r) 
	def yellow(s="", r="\033[m"):
		return "\033[1;33m%s%s" % (s, r) 
	def blue(s="", r="\033[m"):
		return "\033[0;34m%s%s" % (s, r) 
	def light_blue(s="", r="\033[m"):
		return "\033[0;36m%s%s" % (s, r) 
	def reset(s=""):
		return "\033[m%s" % s

	if not opt:
		x = string
		x = x.replace("=>", blue("=>"))
		x = x.replace("<=", blue("<="))
		x = x.replace(":", blue(":"))
		x = x.replace("[PASS]", green("[PASS]"))
		x = x.replace("[FAIL]", red("[FAIL]"))
		return x
	
	elif opt == 1:
		return light_blue(string)

	elif opt == 2:
		x = string.replace('asses: ', 'asses: %s' % green(r=""))
		x = x.replace('ails: ', 'ails: %s' % red(r=""))
		x = x.replace(', ', reset(', '))
		x = x.replace('otal: ', 'otal: %s' % light_blue(r=""))
		return "%s%s" % (x, reset())

def whereis(program):
	for path in os.environ.get('PATH', '').split(':'):
		if os.path.exists(os.path.join(path, program)) and \
		   not os.path.isdir(os.path.join(path, program)):
			return os.path.join(path, program)
	return None

# Courtesy of https://gist.github.com/844388. Thanks!
class OrderedDictYAMLLoader(yaml.Loader):
	"""A YAML loader that loads mappings into ordered dictionaries."""

	def __init__(self, *args, **kwargs):
		yaml.Loader.__init__(self, *args, **kwargs)

		self.add_constructor(u'tag:yaml.org,2002:map', type(self).construct_yaml_map)
		self.add_constructor(u'tag:yaml.org,2002:omap', type(self).construct_yaml_map)

	def construct_yaml_map(self, node):
		data = OrderedDict()
		yield data
		value = self.construct_mapping(node)
		data.update(value)

	def construct_mapping(self, node, deep=False):
		if isinstance(node, yaml.MappingNode):
			self.flatten_mapping(node)
		else:
			raise yaml.constructor.ConstructorError(None, None,
				'expected a mapping node, but found %s' % node.id, node.start_mark)

		mapping = OrderedDict()
		for key_node, value_node in node.value:
			key = self.construct_object(key_node, deep=deep)
			try:
				hash(key)
			except TypeError, exc:
				raise yaml.constructor.ConstructorError('while constructing a mapping',
					node.start_mark, 'found unacceptable key (%s)' % exc, key_node.start_mark)
			value = self.construct_object(value_node, deep=deep)
			mapping[key] = value
		return mapping

class HfstTester(object):
	class AllOutput:
		@staticmethod
		def final_result(hfst):
			text = "Total passes: %d, Total fails: %d, Total: %d\n"
			print colourise(text % (hfst.passes, hfst.fails, hfst.fails+hfst.passes), 2).encode('utf-8')

	class NormalOutput(AllOutput):
		@staticmethod
		def title(text):
			print colourise("-"*len(text), 1).encode('utf-8')
			print colourise(text, 1).encode('utf-8')
			print colourise("-"*len(text), 1).encode('utf-8')

		@staticmethod
		def success(l, r):
			print colourise("[PASS] %s => %s" % (l, r)).encode('utf-8')

		@staticmethod
		def failure(form, err, errlist):
			print colourise("[FAIL] %s => %s: %s" % (form, err, ", ".join(errlist)))

		@staticmethod
		def result(title, test, counts):
			p = counts["Pass"]
			f = counts["Fail"]
			text = "Test %d - Passes: %d, Fails: %d, Total: %d\n"
			print colourise(text % (test, p, f, p+f), 2).encode('utf-8')

	class CompactOutput(AllOutput):
		@staticmethod
		def title(*args):
			pass

		@staticmethod
		def success(*args):
			pass

		@staticmethod
		def failure(*args):
			pass

		@staticmethod
		def result(title, test, counts):
			p = counts["Pass"]
			f = counts["Fail"]
			out = "%s %d/%d/%d" % (title, p, f, p+f)
			if counts["Fail"] > 0:
				print colourise("[FAIL] %s" % out)
			else:
				print colourise("[PASS] %s" % out)
			
	def __init__(self):
		self.fails = 0
		self.passes = 0

		self.count = []
		self.parse_args()
		self.load_config()

	def start(self):
		self.run_tests(self.args.test)

	def parse_args(self):
		argparser = argparse.ArgumentParser(
			description="""Test morphological transducers for consistency. 
			`hfst-lookup` (or Xerox' `lookup` with argument -x) must be
			available on the PATH.""",
			epilog="Will run all tests in the test_file by default.")
		argparser.add_argument("-c", "--colour",
			dest="colour", action="store_true",
			help="Colours the output")
		argparser.add_argument("-C", "--compact",
			dest="compact", action="store_true",
			help="Makes output more compact")
		argparser.add_argument("-i", "--ignore-extra-analyses",
			dest="ignore_analyses", action="store_true",
			help="""Ignore extra analyses when there are more than expected,
			will PASS if the expected one is found.""")
		argparser.add_argument("-s", "--surface",
			dest="surface", action="store_true",
			help="Surface input/analysis tests only")
		argparser.add_argument("-l", "--lexical",
			dest="lexical", action="store_true",
			help="Lexical input/generation tests only")
		argparser.add_argument("-f", "--hide-fails",
			dest="hide_fail", action="store_true",
			help="Suppresses passes to make finding failures easier")
		argparser.add_argument("-p", "--hide-passes",
			dest="hide_pass", action="store_true",
			help="Suppresses failures to make finding passes easier")
		argparser.add_argument("-S", "--section", default=["hfst"],
			dest="section", nargs=1, required=False, 
			help="The section to be used for testing (default is `hfst`)")
		argparser.add_argument("-t", "--test",
			dest="test", nargs=1, required=False,
			help="""Which test to run (Default: all). TEST = test ID, e.g.
			'Noun - gåetie' (remember quotes if the ID contains spaces)""")
		argparser.add_argument("-v", "--verbose",
			dest="verbose", action="store_true",
			help="More verbose output.")
		argparser.add_argument("test_file", nargs=1,
			help="YAML file with test rules")
		self.args = argparser.parse_args()

	def load_config(self):
		global colourise
		f = yaml.load(open(self.args.test_file[0]), OrderedDictYAMLLoader)
		
		section = self.args.section[0]
		if not section in f["Config"]:
			raise AttributeError("'%s' not found in Config of test file." % section)
		
		self.program = f["Config"][section].get("App", "hfst-lookup")
		if not whereis(self.program):
			raise IOError("Cannot find `%s`. Check $PATH." % self.program)

		if self.args.verbose:
			print("`%s` will be used for parsing dictionaries." % self.program)

		self.gen = f["Config"][section].get("Gen", None)
		self.morph = f["Config"][section].get("Morph", None)
	
		if self.gen == self.morph == None:
			raise AttributeError("One of Gen or Morph must be configured.")

		for i in (self.gen, self.morph):
			if i and not os.path.isfile(i):
				raise IOError("File %s does not exist." % i)
		
		self.tests = f["Tests"]
		for test in self.tests:
			for key, val in self.tests[test].iteritems():
				self.tests[test][key] = string_to_list(val)

		if not self.args.colour:
			colourise = lambda x, y=None: x

		if self.args.compact:
			self.out = HfstTester.CompactOutput
		else:
			self.out = HfstTester.NormalOutput
		
		# Assume that the command line input is utf-8, convert it to unicode
		if self.args.test:
			self.args.test[0] = self.args.test[0].decode('utf-8')
		
	def run_tests(self, input=None):
		if self.args.surface == self.args.lexical == False:
			self.args.surface = self.args.lexical = True
		

		if(input != None):
			self.parse_fsts(self.tests[input[0]])
			if self.args.lexical: self.run_test(input[0], True)
			if self.args.surface: self.run_test(input[0], False)
		
		else:
			tests = {}
			for t in self.tests:
				tests.update(self.tests[t])
			self.parse_fsts(tests)
			for t in self.tests:
				if self.args.lexical: self.run_test(t, True)
				if self.args.surface: self.run_test(t, False)
		
		if self.args.verbose:
			self.out.final_result(self)

	def parse_fsts(self, tests):
		invtests = invert_dict(tests)
		manager = Manager()
		self.results = manager.dict({"gen": {}, "morph": {}})

		def parser(self, d, f, tests):
			keys = tests.keys()
			app = Popen([self.program, f], stdin=PIPE, stdout=PIPE, stderr=PIPE)
			args = '\n'.join(keys) + '\n'
			app.stdin.write(args.encode('utf-8'))
			res = app.communicate()[0].decode('utf-8').split('\n\n')
			self.results[d] = self.parse_fst_output(res)
		
		gen = Process(target=parser, args=(self, "gen", self.gen, tests))
		gen.daemon = True
		gen.start()
		if self.args.verbose:
			print("Generating...")
		
		morph = Process(target=parser, args=(self, "morph", self.morph, invtests))
		morph.daemon = True
		morph.start()
		if self.args.verbose:
			print("Morphing...")

		gen.join()
		morph.join()

		if self.args.verbose:
			print("Done!")
		
	def run_test(self, input, is_lexical):
		if is_lexical:
			desc = "Lexical/Generation"
			f = "gen"
			tests = self.tests[input]
			invtests = invert_dict(self.tests[input])

		else: #surface
			desc = "Surface/Analysis"
			f = "morph"
			tests = invert_dict(self.tests[input])
			invtests = self.tests[input]

		if not f:
			return

		c = len(self.count)
		self.count.append({"Pass":0, "Fail":0})
		
		title = "Test %d: %s (%s)" % (c, input, desc)
		self.out.title(title)

		for test, forms in tests.iteritems():
			expected_results = set(forms)
			actual_results = set(self.results[f][test])

			invalid = set()
			missing = set()
			success = set()
			passed = False

			for form in expected_results:
				if not form in actual_results:
					invalid.add(form.encode('utf-8'))
			
			for form in actual_results:
				if not form in expected_results:
					missing.add(form.encode('utf-8'))
		
			for form in expected_results:
				if not form in (invalid | missing):
					passed = True
					success.add(form.encode('utf-8'))
					self.count[c]["Pass"] += 1
					if not self.args.hide_pass:
						self.out.success(test, form)				
			
			if not self.args.hide_fail:
				if len(invalid) > 0:
					self.out.failure(test.encode('utf-8'), "Invalid test item", invalid)
					self.count[c]["Fail"] += len(invalid)
				if len(missing) > 0 and (not self.args.ignore_analyses or not passed):
					self.out.failure(test.encode('utf-8'), "Unexpected output", missing)
					self.count[c]["Fail"] += len(missing)

		self.out.result(title, c, self.count[c])
		
		self.passes += self.count[c]["Pass"]
		self.fails += self.count[c]["Fail"]
	
	def parse_fst_output(self, fst):
		parsed = {}
		for item in fst:
			res = item.replace('\r\n','\n').replace('\r','\n').split('\n')
			for i in res:
				if i.strip() != '':
					results = i.split('\t')
					key = results[0].strip()
					if not key in parsed:
						parsed[key] = set()
					# This test is needed because xfst's lookup
					# sometimes output strings like
					# bearkoe\tbearkoe\t+N+Sg+Nom, instead of the expected
					# bearkoe\tbearkoe+N+Sg+Nom
					if len(results) > 2 and results[2][0] == '+':
						parsed[key].add(results[1].strip() + results[2].strip())
					else:
						parsed[key].add(results[1].strip())
		return parsed

if __name__ == "__main__":
	try:
		hfst = HfstTester()
		hfst.start()
	except KeyboardInterrupt:
		pass
