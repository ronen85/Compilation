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

def main():
	if len(sys.argv) < 2:
		print("Usage: pddl.py <domain> <problem>")
		return
	domainfile = sys.argv[1]
	problemfile = sys.argv[2]
	(dom,prob) = pddl.parseDomainAndProblem(domainfile, problemfile)
	MakeDomain(dom, prob, agentslist, waitlist, print_condition)
	return

if __name__ == "__main__":
	main()