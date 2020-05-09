#! /usr/bin/env python3

import collections
from fractions import Fraction as F
import itertools

def confidence_interval(data):
    return min(data), min(data)

def in_range(lo, hi, x):
    return lo <= x and x <= hi

def normalize(dist):
    denom = sum(dist.values())
    return {data: F(v, denom) for data,v in dist.items() if v != 0}

def distribution(theta):
    d = {data:1 for data in itertools.product([theta,theta+1], repeat=2)}
    return normalize(d)

def joint_pmf(dist1, dist2):
    dist = collections.defaultdict(F)
    for d1,d2 in itertools.product(dist1.keys(), dist2.keys()):
        dist[d1,d2] += dist1[d1]*dist2[d2]
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

def in_ci(theta, data):
    d1,d2 = data
    lo,hi = confidence_interval((d1,d2))
    return (lo <= theta and theta <= hi)

def a_in_ci(dist):
    return apply(dist, lambda k: in_ci(*k))

def theta_ci(dist):
    return apply(dist, lambda k: (k[0], confidence_interval(k[1:])))

def theta_given_data(dist):
    data_dists = collections.defaultdict(lambda: collections.defaultdict(F))
    for theta, data in dist:
        data_dists[data][theta] += dist[theta,data]
    return {data:normalize(nd) for data,nd in data_dists.items()}

def in_range_given_ci(dist,lo,hi):
    newdist = collections.defaultdict(F)
    for theta, ci in dist:
        if ci == (lo, hi):
            newdist[in_range(lo,hi,theta)] += dist[theta,ci]
    return normalize(newdist)

for (t1,t2),ip1 in itertools.product(
        itertools.product(range(2), repeat=2),
        range(2,3)):
    print('====',t1,t2,ip1)
    d1 = joint_pmf({t1:1}, distribution(t1))
    d2 = joint_pmf({t2:1}, distribution(t2))

    merge = weighted_merge(d1,d2,F(1,ip1))
    screened = a_in_ci(merge)
    if screened[True] != F(3,4):
        pdist(d1)
        pdist(d2)
        pdist(screened)

    tci = theta_ci(merge)
    datas = sorted(data for theta,data in merge)
    dist = theta_given_data(merge)
    for data in datas:
        print('->',data)
        pdist(dist[data])
