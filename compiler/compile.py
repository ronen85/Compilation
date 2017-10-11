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

def Test(FixADL = True, print_condition = False):
	domainfile = '../expfiles/drink/drink-world3.pddl'
	problemfile = '../expfiles/drink/drink-prob3.pddl'
	agentsfile = '../expfiles/drink/agentsfile.txt'
	waitfile = '../expfiles/drink/waitfile.txt'
	agentslist = grabFileAsList(agentsfile)
	waitlist = grabFileAsList(waitfile)
	[dom, prob] = pddl.parseDomainAndProblem(domainfile, problemfile)
	c_domain = MakeDomain(dom, prob, agentslist, waitlist, FixADL = True)
	c_problem = MakeProblem(dom, prob, agentslist, waitlist)
	if FixADL:
		for action in c_domain.durative_actions:
			action.cond = FixADLConds(action.cond, True)
	if os.path.exists('test'):
		c_domain_file = open('test/c_domain_file.pddl','wb')
		c_domain_file.write(c_domain.asPDDL())
		c_domain_file.close()
		c_problem_file = open('test/c_problem_file.pddl','wb')
		c_problem_file.write(c_problem.asPDDL())
		c_problem_file.close()
	else:
		print 'test dir does not exists.'
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

def testCrewplanning():
	FixADL = True
	print '\n'*50
	print 'Start test crew plannng problem:\n'

	print '########################## Parse Files ##########################'
	domainfile =  '../expfiles/crewplanning/p05-domain.pddl'
	problemfile = '../expfiles/crewplanning/p05.pddl'
	agentsfile =  '../expfiles/crewplanning/agentsfile.txt'
	waitfile =    '../expfiles/crewplanning/waitfile.txt'
	agentslist = grabFileAsList(agentsfile)
	waitlist = grabFileAsList(waitfile)
	[dom, prob] = pddl.parseDomainAndProblem(domainfile, problemfile)
	print '#################### Parse Files Is Complete ####################\n'

	print '######################### Compile Files #########################'
	c_domain = MakeDomain(dom, prob, agentslist, waitlist, FixADL = True)
	print '(domain is compiled ...)'
	c_problem = MakeProblem(dom, prob, agentslist, waitlist)
	print '(problem is compiled ...)'
	if FixADL:
		for action in c_domain.durative_actions:
			action.cond = FixADLConds(action.cond, True)
		print '(ADL condition removed from actions ...)'
	print '################### Compile Files Is Complete ###################\n'

	print '############### Write Domain and Problem to Files ###############'
	c_domain_file = open('../expfiles/crewplanning/compiledFiles/c_domain_file.pddl','wb')
	c_domain_file.write(c_domain.asPDDL())
	c_domain_file.close()
	print '(domain file is ready ...)'
	c_problem_file = open('../expfiles/crewplanning/compiledFiles/c_problem_file.pddl','wb')
	c_problem_file.write(c_problem.asPDDL())
	c_problem_file.close()
	print '(problem file is ready ...)'
	print '######### Write Domain and Problem to Files is Complete #########\n'
	return


def main():
	if sys.argv[1] == 'drink':
		Test()
		return
	elif sys.argv[1] == 'crew':
		testCrewplanning()
		return
	else:
		print 'argument is not valid\ntry drink or crew arguments.'
	# domainfile = sys.argv[1]
	# problemfile = sys.argv[2]
	# agentsfile = sys.argv[3]
	# waitfile = sys.argv[4]
	# agentslist = []
	# with open(agentsfile) as f:
	# 	for line in f:
	# 		agentslist.append(line.rstrip())
	# print agentslist
	# waitlist = []
	# with open(waitfile) as f:
	# 	for line in f:
	# 		waitlist.append(line.rstrip())
	# print waitlist
	return

if __name__ == "__main__":
	main()
