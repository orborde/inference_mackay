import collections
import random
import itertools

from common import *

def flip_f(p):
    def func():
        if random.uniform(0, 1) < p:
            return H
        return T
    return func

FLIPS = {
    'flip50': flip_f(0.5),
    'flip75': flip_f(0.75)
    }


def flipgame(flip, stoprule):
    flips = []
    stats = collections.defaultdict(int)
    while not stoprule(flips, stats):
        f = flip()
        flips.append(f)
        stats[f] += 1
    return flips

def is_match(flips):
    return flips == TARGET

def match_prob(flip, stoprule, runs):
    runi = xrange(runs)
    matches = 0
    for i in runi:
        flips = flipgame(flip, stoprule)
        if is_match(flips):
            matches += 1
    return float(matches) / runs

RUNS=100000000
options = list(itertools.product(sorted(STOPS), sorted(FLIPS)))
for stoprule, flip in options:
    mp = match_prob(FLIPS[flip], STOPS[stoprule], RUNS)
    print stoprule, flip, mp

