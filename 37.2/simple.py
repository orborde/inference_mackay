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
    def rule(flips):
        #assert len(flips) <= N
        return (len(flips) == N)
    return rule

def stop_tails_N_f(N):
    def rule(flips):
        count = flips.count(T)
        #assert count <= N
        if count == N:
            #assert flips[-1] is T
            return True
        return False
    return rule

def stop_one_more_heads(flips):
    heads = flips.count(H)
    tails = flips.count(T)
    if heads == tails + 1:
        return True
    return False

FLIPS = {
    'flip50': flip_f(0.5),
    'flip75': flip_f(0.75)
    }

LENSTOP=12
TAILSTOP=3
STOPS = {
    'len_%d' % LENSTOP: stop_len_N_f(LENSTOP),
    #'tails_%d' % TAILSTOP: stop_tails_N_f(TAILSTOP)
    'one_more_head': stop_one_more_heads,
}


def flipgame(flip, stoprule):
    flips = []
    while not stoprule(flips):
        flips.append(flip())
    return flips


def is_match(flips):
    for rule in STOPS.itervalues():
        if not rule(flips):
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

print 'Let us try!'
for i in xrange(10000):
    print flipgame(FLIPS['flip50'], stop_one_more_heads)

print 'Done with that'
import sys
sys.exit(0)


options = list(itertools.product(sorted(FLIPS), sorted(STOPS)))
for flip, stoprule in options:
    mp = match_prob(FLIPS[flip], STOPS[stoprule], RUNS)
    print flip, stoprule, mp

