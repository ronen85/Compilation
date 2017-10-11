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

def printBasicInfo(action, waitlist):
    # grab basic conditions
    pref_start = GrabCond('pref_start', action, waitlist)
    prew_start = GrabCond('prew_start', action, waitlist)
    pref_inv = GrabCond('pref_inv', action, waitlist)
    pref_end = GrabCond('pref_end', action, waitlist)
    # grab basic effects
    add_start = GrabEff('add_start', action)
    del_start = GrabEff('del_start', action)
    add_end = GrabEff('add_end', action)
    del_end = GrabEff('del_end', action)
    # print info
    print '\npref_start conds are: ',[a.asPDDL() for a in pref_start]
    print 'prew_start conds are: ',[a.asPDDL() for a in prew_start]
    print 'pref_inv are: ',[a.asPDDL() for a in pref_inv]
    print 'pref_end are: ',[a.asPDDL() for a in pref_end], '\n'
    print '\nadd start effects are: ',[a.asPDDL() for a in add_start]
    print 'del start effects are: ',[a.asPDDL() for a in del_start]
    print 'add end effects are: ',[a.asPDDL() for a in add_end]
    print 'del end effects are: ',[a.asPDDL() for a in del_end], '\n'
    return

if __name__ == "__main__":
    waitlist = ['working']
    agentslist = ['d0', 'd1']
    agentTypename = 'driver'
    agentTypeparameter = 'driver' # e.g ?driver
    domain_path =  '../expfiles/driverlog/domain.pddl'
    problem_path = '../expfiles/driverlog/pfile1.pddl'
    (dom,prob) = pddl.parseDomainAndProblem(domain_path, problem_path)
    params = CompilationParameters(domain_path, problem_path, agentTypename, agentTypeparameter, waitlist)

    get_preds = True
    get_agents = False
    make_funcs = False
    make_consts = False
    make_action_s = False
    make_action_fstart = False
    print_condition = True
    print '\n'*100
    if get_preds:
        print '\n'*3,'Compiling predicates ...'
        MakePredicates(dom, prob, params)
    if get_agents:
        print '\n'*3,\
        'Agents type name is: ',agentTypename,', Getting agents now ...'
        constants = MakeConstants(dom, prob)
        agents = GetAgents(constants, agentTypename)
        print 'the agents are: ', [a.asPDDL() for a in agents]
    if make_funcs:
        funcs = MakeFunctions(dom, prob, waitlist, True)
    if make_consts:
        print 'Getting constants now ...'
        constants = MakeConstants(dom, prob, True)
    if make_action_s:
        print '\ncompiling action_s, Good Luck !'
        action = dom.durative_actions[0]
        constants = MakeConstants(dom, prob)
        printBasicInfo(action, waitlist)
        action_s = MakeActions_s(action, constants, waitlist, agentTypename, agentTypeparameter, print_condition = True)
    if make_action_fstart:
        action = dom.durative_actions[1]
        print '\nthe action is: ', action.name
        print 'compiling actions_fstart, Good Luck !'
        constants = MakeConstants(dom, prob)
        printBasicInfo(action, waitlist)
        actions_fstart = MakeActions_fstart(action, constants, waitlist, print_condition)
