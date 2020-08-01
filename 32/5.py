#!/usr/bin/env python3

"""
How can you use a coin to create a random ranking of 3
people? Construct a solution that uses exact sampling. For example,
you could apply exact sampling to a Markov chain in which the coin is
repeatedly used alternately to decide whether to switch first and second,
then whether to switch second and third.
"""

import collections
import itertools
from typing import *
import random

def coin():
    return random.randint(0,1) == 1

def flips():
    return (coin(), coin())

def apply(state, f01, f12):
    if f01:
        state = state[1], state[0], state[2]
    if f12:
        state = state[0], state[2], state[1]
    return state

def cftp_shuffle(collection: List):
    lookback = 1
    history = collections.defaultdict(flips)

    while True:
        states = list(itertools.permutations(collection))
        for i in range(lookback):
            t = -lookback + i
            f01, f12 = history[t]

            states = [apply(state, f01, f12) for state in states]

        if len(set(states)) == 1:
            return states[0]
        
        lookback += 1

outcomes = collections.Counter()

for i in range(10000):
    