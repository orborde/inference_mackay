#! /usr/bin/env python3

import collections
from fractions import Fraction as F
import itertools

def confidence_interval(data):
    return [min(data), min(data)]

def normalize(dist):
    denom = sum(dist.values())
    return {data: F(v, denom) for data,v in dist.items()}

def distribution(theta):
    d = {data:1 for data in itertools.product([theta,theta+1], repeat=2)}
    return normalize(d)

def joint_pmf(dist1, dist2):
    dist = collections.defaultdict(F)
    for d1,d2 in itertools.product(dist1.keys(), dist2.keys()):
        dist[d1+d2] += dist1[d1]*dist2[d2]
    return normalize(dist)

def weighted_merge(dist1, dist2, p1):
    dist = collections.defaultdict(F)
    def add(d,w):
        for k in d:
            dist[k] += d[k]*w

    add(dist1, p1)
    add(dist2, 1-p1)
    return normalize(dist)

def pdist(dist):
    for k in sorted(dist.keys()):
        print(k, dist[k])
    print()

def apply(din, f):
    dist = collections.defaultdict(F)
    for k in din:
        dist[f(k)] += din[k]
    return normalize(dist)

def in_ci(theta, d1, d2):
    lo,hi = confidence_interval((d1,d2))
    return (lo <= theta and theta <= hi)

def a_in_ci(dist):
    return apply(dist, lambda k: in_ci(*k))

for (t1,t2),ip1 in itertools.product(
        itertools.product(range(10), repeat=2),
        range(1,10)):
    d1 = joint_pmf({(t1,):1}, distribution(t1))
    d2 = joint_pmf({(t2,):1}, distribution(t2))

    merge = weighted_merge(d1,d2,F(1,ip1))
    screened = a_in_ci(merge)
    if screened[True] != F(3,4):
        pdist(d1)
        print()
        pdist(d2)
        print()
        pdist(screened)
        print()
