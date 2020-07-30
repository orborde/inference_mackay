#!/usr/bin/env python3

import collections
from enum import Enum
import itertools
from fractions import Fraction as F
from typing import *
import pprint


class Direction(Enum):
    LEFT = "LEFT"
    STAY = "STAY"
    RIGHT = "RIGHT"
DIRECTIONS = list(Direction)

State = NewType("State", int)
STATES = [State(i) for i in [1,2,3]]

def shift(state: State, direction: Direction):
    if direction == Direction.LEFT:
        newstate = state-1
    elif direction == Direction.STAY:
        newstate = state
    elif direction == Direction.RIGHT:
        newstate = state+1

    if newstate in STATES:
        return newstate
    else:
        return state

NO_COALESCENCE = "NO_COALESCENCE"

# Simulate all possible exact sampling outcomes involving up
# to N steps in the past. Return the PMF of the resulting sample.
def sample_distribution(N: int):
    histories = itertools.product(DIRECTIONS, repeat=N)
    p_single = F(1, len(DIRECTIONS)**N)

    final_distribution = collections.defaultdict(F)
    for history in histories:
        time_function = {
            -(i+1):h for (i, h) in enumerate(history)
            }
        outcome = monte_carlo_exact(time_function)
        final_distribution[outcome] += p_single

    assert sum(final_distribution.values()) == 1
    return dict(final_distribution)


def monte_carlo_exact(time_function: Dict[int, Direction]):
    for lookback in range(1, len(time_function)+1):
        meta_state = STATES
        for t in range(-lookback, 0):
            direction = time_function[t]
            meta_state = [shift(state, direction) for state in meta_state]
        
        coalesced = (len(set(meta_state)) == 1)
        if coalesced:
            return meta_state[0]

    return NO_COALESCENCE


if __name__ == '__main__':
    last = None
    for lookback in range(1, 15+1):
        distribution = sample_distribution(lookback)
        pprint.pprint((lookback, distribution))
        if last is not None:
            pprint.pprint({state: float(distribution.get(state, 0)-last.get(state, 0))
            for state in STATES})
        last=distribution
