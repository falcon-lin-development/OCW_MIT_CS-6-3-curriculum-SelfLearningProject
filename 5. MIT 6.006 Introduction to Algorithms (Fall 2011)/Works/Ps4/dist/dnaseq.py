#!/usr/bin/env python2.7

import unittest
from dnaseqlib import *
import random
import os


### Utility classes ###

# Maps integer keys to a set of arbitrary values.
class Multidict:
    # Initializes a new multi-value dictionary, and adds any key-value
    # 2-tuples in the iterable sequence pairs to the data structure.
    def __init__(self, pairs=[]):
        # This may crash with unexpected pairs input.
        # expecting a list of tuple in pairs
        self.d = dict(pairs)

    # Associates the value v with the key k.
    def put(self, k, v):
        if self.d.has_key(k):
            self.d[k].append(v)
        else:
            self.d[k] = [v,]

    # Gets any values that have been associated with the key k; or, if
    # none have been, returns an empty sequence.
    def get(self, k):
        if self.d.has_key(k):
            return self.d[k]
        else:
            return []


# Given a sequence of nucleotides, return all k-length subsequences
# and their hashes.  (What else do you need to know about each
# subsequence?)
def subsequenceHashes(seq, k):
    """Stupid non-general  implementation"""
    s = seq[:k]
    w = RollingHash(s)
    yield s, w.curhash, 0
    for i in range(k, len(seq), 1):
        next_c = seq[i]
        s += next_c
        prev_c = seq[i-k]
        s = s[1:]
        w.slide(prev_c, next_c)
        yield s, w.curhash, i-k+1 # sub_seq, hash, dropped position+1=current pos


# Similar to subsequenceHashes(), but returns one k-length subsequence
# every m nucleotides.  (This will be useful when you try to use two
# whole data files.)
def intervalSubsequenceHashes(seq, k, m):
    subseqs_num = len(seq)//m + 1
    for i in range(subseqs_num):
        start = 0+i*m
        end = start+k
        s = seq[start:end]
        w = RollingHash(s)
        yield s, w.curhash, start


# Searches for commonalities between sequences a and b by comparing
# subsequences of length k.  The sequences a and b should be iterators
# that return nucleotides.  The table is built by computing one hash
# every m nucleotides (for m >= k).
def getExactSubmatches(a, b, k, m):
    a = ''.join([c for c in a])
    a_dict = Multidict()
    for subseq1, h1, i1 in intervalSubsequenceHashes(a, k, m):
        a_dict.put(h1, (subseq1, i1))
    print "Length of hash table: {0}".format(len(a_dict.d))

    b = ''.join([c for c in b])
    for subseq2, h2, i2 in subsequenceHashes(b, k):
        for seq, i1 in a_dict.get(h2):
            if subseq2 != seq:
                continue
            yield i1, i2
    return

def slow_getExactSubmatches(a, b, k, m):
    a = ''.join([c for c in a])
    a_dict = Multidict()
    for subseq1, h1, i1 in subsequenceHashes(a, k):
        a_dict.put(h1, (subseq1, i1))
    print "Length of hash table: {0}".format(len(a_dict.d))

    b = ''.join([c for c in b])
    for subseq2, h2, i2 in subsequenceHashes(b, k):
        for seq, i1 in a_dict.get(h2):
            if subseq2 != seq:
                continue
            yield i1, i2
    return


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'Usage: {0} [file_a.fa] [file_b.fa] [True=>fast_algo]'.format(sys.argv[0])
        sys.exit(1)

    # The arguments are, in order: 1) Your getExactSubmatches
    # function, 2) the filename to which the image should be written,
    # 3) a tuple giving the width and height of the image, 4) the
    # filename of sequence A, 5) the filename of sequence B, 6) k, the
    # subsequence size, and 7) m, the sampling interval for sequence
    # A.
    name = sys.argv[1][5:-3] + "_vs_" + sys.argv[2][5:-3] + ".png"
    if sys.argv[3] == "True":
        compareSequences(getExactSubmatches, "fast_"+name, (500, 500), sys.argv[1], sys.argv[2], 8, 100)
    else:
        compareSequences(slow_getExactSubmatches, "slow_"+name, (500, 500), sys.argv[1], sys.argv[2], 8, 100)
