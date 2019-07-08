#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from scipy import ndimage


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#####################
#   DOMAIN SETUP    #
#####################

# spatial step width
dx = .5

# domain size
N = 128
M = 128

# heat array
HEAT = np.zeros((N, M))

# diffusivity array
ETA = np.full_like(HEAT, 0.02)
ETA[54:74,54:74] = 0.01

# compute time step according to CFL condition:
#   dt < dx^2 / (2 * eta)
dt = .2 * dx**2 / (2. * ETA.max())

# flow array (2-dim)
U = np.zeros((2, *HEAT.shape))
U[0,:,49:54] = 1.

# set initial values
HEAT[54:74,54:74] = 1.
# compute initial total heat
INTEGRAL = HEAT.sum()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#############################
#   DIFFERENCE OPERATORS    #
#############################

# LAPLACIAN

STENCIL = np.array([
    [0., 1., 0.],
    [1.,-4., 1.],
    [0., 1., 0.]
])

def Lap(a, dx):
    # convolve array with stencil
    # impose von-Neumann boundary conditions (a[0] = a[1])
    return ndimage.convolve(a, STENCIL, mode='nearest') / dx**2


# DIVERGENCE

# array in which to write result
DIV = np.zeros_like(HEAT)

def Div(a, dx):
    global DIV
    # compute divergence of 2-dim vector field
    # compute central difference
    DIV[1:]    = a[0,1:] - a[0,:-1]
    DIV[:,1:] += a[1,:,1:] - a[1,:,:-1]
    # impose von-Neumann boundary conditions
    DIV[0]   = DIV[1]
    DIV[:,0] = DIV[:,1]
    return DIV / (2. * dx)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#####################
#   INTEGRATOR      #
#####################

def euler_step():
    global HEAT
    # simple euler scheme
    # compute some steps before plotting
    for _ in range(10):
        # diffusion
        HEAT += dt * Lap(ETA * HEAT, dx)
        # convection
        #  HEAT -= dt * Div(U * HEAT, dx)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#####################
#   VISUALIZATION   #
#####################

def step(i):
    euler_step()
    img.set_data(HEAT)
    #  print('err = %f' % np.abs(INTEGRAL - HEAT.sum()))
    return img,


fig  = plt.figure()
plt.grid(False)
img  = plt.imshow(HEAT, cmap=plt.get_cmap('plasma'), animated=True)
anim = animation.FuncAnimation(fig, step, repeat=False, blit=True)

plt.show()


#  vim: set ff=unix tw=79 sw=4 ts=8 et ic ai :
