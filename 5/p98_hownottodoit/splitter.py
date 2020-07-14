#! /usr/bin/env python3

ENSEMBLE={
    'a': .5,
    'b': .25,
    'c': .25,
}

def p(items, ensemble):
    return sum(ensemble[i] for i in items)

def split(items):
    possibilities = ((abs(z - (1 - z)), subspace) for z,subspace in
                     ((p(subspace, items), subspace) for subspace in powerset(items)))
    _, best = min(possibilities)
    return best

def split_path(item, ensemble):
    if len(ensemble) == 1:
        assert item in ensemble
        return ensemble

    bsplit = split(ensemble)
    if item in bsplit:
        new_ensemble = {x: ensemble[x] for x in bsplit}
    else:
        new_ensemble = {item
        return bsplit + split_path(item, new_ensemble)


def test_split():
    for item in ensemble:
        # Count how many split-by-probability measures it takes to get down to one possibility.
        pass

if __name__=='__main__':
    import doctest
    fails, _ = doctest.testmod()
    assert fails==0
