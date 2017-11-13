#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append("../pythonpddl")
sys.path.append("../compiler")
import pddl
from antlr4 import *
import pddlLexer
import pddlParser
import itertools
from copy import deepcopy
from compilation_v1 import *

def findNegPreds(dom):
    """
    this function purpose is to:
    - find all of the negative preconditions in the domain (both DA's and A's).
    - return the name of the negative preconditions predicates.
    dom is a pddl.Domain, negPreds is a list (e.g [u'hold-cup', u'full', u'at-g'])
    """
    print_condition = False
    negPreds = []
    for durative_action in dom.durative_actions:
        if print_condition: print durative_action.name
        for cond in durative_action.cond:
            if print_condition: print ' ', cond.asPDDL()
            if cond.formula.op == 'not':
                if print_condition: print '  this is a negPred'
                negPreds.append(cond.formula.subformulas[0].subformulas[0].name)
    if print_condition: print '\n'*5
    for action in dom.actions:
        if print_condition: print action.name
        for cond in action.pre.subformulas:
            if print_condition: print ' ', cond.asPDDL()
            if cond.op == 'not':
                if print_condition: print '  this is a negPred'
                negPreds.append(cond.subformulas[0].subformulas[0].name)
    negPreds = list(set(negPreds))
    if print_condition: print '\nthe negPreds are: ', negPreds
    return negPreds

def makeReversePred(negPred):
    """
    negPred is pddl.Predicate
    this function returns the reversed version of the predicate
    e.g (on-table ?c - cup) --> (isnt-on-table ?c - cup)
    """
    revNegPred = deepcopy(negPred)
    revNegPred.name = 'isnt-'+ revNegPred.name
    # print 'the reverse predicate is: ', revNegPred.asPDDL()
    return revNegPred

def fixDomPredicates(dom):
    """
    this function purpose is to:
    - recieve a pddl.Domain object
    - grab the negative predicates with findNegPreds function.
    - go through all the predicates in the domain.
        - insert the predicate into a new list newPreds
        - if the predicate is a negative predicate
            - make a reversed copy with makeReversePred function
            - insert the reversed copy to newPreds list
    - return the list of predicates
    """
    print_condition = False
    newPreds = []
    negPreds = findNegPreds(dom)
    for pred in dom.predicates:
        if print_condition: print 'predicate name is: ', pred.name
        newPreds.append(deepcopy(pred))
        if pred.name in negPreds:
            if print_condition: print '  this is a negetive predicate'
            newPreds.append(makeReversePred(pred))
    if print_condition:
        print '\n'*5
        for pred in newPreds:
            print pred.asPDDL()
    return newPreds;

def effTofix(input_effect):
    if isinstance(input_effect, pddl.TimedFormula):
        eff = input_effect.formula
    elif isinstance(input_effect, pddl.Formula):
        eff = input_effect
    else:
        print 'the input_effect type is: ', input_effect
        print 'ERROR WITH EFFECT TYPE - 1'
    print_condition = False
    if print_condition: print '   the eff to be fixed is ' , eff.asPDDL()
    fixedEffs = []
    fixedEffs.append(deepcopy(eff))
    reversedEff = deepcopy(eff)
    if eff.op == None:
        if eff.subformulas[0].name.startswith('isnt-'):
            # e.g :(isnt-act ...) ->
            #      (isnt-act ...) + (not (act ...))
            if print_condition: print '   this is an add effect'
            if print_condition: print '   this is an negetive (isnt) effect' # (isnt-on-table ?c)
            reversedEff.op = 'not'
            reversedEff.subformulas[0].name = reversedEff.subformulas[0].name[5:]
            fixedEffs.append(reversedEff)
        else:
            #  e.g :(act ...) ->
            #       (act ...) + (not (isnt-act ...))
            if print_condition: print '   this is an add effect'
            if print_condition: print '   this is an positive effect'
            reversedEff.op = 'not'
            reversedEff.subformulas[0].name = 'isnt-' + reversedEff.subformulas[0].name
            fixedEffs.append(reversedEff)
    elif eff.op == 'not':
        if eff.subformulas[0].name.startswith('isnt-'):
            # e.g :(not (isnt-act ...)) ->
            #      (not (isnt-act ...)) + (act ...))
            if print_condition: print '   this is an del effect'
            if print_condition: print '   this is an negetive (isnt) effect'
            reversedEff.op = None
            reversedEff.subformulas[0].name = reversedEff.subformulas[0].name[5:]
            fixedEffs.append(reversedEff)
        else:
            # e.g :(not (act ...)) ->
            #      (not (act ...)) + (isnt-act ...))
            if print_condition: print '   this is an del effect'
            if print_condition: print '   this is an positive effect'
            reversedEff.op = None
            reversedEff.subformulas[0].name = 'isnt-' + reversedEff.subformulas[0].name
            fixedEffs.append(reversedEff)
    else:
        print 'op is not clear (not None nor not)'

    if print_condition: print '   the corrected effects are: ', [e.asPDDL() for e in fixedEffs]

    if isinstance(input_effect, pddl.TimedFormula):
        timedFixedEffs = []
        for eff in fixedEffs:
            timespecifier = input_effect.timespecifier
            timedEff = pddl.TimedFormula(timespecifier, eff)
            timedFixedEffs.append(timedEff)
        return timedFixedEffs
    elif isinstance(input_effect, pddl.Formula):
        return fixedEffs
    else:
        print 'ERROR WITH EFFECT TYPE - 2'
        return

