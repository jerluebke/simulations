# -*- coding: utf-8 -*-

import numpy as np
from scipy.spatial.distance import pdist, squareform


class Box:
    def __init__(self, state, bounds, radius, dim=2):
        """
        state is a n x (2*dim+1)-array (n: number of particles):
            [x, y, [z], vx, vy, [vz], mass]

        bounds: [xmin, xmax, ymin, ymax, [zmin, zmax]]
        """
        self.state = state
        self.bounds = bounds
        self.r = radius
        self.d = dim

    def step(self, dt):
        self.state[:, :self.d] += dt * self.state[:, self.d:2*self.d]
        #  self.state[:, :2] += dt * self.state[:, 2:4]
        self.find_collisions()
        self.bound_check()

    def find_collisions(self):
        # pairwise distances d[i, j]
        d = squareform(pdist(self.state[:, :self.d]))
        #  d = squareform(pdist(self.state[:, :2]))
        # relevant indicies
        ind1, ind2 = np.where(d < 2*self.r)
        unique = (ind1 < ind2)
        ind1 = ind1[unique]
        ind2 = ind2[unique]
        for j, k in zip(ind1, ind2):
            self.state[:, self.d:2*self.d][j], self.state[:, self.d:2*self.d][k] = \
                self.collision(self.state[j], self.state[k])
            #  self.state[:, 2:4][j], self.state[:, 2:4][k] = \

    def collision(self, p, q):
        x1 = p[:self.d]
        x2 = q[:self.d]
        v1 = p[self.d:2*self.d]
        v2 = q[self.d:2*self.d]
        m1 = p[2*self.d]
        m2 = q[2*self.d]
        #  x1 = p[:2]
        #  x2 = q[:2]
        #  v1 = p[2:4]
        #  v2 = q[2:4]
        #  m1 = p[4]
        #  m2 = q[4]

        x_rel = x1 - x2
        v_rel = v1 - v2
        xx_rel = np.dot(x_rel, x_rel)
        vx_rel = np.dot(v_rel, x_rel)
        # new relative velocity (collision of spheres)
        v_rel = 2 * x_rel * vx_rel / xx_rel - v_rel
        # center of mass momentum
        v_cm = (m1 * v1 + m2 * v2) / (m1 + m2)

        v1_new = v_cm + v_rel * m2 / (m1 + m2)
        v2_new = v_cm - v_rel * m1 / (m1 + m2)
        return v1_new, v2_new

    def bound_check(self):
        # create mask for values out of bounds
        x1 = (self.state[:, 0] < self.bounds[0] + self.r)
        x2 = (self.state[:, 0] > self.bounds[1] - self.r)
        y1 = (self.state[:, 1] < self.bounds[2] + self.r)
        y2 = (self.state[:, 1] > self.bounds[3] - self.r)

        # correct positions
        self.state[x1, 0] = self.bounds[0] + self.r
        self.state[x2, 0] = self.bounds[1] - self.r
        self.state[y1, 1] = self.bounds[2] + self.r
        self.state[y2, 1] = self.bounds[3] - self.r

        # revert velocities
        self.state[x1 | x2, self.d] *= -1
        self.state[y1 | y2, self.d+1] *= -1

        if self.d == 3:
            z1 = (self.state[:, 2] < self.bounds[4] + self.r)
            z2 = (self.state[:, 2] > self.bounds[5] - self.r)
            self.state[z1, 2] = self.bounds[4] + self.r
            self.state[z2, 2] = self.bounds[5] - self.r
            self.state[z1 | z2, self.d+2] *= -1
