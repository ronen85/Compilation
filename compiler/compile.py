#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../pythonpddl")
import pddl
from antlr4 import *
import pddlLexer
import pddlParser
import itertools
from copy import deepcopy
from compilation import *


# test : python compile.py  ../expfiles/drink/drink-world2.pddl ../expfiles/drink/drink-prob2.pddl ../expfiles/drink/agentsfile.txt ../expfiles/drink/waitfile.txt

def main():
	domainfile = sys.argv[1]
	problemfile = sys.argv[2]
	agentsfile = sys.argv[3]
	waitfile = sys.argv[4]
	agentslist = []
	with open(agentsfile) as f:
		for line in f:
			agentslist.append(line.rstrip())
	print agentslist
	waitlist = []
	with open(waitfile) as f:
		for line in f:
			waitlist.append(line.rstrip())
	print waitlist
	# if len(sys.argv) < 2:
	# 	print("Usage: pddl.py <domain> <problem>")
	# 	return
	# (dom,prob) = pddl.parseDomainAndProblem(domainfile, problemfile)
	# MakeDomain(dom, prob, agentslist, waitlist, print_condition)
	return

if __name__ == "__main__":
	main()
