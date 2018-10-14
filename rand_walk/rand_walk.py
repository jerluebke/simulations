# -*- coding: utf-8 -*-

import numpy as np
from numpy.random import randint as rg


def rand_walk(s=100):
    """
    usage:
        >>> plt.plot(rand_walk(steps))
    """
    res = np.zeros(s)
    res[0] = rg(100)
    i = 1
    while i < s:
        step = rg(2)
        res[i] = res[i-1] + 1 if step else res[i-1] - 1
        i+=1
    return res


def rand_walk_2d(s=100, t=100):
    """
    usage:
        >>> plt.imshow(rand_walk_2d(size, steps), cmap='gray_r')
    """
    res = np.zeros((s, s))
    a, b = rg(0, s, 2)
    print("start: (%d, %d)" % (a, b))

    i = 0
    while i < t:
        d = rg(4)
        if d == 0:
            a = s-1 if not a else a-1
        elif d == 1:
            a = 0 if a == s-1 else a+1
        elif d == 2:
            b = s-1 if not b else b-1
        elif d == 3:
            b = 0 if b == s-1 else b+1
        c = res[a][b]
        res[a][b] = c+1 if c != 255 else c
        i += 1

    print("end: (%d, %d)" % (a, b))
    return res
