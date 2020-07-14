# THIS IS BROKEN!
#
# Exhaustively search progressively longer flip sequence lengths and
# compute the probability of getting something matching the target
# sequence. Unfortunately, some of the stopping conditions could
# theoretically run forever; hence the breadth-first search.

import collections
import doctest
import itertools
import time

from common import *

P_HEADS = [0.5, 0.75]

def probability(seq, p_heads):
    """
    >>> probability([H,T,H], 0.5)
    0.125
    >>> probability([H,H], 0.5)
    0.25
    """
    p = 1
    for flip in seq:
        if flip is H: p *= p_heads
        if flip is T: p *= (1 - p_heads)
    return p

def stop_len12(flips):
    return len(flips) == 1
def stop_3tails(flips):
    return flips[-1] == T and flips.count(T) == 3

STOPS = [stop_len12, stop_3tails]

fails, _ = doctest.testmod()
assert fails == 0

mass = collections.defaultdict(int)
depth = 0
while True:
    depth += 1
    start = time.time()
    total_checked = 0
    print 'Starting depth', depth

    for seq in itertools.product([H,T], repeat=depth):
        total_checked += 1

        for p in P_HEADS:
            p_seq = probability(seq, p)

            for stop_f in STOPS:
                possible = stop_f
                if not possible(seq):
                    continue

                key = (stop_f.__name__, p)
                mass[key] += p_seq

    print '  ', total_checked, 'sequences checked'
    print
    for key in itertools.product([s.__name__ for s in STOPS], P_HEADS):
        print '  ', key, mass[key]
    print

    if depth == 12: break
