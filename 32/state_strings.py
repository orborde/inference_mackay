#!/usr/bin/env python3

from enum import Enum
import itertools

L="L"
S="S"
R="R"
SHIFTS=[L,S,R]

def condensed_history(s):
    return ''.join(c for c in s if c != S)

def has_a_double(s):
    cs = condensed_history(s)
    return ((L+L) in cs) or ((R+R) in cs)

N=8
histories = map(lambda t: ''.join(t), itertools.product(SHIFTS, repeat=N))

survivor_histories = filter(lambda s: not has_a_double(s), histories)

for h in survivor_histories:
    print(''.join(h), condensed_history(h))