import collections
import random
import itertools

H="H"
T="T"

def flip_f(p):
    def func():
        if random.uniform(0, 1) < p:
            return H
        return T
    return func

def stop_len_N_f(N):
    def rule(flips, stats):
        #assert len(flips) <= N
        return (len(flips) == N)
    return rule

def stop_tails_N_f(N):
    def rule(flips, stats):
        count = stats[T]
        #assert count <= N
        if count == N:
            #assert flips[-1] is T
            return True
        return False
    return rule

FLIPS = {
    'flip50': flip_f(0.5),
    'flip75': flip_f(0.75)
    }

LENSTOP=12
TAILSTOP=3
STOPS = {
    'len_%d' % LENSTOP: stop_len_N_f(LENSTOP),
    'tails_%d' % TAILSTOP: stop_tails_N_f(TAILSTOP)
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
    stats = collections.defaultdict(int)
    for f in flips:
        stats[f] += 1
    for rule in STOPS.itervalues():
        if not rule(flips, stats):
            return False
    return True

def match_prob(flip, stoprule, runs):
    runi = xrange(runs)
    matches = 0
    for i in runi:
        flips = flipgame(flip, stoprule)
        if is_match(flips):
            matches += 1
    return float(matches) / runs

RUNS=1000000
options = list(itertools.product(sorted(FLIPS), sorted(STOPS)))
for flip, stoprule in options:
    mp = match_prob(FLIPS[flip], STOPS[stoprule], RUNS)
    print flip, stoprule, mp

