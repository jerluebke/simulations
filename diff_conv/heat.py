#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from scipy import ndimage


STENCIL = np.array([
    [0., 1., 0.],
    [1.,-4., 1.],
    [0., 1., 0.]
])

dx  = .5
N   = 128
M   = 128
HEAT = np.zeros((N, M))
ETA = np.full_like(HEAT, 0.02)
ETA[54:74,54:74] = 0.01
DIV = np.zeros_like(HEAT)
U = np.zeros((2, *HEAT.shape))
U[0,:,49:54] = 1.

dt = .2 * dx**2 / (2. * ETA.max())

HEAT[54:74,54:74] = 1.
INTEGRAL = HEAT.sum()


def Lap(a, dx):
    return ndimage.convolve(a, STENCIL, mode='nearest') / dx**2


def Div(a, dx):
    global DIV
    DIV[1:]    = a[0,1:] - a[0,:-1]
    DIV[:,1:] += a[1,:,1:] - a[1,:,:-1]
    DIV[0]   = DIV[1]
    DIV[:,0] = DIV[:,1]
    return DIV / (2. * dx)


def euler_step():
    global HEAT
    for _ in range(10):
        HEAT += dt * Lap(ETA * HEAT, dx)
        HEAT -= dt * Div(U * HEAT, dx)


def step(i):
    euler_step()
    img.set_data(HEAT)
    #  print('err = %f' % np.abs(INTEGRAL - HEAT.sum()))
    return img,


fig = plt.figure()
plt.grid(False)
img = plt.imshow(HEAT, cmap=plt.get_cmap('plasma'), animated=True)
anim = animation.FuncAnimation(fig, step, repeat=False, blit=True)

plt.show()


#  vim: set ff=unix tw=79 sw=4 ts=8 et ic ai :
