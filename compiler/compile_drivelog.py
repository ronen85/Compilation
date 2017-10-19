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
from compilation_v1 import *

def printActionBasicInfo(action, params):
	waitlist = params.waitlist
	# grab basic conditions
	pref_start = GrabCond('pref_start', action, params)
	prew_start = GrabCond('prew_start', action, params)
	pref_inv = GrabCond('pref_inv', action, params)
	pref_end = GrabCond('pref_end', action, params)
	neg_pref_start = GrabCond('neg_pref_start', action, params)
	neg_prew_start = GrabCond('neg_prew_start', action, params)
	neg_pref_inv =   GrabCond('neg_pref_inv', action, params)
	neg_pref_end =   GrabCond('neg_pref_end', action, params)
	# grab basic effects
	add_start = GrabEff('add_start', action)
	del_start = GrabEff('del_start', action)
	add_end = GrabEff('add_end', action)
	del_end = GrabEff('del_end', action)
	# print info
	print '\nthe action name is: ', action.name
	print '\n################ conditions ################'
	print 'pref_start conds are: ',[a.asPDDL() for a in pref_start]
	print 'prew_start conds are: ',[a.asPDDL() for a in prew_start]
	print 'pref_inv conds are: ',[a.asPDDL() for a in pref_inv]
	print 'pref_end conds are: ',[a.asPDDL() for a in pref_end], '\n'
	print 'the  negative conditions are: '
	print 'pref_start negative conds are: ',[a.asPDDL() for a in neg_pref_start]
	print 'prew_start negative conds are: ',[a.asPDDL() for a in neg_prew_start]
	print 'pref_inv negative conds are: ',  [a.asPDDL() for a in neg_pref_inv]
	print 'pref_end negative conds are: ',  [a.asPDDL() for a in neg_pref_end], '\n'
	print '\n################## effects ##################'
	print '\nadd start effects are: ',[a.asPDDL() for a in add_start]
	print 'del start effects are: ',[a.asPDDL() for a in del_start]
	print 'add end effects are: ',[a.asPDDL() for a in add_end]
	print 'del end effects are: ',[a.asPDDL() for a in del_end], '\n'
	return

def debug():
	get_preds = False
	get_agents = False
	make_funcs = False
	make_consts = False
	make_action_s = False
	make_action_fstart = False
	make_action_fend = False
	make_action_finv_start = False
	make_action_finv_end = False
	make_action_wx = False
	make_action_end_s = False
	make_action_end_f = False
	make_goals = False
	make_initial_state = False
	getObjectsOfType_test = False
	make_compiled_domain = True
	make_compiled_problem = True
	print '\n'*100
	if get_preds:
		print '\n'*3,'Compiling predicates ...'
		preds = MakePredicates(dom, prob, params)
	if get_agents:
		print '\n'*3,\
		'Agents type name is: ',params.agentTypename,', Getting agents now ...'
		constants = MakeConstants(dom, prob)
		agents = GetAgents(constants, params)
		print 'the agents are: ', [a.asPDDL() for a in agents]
	if make_funcs:
		funcs = MakeFunctions(dom, prob, waitlist, True)
	if make_consts:
		print 'Getting constants now ...'
		constants = MakeConstants(dom, prob)
		print 'the constants are:\n', constants.asPDDL()
	if make_action_s:
		print '\ncompiling action_s, Good Luck !'
		action = dom.durative_actions[2]
		constants = MakeConstants(dom, prob)
		action_s = MakeActions_s(action, constants, params)
		print '\ncompiled action info:'
		printActionBasicInfo(action_s, params)
	if make_action_fstart:
		print '\ncompiling action_fstart, Good Luck !'
		action = dom.durative_actions[1]
		print '\noriginal action info:'
		printActionBasicInfo(action, params)
		constants = MakeConstants(dom, prob)
		actions_fstart = MakeActions_fstart(action, constants, params)
		print '\ncompiled action info:'
		printActionBasicInfo(actions_fstart[0], params)
	if make_action_fend:
		print '\ncompiling action_fend, Good Luck !'
		action = dom.durative_actions[0]
		print '\noriginal action info:'
		printActionBasicInfo(action, params)
		constants = MakeConstants(dom, prob)
		actions_fend = MakeActions_fend(action, constants, params)
		print '\ncompiled action info:'
		printActionBasicInfo(actions_fend[0], params)
	if make_action_finv_start:
		print '\ncompiling action_finv_start, Good Luck !'
		action = dom.durative_actions[0]
		print '\noriginal action info:'
		printActionBasicInfo(action, params)
		constants = MakeConstants(dom, prob)
		action_finv_start = MakeAction_finv_start(action, constants, params)
		print '\ncompiled action info:'
		printActionBasicInfo(action_finv_start, params)
	if make_action_finv_end:
		print '\ncompiling action_finv_start, Good Luck !'
		action = dom.durative_actions[0]
		print '\noriginal action info:'
		printActionBasicInfo(action, params)
		constants = MakeConstants(dom, prob)
		action_finv_end = MakeAction_finv_end(action, constants, params)
		print '\ncompiled action info:'
		printActionBasicInfo(action_finv_end, params)
	if make_action_wx:
		print '\ncompiling action_finv_start, Good Luck !'
		action = dom.durative_actions[0]
		print '\noriginal action info:'
		printActionBasicInfo(action, params)
		constants = MakeConstants(dom, prob)
		action_wx = MakeActions_Wait(action, constants, params)
		print '\ncompiled action info:'
		printActionBasicInfo(action_wx[0], params)
	if make_action_end_s:
		end_s_actions = MakeActions_end_s(dom, prob, params)
	if make_action_end_f:
		end_f_actions = MakeActions_end_f(dom, prob, params)
		print 'the comiled action is:'
		print end_f_actions[0].asPDDL()
	if make_goals:
		print 'compiling goals:'
		goal_state = MakeGoalState(dom, prob, params)
	if make_initial_state:
		print 'compiling initial state:'
		constants = MakeConstants(dom, prob)
		initial_state = MakeInitialState_new(dom, prob, constants, params)
	if getObjectsOfType_test:
		getObjectsOfType(dom, prob, 'locatable', params)
	return;

if __name__ == "__main__":
	params = CompilationParameters()
	params.waitlist = ['at', 'rested']
	params.agentslist = ['driver1', 'driver2']
	params.agentTypename = 'driver'
	params.agentTypeparameter = 'driver' # e.g ?driver
	params.domain_path =  '../expfiles/driverlog/corrected_domain.pddl'
	params.problem_path = '../expfiles/driverlog/p0.pddl'
	params.print_condition = False

	(dom,prob) = pddl.parseDomainAndProblem(params.domain_path, params.problem_path)

	make_compiled_domain = True
	make_compiled_problem = True
	make_files = True

	print '\n'*100

	if make_compiled_domain:
		print 'Compiling new domain ...'
		c_domain = MakeDomain(dom, prob, params)
		print 'Compiling new domain complete.\n'
		if make_files:
			c_domain_file = open('c_domain_file_tmp.pddl','wb')
			c_domain_file.write(c_domain.asPDDL())
			c_domain_file.close()

	if make_compiled_problem:
		print 'Compiling new problem ...'
		c_problem = MakeProblem(dom, prob, params)
		print 'Compiling new problem complete.\n'
		if make_files:
			c_problem_file = open('c_problem_file_tmp.pddl','wb')
			c_problem_file.write(c_problem.asPDDL())
			c_problem_file.close()
