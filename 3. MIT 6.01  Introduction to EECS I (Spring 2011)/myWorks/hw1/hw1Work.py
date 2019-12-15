#import pdb
import sm
import string
import operator

class BinaryOp:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return self.opStr + '(' + \
               str(self.left) + ', ' +\
               str(self.right) + ')'
    __repr__ = __str__
    
#    def evaluation(self, env): # lazy partial evaluation
#        left = self.left.evaluation(env)
#        right = self.right.evaluation(env)
#        if isNum(left) and isNum(right):
#            return self.opr(left, right)
#        else:
#            return self.__class__(left, right)
        
        
    def evaluation(self, env): # eager evaluation
        return self.opr(self.left.evaluation(env), \
                              self.right.evaluation(env))
        
class Sum(BinaryOp):
    opStr = 'Sum'
    def opr(self, x, y):
        return operator.add(x,y)

class Prod(BinaryOp):
    opStr = 'Prod'
    def opr(self, x, y):
        return operator.mul(x,y)


class Quot(BinaryOp):
    opStr = 'Quot'
    def opr(self, x, y):
        return operator.truediv(x,y)

class Diff(BinaryOp):
    opStr = 'Diff'
    def opr(self, x, y):
        return operator.sub(x,y)


class Assign(BinaryOp):
    opStr = 'Assign'
    
#    def evaluation(self, env):#lazy partial
#        left = self.left.name
#        right = self.right
#        env[left] = right
    def evaluation(self, env): # eager
        left = self.left.name
        right = self.right.evaluation(env)
        env[left] = right
            
        
        
class Number:
    def __init__(self, val):
        self.value = val
    def __str__(self):
        return 'Num('+str(self.value)+')'
    __repr__ = __str__
    def evaluation(self, env):
        return self.value

class Variable:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'Var('+self.name+')'
    __repr__ = __str__
#    def evaluation(self, env): #lazy partial
#        key = self.name
#        value = env.get(key, None)
#        if value == None:
#            return self
#        else:
#            if type(value) == int or type(value) == float or type(value) == str:
#                return value
#            else:
#                return value.evaluation(env)
    def evaluation(self, env): #eager
        key = self.name
        value = env.get(key, None)
        if value == None:
            return key
        else:
            return value
        

# characters that are single-character tokens
seps = ['(', ')', '+', '-', '*', '/', '=']

# Convert strings into a list of tokens (strings)
def tokenize_0(string):
    out = []
    tem = ''
    for char in string:
        if char in seps:
            if len(tem) > 0:
                out.append(tem)
                tem = ''
            out.append(char)
        elif char == ' ':
            if len(tem) > 0:
                out.append(tem)
                tem = ''
        else:
            tem += char
        
    if len(tem)>0:
        out.append(tem)
    return out

class Tokenizer(sm.SM):
    def __init__(self):
        self.startState = ''
    def getNextValues(self, state, inp):
        if inp == ' ':
            return '', state
        elif inp in seps:
            return inp, state
        else:
            if state in seps:
                return inp, state
            else:
                return state + inp, ''

def tokenize(inputString):
    a = Tokenizer().transduce(inputString + ' ')
    n = a.count('')
    for i in range(n):
        a.remove('')
    return a

# tokens is a list of tokens
# returns a syntax tree:  an instance of {\tt Number}, {\tt Variable},
# or one of the subclasses of {\tt BinaryOp} 
def parse(tokens):
#    op = ['+', '-', '*', '/', '=']
    def parseExp(i):
        # t::=token i::=index
        t = tokens[i]
        #base case
        if numberTok(t):
            return Number(float(t)), i+1
        elif variableTok(t):
            return Variable(t), i+1
        elif t == '+':
            return Sum, i+1
        elif t == '-':
            return Diff, i+1
        elif t == '*':
            return Prod, i+1
        elif t == '/':
            return Quot, i+1
        elif t == '=':
            return Assign, i+1
        
        #recusive step
        elif t == '(':
            left_tree, nextIndex0 = parseExp(i+1)
            op_class, nextIndex1 = parseExp(nextIndex0)
            right_tree, nextIndex2 = parseExp(nextIndex1)
            assert tokens[nextIndex2] == ')', ('somethings wrong:', tokens[nextIndex2])
            return op_class(left_tree, right_tree), nextIndex2+1
        #catch error          
        else:
            raise ValueError('somethings wrong:', t)
            
    (parsedExp, nextIndex) = parseExp(0)
    return parsedExp

