# -*- coding: utf-8 -*-

import numpy as np
from numpy.random import randint as rg

def rand_walk_mpl(s=100):
    """
    usage:
        >>> from mpl_toolkits.mplot3d import Axes3D
        >>> fig = plt.figure()
        >>> ax = fig.add_subplot(111, projection='3d')
        >>> ax.plot(*rand_walk_mpl(steps))
    """
    steps = []
    cur = [0, 0, 0]
    i = 0
    while i < s:
        cur[rg(3)] += [-1, 1][rg(2)]
        steps.append(cur[:])
        i += 1
    return zip(*steps)


def rand_walk_mv(s=100, t=10000):
    """
    usage:
        >>> from mayavi import mlab
        >>> rw = mlab.pipeline.volume(mlab.pipeline.scatter_field(\
        ...     rand_walk_mv(size, steps)))
        >>> mlab.outline(rw)
    """
    res = np.zeros((s, s, s))
    c = rg(0, s, 3)
    res[tuple(c)] = 1
    i = 1
    while i < t:
        c += rg(-1, 2, 3)
        c[c==s] = 0
        c[c==-1] = s-1
        #  ct = tuple(c)
        #  cv = res[ct]
        #  res[ct] = cv if cv==255 else cv+1
        res[tuple(c)] += 1
        i += 1
    return res
