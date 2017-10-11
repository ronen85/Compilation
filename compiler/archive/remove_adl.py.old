#!/usr/bin/env python
# -*- coding: utf-8 -*-



#
# status: not released !!!
# this program grabs PDDL problem and domain and removes 'not' from:
# - preconditions
# - goal
# in order to save the data we make the following changes:
# - predicates:
#     for all predicates in domain :
# 	copy and add 'isnt-' to name
# - actions:
#     for all actions
# 	for all conditions in action
# 		if op = not
# 			op = None
# 			cond.name = isnt + cond.name
# 	for all effects in action
# 		if op = None
# 			add effect with
# 				op = not
# 				eff.name += isnt
# 		else if op = not
# 			add effect with
# 				op = None
# 				eff.name += isnt
# - intial state:
#     for all possible predicates not in the original initial state
#     	add predicate with pred.name += isnt
# - goals:
#     if goal.op = not
# 		goal.op = None
# 		goal.name += isnt
# """
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

def makeADLfreePredicates(predicates):
    adlFreePredicates = []
    for pred in predicates:
        one_pred = deepcopy(pred)
        second_pred = deepcopy(pred)
        second_pred.name = 'isnt-' + second_pred.name
        adlFreePredicates += [one_pred, second_pred]
    # print map(lambda x: x.asPDDL(), adlFreePredicates)
    return adlFreePredicates

def makeADLfreePreconditions(pre):
    adlFreesubformulas = []
    for subform in pre.subformulas:
        if subform.op == 'not':
            adlfreeName = 'isnt-' + subform.subformulas[0].subformulas[0].name
            adlfreeArgs = deepcopy(subform.subformulas[0].subformulas[0].args)
            adlfreePred = pddl.Predicate(adlfreeName, adlfreeArgs)
            adlfreeForm = pddl.Formula([adlfreePred], None)
            newPreCond = pddl.Formula([adlfreeForm], None)
            adlFreesubformulas.append(newPreCond)
        else:
            adlFreesubformulas.append(deepcopy(subform))
    adlFreePre = pddl.Formula(adlFreesubformulas, op = 'and')
    # print adlFreePre.asPDDL()
    return adlFreePre

def makeADLfreeDurativePreonditions(durative_action):
    adlfreeCondsList = []
    for cond in durative_action.cond:
        # print 'the cond is: ', cond.asPDDL()
        if cond.formula.op == 'not':
            adlFreecond_name = 'isnt-' + cond.formula.subformulas[0].subformulas[0].name
            adlFreecond_args = deepcopy(cond.formula.subformulas[0].subformulas[0].args)
            adlFreecond_pred = pddl.Predicate(adlFreecond_name, adlFreecond_args)
            adlFreecond_subform = [ adlFreecond_pred ]
            adlFreecond_form = pddl.Formula([pddl.Formula(adlFreecond_subform)], None)
            adlFreecond = pddl.TimedFormula(cond.timespecifier, adlFreecond_form )
        else:
            adlFreecond = deepcopy(cond)
        adlfreeCondsList.append(adlFreecond)
    # print '\nthe original conditions are: ', map(lambda x: str(x.asPDDL()), durative_action.cond)
    # print 'the comiled conditions are: ', map(lambda x: str(x.asPDDL()), adlfreeCondsList)
    return adlfreeCondsList

def makeADLfreeEffects(effects):
    adlFreeEffs = []
    for eff in effects:
        # print 'the effect is: ', eff.asPDDL()
        if eff.op == None:
            adlFreeEffs.append(deepcopy(eff))
            predArgs = deepcopy(eff.subformulas[0].args)
            predName = 'isnt-' + eff.subformulas[0].name
            negEffpred = pddl.Predicate(predName, predArgs)
            negEffsubforms = [ negEffpred ]
            negEff = pddl.Formula(negEffsubforms, 'not')
            adlFreeEffs.append(negEff)
        elif eff.op == 'not':
            adlFreeEffs.append(deepcopy(eff))
            predArgs = deepcopy(eff.subformulas[0].args)
            predName = 'isnt-' + eff.subformulas[0].name
            negEffpred = pddl.Predicate(predName, predArgs)
            negEffsubforms = [ negEffpred ]
            negEff = pddl.Formula(negEffsubforms, None)
            adlFreeEffs.append(negEff)
    # print map(lambda x: x.asPDDL(), adlFreeEffs )
    return adlFreeEffs

