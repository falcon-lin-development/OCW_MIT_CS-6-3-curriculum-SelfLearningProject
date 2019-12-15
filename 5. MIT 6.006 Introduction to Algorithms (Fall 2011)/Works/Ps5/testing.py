from arithmetic import *
import unittest


_b = base
print "n: {0}".format(n)
print "_b: {0}".format(base)
print "a: {0}".format(a), eval(a)
print "b: {0}".format(b), eval(b)
print "m: {0}".format(m), eval(m)
print "eval(E)/a: {0}".format(eval(a))


class Arithmetic_tests(unittest.TestCase):
    def test_add(self):
        t = eval(ADD(b, a, n))
        answer = eval(b) + eval(a)
        self.assertTrue(t == answer, "{0} + {1} = {2}|{3}".format(eval(b), eval(a), t, answer))

    def test_sub(self):
        t = eval(SUBTRACT(b,a,n))
        answer = eval(b) - eval(a)
        self.assertTrue(t == answer, "{0} - {1} = {2}|{3}".format(eval(b), eval(a), t, answer))

    def test_div(self):
        t = eval(DIV(b,a,n))
        answer = eval(b) // eval(a)
        self.assertTrue(t == answer, "{0} // {1} = {2}|{3}".format(eval(b),eval(a), t, answer))

    def test_mod(self):
        t = eval(MOD(b,a,n))
        answer = eval(b) % eval(a)
        self.assertTrue(t == answer, "{0} % {1} = {2}|{3}".format(eval(b), eval(a), t, answer))

    def test_Mul(self):
        t = eval(MUL(b,a,n))
        answer = eval(b) * eval(a)
        self.assertTrue(t == answer, "{0} * {1} = {2}|{3}".format(eval(b), eval(a), t, answer))

    def test_pow_mod(self):
        t = eval(PowMod(b, a, m, n))
        answer = eval(b) ** eval(a) % eval(m)
        self.assertTrue(t == answer, "{0}^{1} %{4} = {2}|{3}".format(eval(b), eval(a), t, answer, eval(m)))

if __name__ ==  "__main__":
    unittest.main()