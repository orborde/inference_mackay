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


def condensed_history(history: List[Direction]):
    return [d for d in history if d is not Direction.STAY]

# Is this a circled node?
def end_doubled(history: List[Direction]):
    ch = condensed_history(history)
    if len(ch) < 2:
        return False
    return ch[-1] == ch[-2]
    
def survivors_after(N: int):
    histories = [[]]

    for _ in range(N):
        new_histories = []

        for h in histories:
            new_histories.append(h + [Direction.LEFT])
            new_histories.append(h + [Direction.STAY])
            new_histories.append(h + [Direction.RIGHT])
        
        histories = [h for h in new_histories if not end_doubled(h)]

    return histories

def execute(start: State, path: List[Direction]):
    cur = start
    for step in path:
        cur = shift(cur, step)
    return cur

if __name__ == '__main__':
    paths = survivors_after(15)
    #pprint.pprint(paths)
    fstates = collections.Counter()
    for path in paths:
        for start in STATES:
            fstates[execute(start,path)] += 1
    pprint.pprint(dict(fstates))