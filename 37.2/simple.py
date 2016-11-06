import random
import itertools
from tqdm import tqdm

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
        assert len(flips) <= N
        return (len(flips) == N)
    return rule

def stop_tails_N_f(N):
    def rule(flips):
        count = flips.count(T)
        assert count <= N
        if count == N:
            assert flips[-1] is T
            return True
        return False
    return rule


FLIPS = {
    'flip50': flip_f(0.5),
    'flip90': flip_f(0.9)
    }

STOPS = {
    'stop_len_2': stop_len_N_f(2),
    'stop_tails_2': stop_tails_N_f(1)
}


def flipgame(flip, stoprule):
    flips = []
    while not stoprule(flips):
        flips.append(flip())
    return flips


def is_match(flips):
    return ((flips[-1] is T) and
            (flips.count(T) == 1)
            and (len(flips) == 2))

def match_prob(flip, stoprule, runs, status=None):
    runi = xrange(runs)
    if status is None:
        status = tqdm(runi)
    matches = 0
    for i in runi:
        flips = flipgame(flip, stoprule)
        if is_match(flips):
            matches += 1
        status.update(1)
    return float(matches) / runs

RUNS=1000000
options = list(itertools.product(FLIPS, STOPS))
status = tqdm(total = len(options) * RUNS)
for flip, stoprule in options:
    mp = match_prob(FLIPS[flip], STOPS[stoprule], RUNS, status)
    print flip, stoprule, mp

