#! /usr/bin/env python3

ENSEMBLE={
    'a': .5,
    'b': .25,
    'c': .25,
}


# powerset(ENSEMBLE.keys()) -> ENSEMBLE.keys() -> outcome
# "measure" -> ENSEMBLE.keys() -> outcome
MEASURES=dict()

for measure in powerset(ENSEMBLE.keys()):
    outcomes = dict()
    for item in ENSEMBLE:
        outcomes[item] = (item in measure)