def makeADLfreeDurativeEffects(durative_action):
    adlFreeEffs = []
    for eff in durative_action.eff:
        # print 'the effect is:', eff.asPDDL()
        adlFreeEffs.append(deepcopy(eff))
        if eff.formula.op == 'not':
            # print 'this is a not effect'
            adlFreeEff_name = 'isnt-' + eff.formula.subformulas[0].name
            adlFreeEff_args = deepcopy(eff.formula.subformulas[0].args)
            adlFreeEff_pred = pddl.Predicate(adlFreeEff_name, adlFreeEff_args)
            adlFreeEff_subform = [ adlFreeEff_pred ]
            adlFreeEff_form = pddl.Formula(adlFreeEff_subform , None)
            adlFreeEff = pddl.TimedFormula(eff.timespecifier, adlFreeEff_form)
            adlFreeEffs.append(adlFreeEff)
        elif eff.formula.op == None:
            # print 'this is a normal effect'
            adlFreeEff_name = 'isnt-' + eff.formula.subformulas[0].name
            adlFreeEff_args = deepcopy(eff.formula.subformulas[0].args)
            adlFreeEff_pred = pddl.Predicate(adlFreeEff_name, adlFreeEff_args)
            adlFreeEff_subform = [ adlFreeEff_pred ]
            adlFreeEff_form = pddl.Formula(adlFreeEff_subform , 'not')
            adlFreeEff = pddl.TimedFormula(eff.timespecifier, adlFreeEff_form)
            adlFreeEffs.append(adlFreeEff)
    # print '\n'*2,'the action is: ', durative_action.name
    # print 'the original effects are: ', map(lambda x: str(x.asPDDL()), durative_action.eff)
    # print 'the comiled effects are: ', map(lambda x: str(x.asPDDL()), adlFreeEffs)
    return adlFreeEffs

def makeADLfreeActions(action):
    adlFreeActions = []
    name = action.name
    parameters = deepcopy(action.parameters)
    pre = makeADLfreePreconditions(action.pre)
    eff = makeADLfreeEffects(action.eff)
    adlFreeAct = pddl.Action(name, parameters, pre, eff)
    adlFreeActions.append(adlFreeAct)
    # print adlFreeAct.asPDDL()
    return adlFreeActions

def makeADLfreeDurativeActions(durative_action):
    adlFreeActions = []
    dact_name = durative_action.name
    dact_parameters = deepcopy(durative_action.parameters)
    dact_duration_lb = durative_action.duration_lb
    dact_duration_ub = durative_action.duration_ub
    # print 'start compiling durative actions condtions ...'
    dact_cond = makeADLfreeDurativePreonditions(durative_action)
    dact_eff = makeADLfreeDurativeEffects(durative_action)
    daction = pddl.DurativeAction(dact_name, dact_parameters, dact_duration_lb, dact_duration_ub, dact_cond, dact_eff)
    adlFreeActions.append(daction)
    return adlFreeActions

def makeADLfreeDomain(dom, print_condition = False):
    print 'Making ADL free domain ...'
    name = dom.name + '_no_adl'
    reqs = deepcopy(dom.reqs)
    types = deepcopy(dom.types)
    constants = deepcopy(dom.constants)
    predicates = makeADLfreePredicates(dom.predicates)
    functions = deepcopy(dom.functions)
    actions = []
    for i in range(len(dom.actions)):
        actions += makeADLfreeActions(dom.actions[i])
    durative_actions = []
    # print 'start compiling durative actions ...'
    for i in range(len(dom.durative_actions)):
        durative_actions += makeADLfreeDurativeActions(dom.durative_actions[i])
    no_adl_dom = pddl.Domain(name, reqs, types, constants, predicates, functions, actions, durative_actions)
    return no_adl_dom;

def grabNotConds(dom,prob):
    notConds = []
    for action in dom.actions:
        # print action.name
        for subform in action.pre.subformulas:
            if subform.op == 'not':
                # print subform, subform.asPDDL()
                notConds.append(subform)
    for dact in dom.durative_actions:
        # print dact.name
        for cond in dact.cond:
            if cond.formula.op == 'not':
                # print cond, cond.asPDDL()
                notConds.append(cond.formula)
    print 'the not conditions in domain action are:'
    print map(lambda x: x.asPDDL(), notConds)
    return deepcopy(notConds)

def makeADLfreeInitialstate(dom, prob):
    adlFreeInitialstate = []
    domPreds = makeADLfreePredicates(dom.predicates)
    notConds = grabNotConds(dom,prob) # will get all 'not' conditions from actions

    for form in prob.initialstate:
        print 'the original initial state formula is: ', form.asPDDL()
    return adlFreeInitialstate

def makeADLfreeGoal(goal):
    return

def makeADLfreeProblem(dom, prob):
    name = prob.name + '_no_adl'
    domainname = dom.name + '_no_adl'
    objects = deepcopy(prob.objects)
    initialstate = makeADLfreeInitialstate(dom, prob)
    goal = makeADLfreeGoal(prob.goal)
    metric = prob.metric
    no_adl_prob = pddl.Problem(name, domainname, objects, initialstate, goal , metric)
    return no_adl_prob
# def main():
#     parse = True
#     remove_adl = False
#     print_condition = True
#     domain_path = '../expfiles/drink/drink-world-ADL.pddl'
#     problem_path = '../expfiles/drink/drink-prob-ADL.pddl'
#     if parse:
#         (dom,prob) = pddl.parseDomainAndProblem(domain_path, problem_path)
#     if remove_adl:
#         no_adl_dom = makeADLfreeDomain(dom)
#     return

if __name__ == "__main__":
    print '\n'*50
    parse = True
    remove_adl = True
    print_condition = True
    domain_path = '../expfiles/drink/drink-world-ADL.pddl'
    problem_path = '../expfiles/drink/drink-prob-ADL.pddl'
    if parse:
        (dom,prob) = pddl.parseDomainAndProblem(domain_path, problem_path)
    if remove_adl:
        no_adl_dom = makeADLfreeDomain(dom)
        no_adl_prob = makeADLfreeProblem(dom, prob)
    # main()
