# -*- coding: utf-8 -*-

import numpy as np
from mayavi import mlab
from box import Box


def set_box(nop, bounds, speed, mass):
    state = np.zeros((nop, 7))
    state[:, :3] = np.random.uniform(*bounds[:2], (nop, 3))
    v = np.random.normal(*speed, nop)
    theta = np.random.uniform(0, np.pi, nop)
    phi = np.random.uniform(0, 2*np.pi, nop)
    state[:, 3] = v * np.sin(theta) * np.cos(phi)
    state[:, 4] = v * np.sin(theta) * np.sin(phi)
    state[:, 5] = v * np.cos(theta)
    state[:, 6] = mass
    return Box(state, bounds, 0.10, dim=3)


DT = 1/30
BOUNDS = [-6, 6] * 3
BOX = set_box(1000, BOUNDS, (2, 1), 0.5)

mlab.figure()
points = mlab.points3d(BOX.state[:,0], BOX.state[:,1], BOX.state[:,2],
                       #  BOX.state[:,6],
                       extent=BOUNDS, mode='sphere', scale_factor=0.25,
                       scale_mode='scalar')
ms = points.mlab_source
mlab.outline()

@mlab.animate(delay=10)
def update():
    while 1:
        BOX.step(DT)
        ms.trait_set(x=BOX.state[:,0], y=BOX.state[:,1], z=BOX.state[:,2])
        yield

anim = update()
#  mlab.show()