def fixActionEffs(action, dom):
    """
    input: action and domian
    output: fixed action
    what to fix ?
    - loop over all effects
    - if the predicate of the effect apears in a negetive precondition in the domain
      - add isnt-pred to the effects
    - returns a fixed action
    """
    print_condition = True
    if isinstance(action, pddl.Action):
        fixedAction = deepcopy(action)
        if print_condition: print '\n\n\nstart fixActionEffs for regular action ...'
        negPreds = findNegPreds(dom)
        newEffs = []
        if print_condition: print '\nthe actions effects are:\n', [e.asPDDL() for e in action.eff]
        if print_condition: print '\nnegPreds are: \n', negPreds
        for eff in action.eff:
            if not eff.subformulas[0].name in negPreds:
                newEffs.append(deepcopy(eff))
            else:
                newEffs += effTofix(eff)
        fixedAction.eff = newEffs
        if print_condition: print '\n'*4, 'the new effects are: ', [e.asPDDL() for e in fixedAction.eff]
        return fixedAction.eff
    elif isinstance(action, pddl.DurativeAction):
        fixedAction = deepcopy(action)
        if print_condition: print '\n\n\nstart fixActionEffs for durative action ...'
        negPreds = findNegPreds(dom)
        newEffs = []
        if print_condition: print '\nthe actions effects are:\n', [e.asPDDL() for e in action.eff]
        if print_condition: print '\nnegPreds are: \n', negPreds
        for eff in action.eff:
            if not eff.formula.subformulas[0].name in negPreds:
                newEffs.append(deepcopy(eff))
            else:
                newEffs += effTofix(eff)
        fixedAction.eff = newEffs
        if print_condition: print '\nthe new effects are:\n', [str(e.asPDDL()) for e in fixedAction.eff]
        return fixedAction.eff
    else:
        print 'action type is: ', action
        print 'ERROR WITH ACTION TYPE'
        return None

def fixActionConds(act):
    """
    input:
        act: pddl.DurativeAction/pddl.Action
        domain: pddl.domain
    output:
        fixedConds: list of pddl.Formulas / pddl.Formula

    purpose :
        remove and modify all of the negative condtions
        (e.g not(act ...) -> (isnt-act ...))
    """
    print_condition = True
    if isinstance(act, pddl.DurativeAction):
        if print_condition: print '  this is pddl.DurativeAction'
        fixedAct = deepcopy(act)
        fixedConds = []
        for cond in act.cond:
            if print_condition: print '  the cond is: ', cond.asPDDL()
            if cond.formula.op == 'not':
                if print_condition: print '    this cond has op = not '
                fcond = deepcopy(cond)
                fcond.formula.op = None
                fcond.formula.subformulas[0].subformulas[0].name = 'isnt-' + fcond.formula.subformulas[0].subformulas[0].name
                if print_condition: print '    the fixed cond is: ', fcond.asPDDL()
                fixedConds.append(fcond)
            elif cond.formula.op == None:
                if print_condition: print '    this cond has op = None '
                fixedConds.append(deepcopy(cond))
            else:
                print '    ERROR WITH COND OP '
                return None
        fixedAct.cond = fixedConds
        if print_condition: print '  the new conds are: ', [c.asPDDL() for c in fixedAct.cond]
        return fixedAct.cond
    elif isinstance(act, pddl.Action):
        if print_condition: print 'this is pddl.Action'
        fixedAct = deepcopy(act)
        fixedSubforms = []
        for form in act.pre.subformulas:
            if print_condition: print ' form is: ', form.asPDDL()
            if form.op == None:
                fixedSubforms.append(deepcopy(form))
            elif form.op == 'not':
                if print_condition: print '   this op is not'
                fixedform = deepcopy(form)
                fixedform.op = None
                fixedform.subformulas[0].subformulas[0].name = 'isnt-' + fixedform.subformulas[0].subformulas[0].name
                fixedSubforms.append(fixedform)
        fixedPre = pddl.Formula(fixedSubforms, 'and')
        fixedAct.pre = fixedPre
        if print_condition: print 'the new conds are: '
        if print_condition: print fixedPre.asPDDL()
        return fixedAct.pre
    else:
        print 'ERROR: act instace is not Action.'
        return None

