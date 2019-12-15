#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 18:51:40 2019

@author: Falcon
"""
class SM:
    startState = None
    LegalInputs = []
    name = None
#    def __init__(self):
#        self.start()
    def getStartState(self):
        return self.startState
    def getNextValues(self, state, inp):
        nextState = self.getNextState(state, inp)
        return nextState, nextState
    def start(self):
        self.state = self.startState     
    def get_state(self):
        return self.state       
    def step(self, inp):
        s, o = self.getNextValues(self.state, inp)
        self.state = s
        return o   
    def transduce(self, inputs):
        self.start()
        return [self.step(inp) for inp in inputs if not self.done(self.state)]    
    def run(self, n = 10):
        return self.transduce([None]*n)    
    def done(self, state):
        return False
    
class Adder(SM):
    def getNextState(self, state, inp):
        i1, i2 = splitValue(inp)
        return safeAdd(i1, i2)   
    
class Multiplier(SM):
    def getNextState(self, state, inp):
        i1, i2 = splitValue(inp)
        return safeMul(i1, i2)   

class Accumulator(SM):
    def __init__(self, init):
        self.startSate = init
    def getNextState(self, state, inp):
        return state + inp
    
    
class Gain(SM):
    def __init__(self, k):
        self.k = k
    def getNextState(self, state, inp):
        return inp * self.k
    
    
class Delay(SM):
    def __init__(self, v0):
        self.startState = v0  
        SM.__init__(self)
    def getNextValues(self, state, inp):
        return inp, state
 
    
class Increment(SM):
    def __init__(self, incr):
        self.incr = incr  
        SM.__init__(self)
    def getNextState(self, state, inp):
        return safeAdd(inp, self.incr)


class Wire(SM):
    def getNextState(self, state, inp):
        return inp
    
    
class SMC(SM):
    def __init__(self, sm1, sm2):
        self.startState = (sm1.getStartState(), sm2.getStartState())
        self.sm1 = sm1
        self.sm2 = sm2 
    
#    def start(self): # manipulation
#        SM.start(self)
#        self.sm1.start()
#        self.sm2.start()


class Cascade(SMC):
    def getNextValues(self, state, inp): #pure function
        s1, s2 = state
        newS1, o1 = self.sm1.getNextValues(s1,inp)
        newS2, o2 = self.sm2.getNextValues(s2,o1)
        return ((newS1, newS2), o2)
    

class Parallel(SMC):               
    def getNextValues(self, state, inp):
        s1, s2 = state
        newS1, o1 = self.sm1.getNextValues(s1,inp)
        newS2, o2 = self.sm2.getNextValues(s2,inp)
        return ((newS1, newS2),(o1, o2))
    
class Parallel2(Parallel):
    def getNextValues(self, state, inp):
        s1, s2 = state
        i1, i2 = splitValue(inp)
        newS1, o1 = self.sm1.getNextValues(s1,i1)
        newS2, o2 = self.sm2.getNextValues(s1,i2)
        return ((newS1, newS2),(o1, o2))
    
class Feedback(SM):
    def __init__(self, sm):
        self.startState = sm.startState
        self.sm = sm
                
    def getNextValues(self, state, inp):
        ignore, o = self.sm.getNextValues(state, 'undefined')   
        newS, ignore = self.sm.getNextValues(state, o)
        return newS, o
    
#    def start(self):
#        SM.start(self)
#        self.m.start()
        
class Feedback2(Feedback):
    def getNextValues(self, state, inp):
        ignore, o = self.sm.getNextValues(state, (inp,'undefined'))   
        newS, ignore = self.sm.getNextValues(state, (inp, o))
        return (newS, o)
    
class FeedbackAdd(SMC):
    def getNextValues(self, state, inp):
        s1, s2 = state
#        i1, i2 = inp
        ignore, o2 = self.sm2.getNextValues(s2, 'undefined')
        ignore, correct_o1 = self.sm1.getNextValues(s1, safeAdd(inp, o2))
        NewS2, correct_o2 = self.sm2.getNextValues(s2, correct_o1)
        NewS1, ignore = self.sm1.getNextValues(s1, safeAdd(correct_o2,inp))
        return (NewS1,NewS2),correct_o1
#        ignore, o2 = self.sm2.getNextValues(s2, 'undefined')
#        NewS1, o1 = self.sm1.getNextValues(s1, safeAdd(inp, o2))
#        NewS2, ignore = self.sm2.getNextValues(s2, o1)
#        return (NewS1,NewS2),o1
        
class Switch(SMC):
    def __init_(self,condition, sm1, sm2):
        SMC.__init__(self, sm1, sm2)
        self.condition = condition
    def getNextValues(self, state, inp):
        s1,s2 = state
        if self.condition(inp):
            ns1, o1 = self.sm1.getNextValues(s1, inp)
            return (ns1,s2),o1
        else:
            ns2, o2 = self.sm2.getNextValues(s2, inp)
            return (s1,ns2),o2
        

class Mux(Switch):
    def getNextValues(self, state, inp):
        s1,s2 = state
        ns1, o1 = self.sm1.getNextValues(s1, inp)
        ns2, o2 = self.sm2.getNextValues(s2, inp)
        if self.condition(inp):   
            return (ns1,ns2),o1
        else:
            return (ns1,ns2),o2   
        
class If(SM):
    startState = ('start', None)
    def __init__(self, condition, sm1, sm2):
        self.sm1 = sm1
        self.sm2 = sm2
        self.condition = condition
#    def start(self):
#        SM.start(self)
#        self.sm1.start()
#        self.sm2.start()
    def getFirstRealState(self, inp):
        if self.condition(inp):
            return('runningM1', self.sm1.startState)
        else:
            return('runningM2', self.sm2.startState)
    def getNextValues(self, state, inp):
        ifState, smState = state
        if ifState == 'start':
            (ifState, smState) = self.getFirstRealState(inp)
        elif ifState == 'runningM1':
            (newS, o) = self.sm1.getNextValues(smState, inp)
            return (('runningM1', newS), o)
        else:
            (newS, o) = self.sm2.getNextValues(smState, inp)
            return (('runningM2', newS), o)
        
        

def Counter(init, step):
    return Feedback(Cascade(Increment(step), Delay(init)))

def coupleMachine(sm1,sm2):
    return Feedback(Cascade(sm1,sm2))
        
a = FeedbackAdd(Delay(0), Wire())
b = FeedbackAdd(Wire(), Delay(0))
fact= Cascade(Counter(1,1),Feedback2(Cascade(Multiplier(),Delay(1))))
        
class ConsumeFiveValues(SM):
    startState = 0,0 # count, total
    def getNextValues(self, state, inp):
        c, t = state
        if c == 4:
            return (5, t+inp), t+inp
        else:
            return (c+1, t+inp), None
    def done(self, state):
        c, t = state
        return c == 5
    
class Repeat(SM):
    def __init__(self, sm, n = None):
        self.sm = sm
        self.startState = 0, self.sm.startState
        self.n = n
    def advanceIfDone(self, counter, smState):
        # suppose to use while for some magical reason
        if self.sm.done(smState) and not self.done((counter, smState)):
            counter += 1
            smState = self.sm.startState
        return (counter, smState)
    def getNextValues(self, state, inp):
        counter, smState = state
        smState, o = self.sm.getNextValues(smState, inp)
        counter, smState = self.advanceIfDone(counter, smState)
        return (counter, smState),o
    def done(self, state):
        counter, smState = state
        return counter == self.n
#    def start(self):
#        SM.start(self)
#        self.sm.start()
        
class CharTSM(SM):
    startState = False
    def __init__(self, c):
        self.c = c
    def getNextValues(self, state, inp):
        return (True, self.c)
    def done(self, state):
        return state
    
a = CharTSM('a')
a = Repeat(a, 5)
        
class Sequence(SM):
#    def start(self):
#        SM.start(self)
#        self.smList[0].start()
    def __init__(self, smList):
        self.smList = smList
        self.startState = (0, self.smList[0].startState)
        self.n = len(smList)
    def getNextValues(self, state, inp):
        counter, smState = state
        smState, o = self.smList[counter].getNextValues(smState, inp)
        counter, smState = self.advanceIfDone(counter, smState)
        return (counter, smState), o
    def advanceIfDone(self, counter, smState):
        if self.done((counter,smState)) and counter < self.n-1:
            counter += 1
            smState = self.smList[counter].startState
            self.smList[counter].start()
        return counter, smState
    def done(self, state):
        counter, smState = state
        return self.smList[counter].done(smState)
    
m = Sequence([CharTSM('a'), CharTSM('b'), CharTSM('c')])

def makeTextSequence(s):
    return Sequence([CharTSM(c) for c in s])

m = makeTextSequence('Hello World')
m = Repeat(makeTextSequence('abc'), 3)

class RepeatUntil(SM):
#    def start(self):
#        SM.start(self)
#        self.sm.start()
    def __init__(self, condition, sm):
        self.sm = sm
        self.condition = condition
        self.startState = (False, self.sm.startState)
    def getNextValues(self, state, inp):
        CondTrue, smState = state
        smState, o = self.sm.getNextValues(smState, inp)
        condTrue = self.condition(inp)
        if self.sm.done(smState) and not condTrue:
            smState = self.sm.getStartState()
        return ((condTrue), smState), o
    def done(self, state):
        condTrue, smState = state
        return self.sm.done(smState) and condTrue

def gT10(x):
    return x>10

m = RepeatUntil(gT10, ConsumeFiveValues())
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
def safeAdd(arg1, arg2):
    u = [None, 'undefined']
    if arg1 in u and arg2 in u:
        return 'undefined'
    elif arg1 in u:
        return arg2
    elif arg2 in u:
        return arg1
    elif isinstance(arg1, int) and isinstance(arg2, int):
        return arg1 + arg2
    else:
        return 'undefined'
    
def safeMul(arg1, arg2):
    u = [None, 'undefined']
    if arg1 in u and arg2 in u:
        return 'undefined'
    elif arg1 in u:
        return arg2
    elif arg2 in u:
        return arg1
    elif isinstance(arg1, int) and isinstance(arg2, int):
        return arg1 * arg2
    else:
        return 'undefined'
    
def safeMul2(arg1, arg2):
    try:
        return int(arg1 * arg2)
    except:
        return 'undefined'
    
def splitValue(v):
    if v == 'undefined':
        return ('undefined', 'undefined')
    else:
        return v
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    