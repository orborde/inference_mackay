#! /usr/bin/env python3

import fractions

F=fractions.Fraction

def combo(weights, items):
    norm = sum(weights)
    return sum(w*i/norm for w,i in zip(weights, items))

def pwin(s):
    if s == 'yy':
        return 1

    if s == 'jj':
        return 0

    if s == 'jy':
        return combo([F(1,6), F(5,36)], [pwin('yy'), pwin('jj')])

    if s == 'y':
        return combo([F(1,6), F(5,36)], [pwin('yy'), pwin('jy')])

    if s == 'j':
        return combo([F(1,6), F(5,36)], [pwin('jy'), pwin('jj')])

    if s == 'start':
        return combo([F(1,6), F(10,36)], [pwin('y'), pwin('j')])

    assert False, 'unknown {}'.format(s)

print(pwin('start'))