# token is a string
# returns True if contains only digits
def numberTok(token):
    for char in token:
        if not char in string.digits: 
            return False
    return True

# token is a string
# returns True its first character is a letter
def variableTok(token):
    for char in token:
        if char in string.ascii_letters: 
            return True
    return False

# thing is any Python entity
# returns True if it is a number
def isNum(thing):
    return type(thing) == int or type(thing) == float

# Run calculator interactively
def calc():
    env = {}
    while True:
        e = input('% ')            # prints %, returns user input
        print('%', parse(tokenize(e)).evaluation(env))# your expression here
        print('   env =', env)

# exprs is a list of strings
# runs calculator on those strings, in sequence, using the same environment
def calcTest(exprs):
    env = {}
    for e in exprs:
        print('%', e)                    # e is the experession 
        print(parse(tokenize(e)).evaluation(env)) # your expression here
        print('   env =', env)

# Simple tokenizer tests
'''Answers are:
['fred']
['777']
['777', 'hi', '33']
['*', '*', '-', ')', '(']
['(', 'hi', '*', 'ho', ')']
['(', 'fred', '+', 'george', ')']
['(', 'hi', '*', 'ho', ')']
['(', 'fred', '+', 'george', ')']
'''
def testTokenize():
    print(tokenize('fred '))
    print(tokenize('777 '))
    print(tokenize('777 hi 33 '))
    print(tokenize('**-)('))
    print(tokenize('( hi * ho )'))
    print(tokenize('(fred + george)'))
    print(tokenize('(hi*ho)'))
    print(tokenize('( fred+george )'))


# Simple parsing tests from the handout
'''Answers are:
Var(a)
Num(888.0)
Sum(Var(fred), Var(george))
Quot(Prod(Var(a), Var(b)), Diff(Var(cee), Var(doh)))
Quot(Prod(Var(a), Var(b)), Diff(Var(cee), Var(doh)))
Assign(Var(a), Prod(Num(3.0), Num(5.0)))
'''
def testParse():
    print(parse(['a']))
    print(parse(['888']))
    print(parse(['(', 'fred', '+', 'george', ')']))
    print(parse(['(', '(', 'a', '*', 'b', ')', '/', '(', 'cee', '-', 'doh', ')' ,')']))
    print(parse(tokenize('((a * b) / (cee - doh))')))
    print(parse(tokenize('(a = (3 * 5))')))

####################################################################
# Test cases for EAGER evaluator
####################################################################

def testEval():
    env = {}
    Assign(Variable('a'), Number(5.0)).evaluation(env)
    print(Variable('a').evaluation(env))
    env['b'] = 2.0
    print(Variable('b').evaluation(env))
    env['c'] = 4.0
    print(Variable('c').evaluation(env))
    print(Sum(Variable('a'), Variable('b')).evaluation(env))
    print(Sum(Diff(Variable('a'), Variable('c')), Variable('b')).evaluation(env))
    Assign(Variable('a'), Sum(Variable('a'), Variable('b'))).evaluation(env)
    print(Variable('a').evaluation(env))
    print(env)

# Basic calculator test cases (see handout)
testExprs = ['(2 + 5)',
             '(z = 6)',
             'z',
             '(w = (z + 1))',
             'w'
             ]
# calcTest(testExprs)

####################################################################
# Test cases for LAZY evaluator
####################################################################

# Simple lazy eval test cases from handout
'''Answers are:
Sum(Var(b), Var(c))
Sum(2.0, Var(c))
6.0
'''
def testLazyEval():
    env = {}
    Assign(Variable('a'), Sum(Variable('b'), Variable('c'))).evaluation(env)
    print(Variable('a').evaluation(env))
    env['b'] = Number(2.0)
    print(Variable('a').evaluation(env))
    env['c'] = Number(4.0)
    print(Variable('a').evaluation(env))
    print(env)

# Lazy partial eval test cases (see handout)
lazyTestExprs = ['(a = (b + c))',
                  '(b = ((d * e) / 2))',
                  'a',
                  '(d = 6)',
                  '(e = 5)',
                  'a',
                  '(c = 9)',
                  'a',
                  '(d = 2)',
                  'a']
# calcTest(lazyTestExprs)

## More test cases (see handout)
partialTestExprs = ['(z = (y + w))',
                    'z',
                    '(y = 2)',
                    'z',
                    '(w = 4)',
                    'z',
                    '(w = 100)',
                    'z']

# calcTest(partialTestExprs)
