#!/usr/bin/env python3

import itertools
import random
from typing import *

N = 100
state = list(range(N))

def coalesced(state: List[int]) -> bool:
    return len(set(state)) == 1

turn=0
lastcount = None
while not coalesced(state):
    if len(set(state)) != lastcount:
        print(turn, len(set(state)))

    random.shuffle(state)

    newstate=[]
    for x,y in zip(state[::2], state[1::2]):
        # Since we shuffled, we don't additionally need to randomly pick
        # a name-giving parent.
        newstate.append(x)
        newstate.append(x)

    assert len(newstate) == N
    lastcount = len(set(state))
    state = newstate
    turn += 1