def makeInitStart(dom, prob):
    """
    input: parsed domain and problem.

    output: expended initial state as a list of pddl.Formula.

    porpuse:
    to remove the use of negative preconditions we call for "isnt-conds"
    e.g (not (act ...)) -> (isnt-act ...))
    there is a need to update the initial state respectively.
    the update: add "isnt-*" predicates to initial state
    algorithm:
    - get the relevant predicates using findNegPreds()
    - get the domain and problem objects
    - for every predicate make all possible options
    - if option is complied with original initial state:
      - add to newInitState[]
        else continue
    - return the original initial state with the above-mentioned list
    """
    newDomPreds = fixDomPredicates(dom)
    print "\nthe new domain predicates are:\n", [str(p.name) for p in newDomPreds]
    filteredPredList = filter(lambda x: x.name.startswith('isnt-'), newDomPreds)
    print "\nthe new and filtered domain predicates are:\n", [p.asPDDL() for p in filteredPredList]
    # print getObjectsOfType(dom, prob, 'agent')
    initialStateAdd = []
    for pred in filteredPredList:
        print '\nthe predicate is: ', pred.asPDDL()
        argumentsOptions = []
        for arg in pred.args.args:
            print '  the arg type is: ', arg.arg_type
            print '    the arg options are: ', getObjectsOfType(dom, prob, arg.arg_type)
            singleArgOptions = getObjectsOfType(dom, prob, arg.arg_type)
            argumentsOptions.append(singleArgOptions)
        print 'the options are: ', argumentsOptions
        argCombinations = itertools.product(*argumentsOptions)
        print '\nthe combinations are :'
        for comb in argCombinations:
            newPred = deepcopy(pred)
    return

if __name__ == "__main__":
    print '\n'*50
    parse = False
    print_condition = False
    find_negPreds = False
    make_reverse_negPred = False
    update_predicates_in_dom = False
    fix_action_conds = False
    fix_action_effs = False
    fix_durative_action_conds = False
    fix_durative_action_effs = False
    make_initial_state = True


    domain_path = '../expfiles/drink/drink-world-ADL.pddl'
    problem_path = '../expfiles/drink/drink-prob-ADL.pddl'

    if parse:
        (dom,prob) = pddl.parseDomainAndProblem(domain_path, problem_path)
        print 'Parse Complete.\n'

    if find_negPreds:
        print 'start looking for a neg pred'
        negPreds = findNegPreds(dom)


    if update_predicates_in_dom:
        (dom,prob) = pddl.parseDomainAndProblem(domain_path, problem_path)
        print 'making new predicates ...'
        preds = fixDomPredicates(dom)

    if fix_action_conds:
        (dom,prob) = pddl.parseDomainAndProblem(domain_path, problem_path)
        print 'start fixing action conds'
        action = dom.actions[0]
        fixed_conds = fixActionConds(action)

    if fix_action_effs:
        (dom,prob) = pddl.parseDomainAndProblem(domain_path, problem_path)
        print 'start fixing the effects of an aciton'
        action = dom.actions[0]
        effs = fixActionEffs(action, dom)

    if fix_durative_action_conds:
        (dom,prob) = pddl.parseDomainAndProblem(domain_path, problem_path)
        print '\n'*50
        print 'start fix_durative_action_conds:'
        dact = dom.durative_actions[3]
        print 'the action is: ', dact.name
        fixed_conds = fixActionConds(dact)

    if fix_durative_action_effs:
        print '\n'*50
        print 'start fix_durative_action_effs:'
        dact = dom.durative_actions[0]
        effs = fixActionEffs(dact, dom)

    if make_initial_state:
        (dom,prob) = pddl.parseDomainAndProblem(domain_path, problem_path)
        print '\n'*50
        print 'Start making Initial State: '
        fixedInit = makeInitStart(dom, prob)
