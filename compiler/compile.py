#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append("../pythonpddl")
import pddl
from antlr4 import *
import pddlLexer
import pddlParser
import itertools
from copy import deepcopy
from compilation import *


def grabFileAsList(file_address):
	new_list = []
	with open(file_address) as f:
		for line in f:
			new_list.append(line.rstrip())
	return new_list;

def Test(print_condition = False):
	domainfile = '../expfiles/drink/drink-world2.pddl'
	problemfile = '../expfiles/drink/drink-prob2.pddl'
	agentsfile = '../expfiles/drink/agentsfile.txt'
	waitfile = '../expfiles/drink/waitfile.txt'
	agentslist = grabFileAsList(agentsfile)
	waitlist = grabFileAsList(waitfile)
	[dom, prob] = pddl.parseDomainAndProblem(domainfile, problemfile)
	c_domain = MakeDomain(dom, prob, agentslist, waitlist)
	c_problem = MakeProblem(dom, prob, agentslist, waitlist)
	if os.path.exists('test'):
		c_domain_file = open('test/c_domain_file.pddl','wb')
		c_domain_file.write(c_domain.asPDDL())
		c_domain_file.close()
		c_problem_file = open('test/c_problem_file.pddl','wb')
		c_problem_file.write(c_problem.asPDDL())
		c_problem_file.close()
	else:
		os.makedirs('test')
	if print_condition:
		print '\n'*30
		print 'the domain is: ', domainfile
		print 'the problem is: ', problemfile
		print 'the agents list is: ', agentslist
		print 'the wait list is: ', waitlist
		print 'the compiled domain is: '
		print c_domain.asPDDL()
		print 'the compiled problem is: '
		print c_problem.asPDDL()
	return

def main():
	if sys.argv[1] == 'test':
		Test()
		return
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
