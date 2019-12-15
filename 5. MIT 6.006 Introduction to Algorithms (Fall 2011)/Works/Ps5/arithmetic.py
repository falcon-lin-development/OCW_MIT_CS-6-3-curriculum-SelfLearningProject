from random import randint
import random
# base = random.choice([2,8,10,16])
base = 256

def PowMod(B,E,M,n, verbose = False):
    R = [0 for i in range(n)] # result
    R[0] = 1
    X = B[:]
    # for i in range(eval(E)):
    #     R = MOD(MUL(R, X, n) , M, 2*n)
    # return R
    for i in range(n):
        # mask = 1
        if verbose: print transform(E[i], 2)
        for bit in transform(E[i],2):
            if verbose: print "-------------------"
            if verbose: print "result:", R, eval(R)
            if bit:
                R = MOD(MUL(R,X,n), M, 2*n)
                if verbose: print "Computed result: ", R, eval(R)
            if verbose: print "multiplier:", X, eval(X)
            if verbose: print "time: ", MUL(X, X, n), eval(MUL(X, X, n))
            X = MOD(MUL(X, X, n), M, 2*n)
            if verbose: print "newX: ", X, eval(X)
            if verbose: print "--------------------"
            # mask = (Word(mask)*Word(2)).LSB()
            # print "mask: {0}".format(mask)
    # print "final result:", R, eval(R)
    return R


def MUL(A, B, n):
    C = [0 for i in range(2*n)]
    while len(A) < n:
        A.append(0)
    while len(B) < n:
        B.append(0)

    for i in range(n):
        carry = 0
        for j in range(n):
            digit = Word(A[i]) * Word(B[j]) + Word(C[i+j]) + Word(carry)
            C[i+j] = digit.LSB()
            carry = digit.MSB()
        C[i + n] = carry
    return C


def DIVMOD(A, B, n):
    if eval(B) == 0:
        raise ZeroDivisionError
    Q = [0 for i in range(n)]
    while len(A) < n:
        A.append(0)
    while len(B) < n:
        B.append(0)
    R = A[:]
    globals()["S0"] = B[:]
    i = 0
    while True:
        i += 1
        old_s = globals()["S{0}".format(i-1)]
        new_s = ADD(old_s, old_s, n)
        globals()["S{0}".format(i)] = new_s
        if CMP(globals()["S{0}".format(i)], A, n) == 'GREATER':
            break
        try:
            if globals()["S{0}".format(i)][n] > 0:
                break
        except IndexError:
            continue
    for j in range(i-1, -1, -1):
        Q = ADD(Q, Q, n)
        if CMP(R, globals()["S{0}".format(j)], n) != "SMALLER":
            R = SUBTRACT(R, globals()["S{0}".format(j)], n)
            Q[0] += 1
    return Q, R


def SUBTRACT(A, B, n):
    assert CMP(A, B, n) != "SMALLER", '{0}:{1}'.format(A, B)
    C = A[:]
    carry = 0
    for i in range(n):
        digit = Word(A[i]) - Word(B[i]) + Word(carry)
        C[i] = digit.LSB()
        carry = digit.MSB()
    # C[n] = carry
    return C


def CMP(A, B, n):
    A = eval(A)
    B = eval(B)
    if A > B:
        return "GREATER"
    elif A < B:
        return "SMALLER"
    else:
        return "EQUAL"


def MOD(A, B, n):
    return DIVMOD(A, B, n)[1]

def DIV(A, B, n):
    return DIVMOD(A, B, n)[0]

def ADD(A, B, n):
    C = [0 for i in range(n+1)]
    carry = 0
    for i in range(n):
        digit = Word(A[i]) + Word(B[i]) + Word(carry)
        C[i] = digit.LSB()
        carry = digit.MSB()
    C[n] = carry
    return C


class Word(object):
    def __init__(self, lsb, msb=0):
        # self.words = [0, v]
        self.msb = msb
        self.lsb = lsb

    def __add__(self, other):
        lsb = self.lsb + other.lsb
        msb, lsb = divmod(lsb, base)
        msb += self.msb + other.msb
        if msb >= base:
            raise Exception, "Summation overflow"
        return self.__class__(lsb, msb)

    def __sub__(self, other):
        # do not support negative number
        lsb = self.lsb - other.lsb
        msb = self.msb - other.msb
        while lsb < 0:
            lsb += base
            msb -= 1
        return self.__class__(lsb, msb)

    def __mul__(self, other):
        # do not support 2 digits multiplication
        assert self.msb == other.msb == 0, "{0}:{1}".format(self.msb, other.msb)
        lsb = self.lsb * other.lsb
        msb = 0
        while lsb >= base:
            msb += 1
            lsb -= base
        return Word(lsb, msb)

    def LSB(self):
        return self.lsb

    def MSB(self):
        return self.msb

    def __str__(self):
        return "{0},{1}".format(self.LSB(), self.MSB())


def eval(num, base=base):
    out = 0
    for i, n in enumerate(num):
        out += n*base**i
    return out

def transform(num, base=base):
    out = []
    if base == 2:
        for i in bin(num)[2:]:
            out.insert(0, int(i))
    elif base == 8:
        for i in oct(num)[1:]:
            out.insert(0, int(i))
    elif base == 10:
        for i in str(num):
            out.insert(0, int(i))
    elif base == 16:
        for i in hex(num)[2:]:
            out.insert(0, int(i))
    else:
        raise Exception
    while len(out)<8:
        out.append(0)
    return out

# n = randint(1, 5)
n = 3
a = [randint(0, base - 1) for i in range(n)]
b = [randint(0, base - 1) for i in range(n)]
m = [randint(0, base - 1) for i in range(n)]
while eval(a) == 0 or eval(b) == 0:
    a = [randint(0, base - 1) for i in range(n)]
    b = [randint(0, base - 1) for i in range(n)]
    m = [randint(0, base - 1) for i in range(n)]

if CMP(a, b, n) == "GREATER":
    a, b = b, a

# n = 2
# a = [1,5]
# b = [2,9]
# m = [4,9]





