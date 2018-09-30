# -*- coding: utf-8 -*-

import numpy as np
from box import Box


def square_one_kind(nop=100, speed=(8, 0.1), bounds=[-4, 4, -4, 4]):
    """
    nop (int): number of particles
    """
    state = np.zeros((nop, 5))
    state[:, :2] = np.random.uniform(*bounds[:2], (nop, 2))
    phi = np.random.uniform(0, 2*np.pi, nop)
    r = np.random.normal(*speed, nop)
    state[:, 2] = r * np.cos(phi)
    state[:, 3] = r * np.sin(phi)
    state[:, 4] = 0.05
    return Box(state, bounds, 0.04)

def rectangle_one_kind_divided(nop=100, speed1=(10, 5),
                               speed2=(1, .5), m1=0.02,
                               m2=0.4, bounds=[-8, 8, -4, 4]):
    state = np.zeros((2*nop, 5))
    state[:nop, 0] = np.random.uniform(bounds[0], 0, nop)
    state[:nop, 1] = np.random.uniform(*bounds[2:], nop)
    state[nop:, 0] = np.random.uniform(0, bounds[1], nop)
    state[nop:, 1] = np.random.uniform(*bounds[2:], nop)
    phi = np.random.uniform(0, 2*np.pi, nop)
    r1 = np.random.normal(*speed1, nop)
    r2 = np.random.normal(*speed2, nop)
    state[:nop, 2] = r1 * np.cos(phi)
    state[nop:, 2] = r2 * np.cos(phi)
    state[:nop, 3] = r1 * np.sin(phi)
    state[nop:, 3] = r2 * np.sin(phi)
    state[:nop, 4] = m1
    state[nop:, 4] = m2
    return Box(state, bounds, 0.04)

def foreign_particles(nop=100, speed=(1, 0.1), nofp=3, fpm=2,
                      bounds=[-4, 4, -4, 4]):
    """
    nofp (int): number of forgein particles (initial velocity = 0)
    fpm (int): forgein particle mass
    """
    state = np.zeros((nop+nofp, 5))
    state[:, :2] = np.random.uniform(*bounds[:2], (nop+nofp, 2))
    phi = np.random.uniform(0, 2*np.pi, nop)
    r = np.random.normal(*speed, nop)
    state[nofp:, 2] = r * np.cos(phi)
    state[nofp:, 3] = r * np.sin(phi)
    state[nofp:, 4] = 0.05
    state[:nofp, 4] = fpm
    return Box(state, bounds, 0.1)
