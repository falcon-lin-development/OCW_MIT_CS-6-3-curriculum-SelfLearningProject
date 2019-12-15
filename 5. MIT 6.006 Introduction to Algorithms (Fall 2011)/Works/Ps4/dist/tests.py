import dnaseq
import imp
foo = imp.load_source("dnaseq-sol", "./dnaseq-sol.py")

a = dnaseq.subsequenceHashes
b = foo.subsequenceHashes

seq = "qwertyuiopasdfghjklzxcvbnm"
out1 = [(h, (i, s)) for s, h, i in a(seq, 3)]
out2 = [i for i in b(iter(seq), 3)]

print out1 == out2
print out1
print "------"
print out2
print '------------------------------------'


a = dnaseq.intervalSubsequenceHashes
b = foo.intervalSubsequenceHashes

seq = "qwertyuiopasdfghjklzxcvbnmqwertyuiopasdwertyufghjklcvbnm"
out1 = [(h, (i, s)) for s, h, i in a(seq, 3, 5)]
out2 = [i for i in b(iter(seq), 3, 5)]

print out1 == out2
print out1
print "------"
print out2
print '------------------------------------'





######testing for transbase
# for i in range(10000):
#     n = random.randint(0, 100000)
#     base = 8
#     result = '0' + (''.join([str(i) for i in trans_base(n, base)])).encode('ascii')
#     test = oct(n)
#     if result != test:
#         print(trans_base(n, base))
#         raise Exception("{0}vs{1}".format(result, test))


####################Testing for sieve_algo proc.##############################
# n = 64000
# rand = random.randint(0, len(sieve_algorithm(n))-1)
# a = sieve_algorithm(n)[-rand:]
# for p in a:
#     for test in sieve_algorithm(n)[:-rand]:
#         if p%test == 0:
#             raise Exception("{0} is not a prime. {1} is a factor".format(p, test))


# ###############Rolling_hashes testing###############
# w = Rolling_hashes(256)
# w.append(34)
# w.append(56)
# w.append(65)
# print w()
# print w.prep()
# print '------------------'
# w.append(77)
# print w.base, w.p, w.magic, w.ibase
# w.skip(34)
# print w.base, w.p, w.magic, w.ibase
# print w()
# print w.prep()
# print '------------------'
# print trans_deci([56,65,77], w.base) % w.p
# print w()

#########test for subsequenceHashes########
# test = subsequenceHashes("Hi I am Falcon", 2)
# for i in test:
#     print i

# finding random large prime
# find a list of primes < 64000
# def sieve_algorithm(n=64000):
#     """implementation of sieve_algorithm"""
#     if os.path.exists("./primeList{0}.txt".format(n)):
#         with open("./primeList{0}.txt".format(n), 'r') as f:
#             return [int(p) for p in f.read().split('\n')]
#     else:
#         # potential improvement by taking the advantage of saved file.
#         out = [i for i in range(2, n + 1)]
#         out_ref = out[:]
#         for i in range(n):
#             for item in out:
#                 if item % out[i] == 0 and item != out[i]:
#                     out_ref.remove(item)
#             else:
#                 out = out_ref[:]
#                 if i + 1 > len(out) - 1:
#                     break
#         f = open("./primeList{0}.txt".format(n), 'w')
#         f.write('\n'.join([str(p) for p in out]))
#         return out
#
#
# # mod_inv
# def egcd(a, b):
#     if a == 0:
#         return [b, 0, 1]
#     else:
#         g, y, x = egcd(b % a, a)
#         return g, x - (b // a) * y, y
#
#
# def modinv(a, m):
#     g, x, y = egcd(a, m)
#     if g != 1:
#         raise Exception("modular inverse does not exit")
#     else:
#         return x % m
#
#
# # calc_max_indice:
# def trans_base(n, base):
#     """Given a decimal number, return a required base expression(list)"""
#     n = n
#     out = []
#     while n != 0:
#         out.insert(0, n % base)
#         n = n // base
#     return out
#
#
# def trans_deci(l, base):
#     """given a based expression(list of int), return the decimal expression"""
#     out = 0
#     use = l[:]
#     use.reverse()
#     for i, a in enumerate(use):
#         out += a * base ** i
#     return out
#
#
# # Rolling hashes
# class Rolling_hashes(object):
#     def __init__(self, base=256, p=None):
#         self.base = base
#         if bool(p): self.p = p
#         if not bool(p): self.p = self._gen_prime()
#         self.hash = 0
#         self.magic = 1
#         self.ibase = modinv(self.base, self.p)
#
#     def seq_append(self, new_seq):
#         for char in new_seq:
#             self.append(char)
#
#     def append(self, new):  # new should be processed into integer before calling this function
#         self.hash = ((self.hash * self.base) + new) % self.p
#         self.magic = (self.magic * self.base) % self.p
#
#     def skip(self, old):
#         self.magic = (self.magic * self.ibase) % self.p
#         self.hash = (self.hash - old * self.magic + self.base * self.p) % self.p
#
#     def __call__(self, *args, **kwargs):
#         return self.hash
#
#     def prep(self):  # pretty representation
#         return trans_base(self.hash, self.base)
#
#     def _gen_prime(self):
#         trial = random.randint(2000000000, 4000000000)
#         primes = sieve_algorithm()
#         for p in primes:
#             if trial % p == 0:
#                 break
#         else:
#             return trial
#         return self._gen_prime()


