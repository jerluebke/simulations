# -*- coding: utf-8 -*-

import numpy as np
import scipy.constants as sc
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from set_box import square_one_kind


def maxwell_boltzmann(v_sq, m):
    v_mean_sq = v_sq.sum(axis=0) / len(v_sq)
    T = v_mean_sq * m / (3 * sc.k)
    p = (2 / np.pi)**(1/2) * (m / (sc.k * T))**(3/2) * v_sq \
           * np.exp(-m * v_sq / (2 * sc.k * T))
    return p / p.sum()


DT = 1/30
BOX = square_one_kind(300, speed=(10, .1))
NOP = int(len(BOX.state)/8)

fig = plt.figure()
ax = fig.add_subplot(121, aspect='equal', autoscale_on=False,
                     xlim=(BOX.bounds[0]-.4, BOX.bounds[1]+.4),
                     ylim=(BOX.bounds[2]-.4, BOX.bounds[3]+.4),
                     xticks=[], yticks=[],
                     xticklabels=[], yticklabels=[])
ax_dist = fig.add_subplot(122, aspect='equal', autoscale_on=False,)

PART_1, = ax.plot([], [], 'bo', ms=6)

v_sq = (BOX.state[:, 2:4]**2).sum(axis=1)
v_sq.sort()

patches = ax_dist.hist(v_sq, bins=NOP, density=True, color='b', zorder=1)[-1]
mb_dist, = ax_dist.plot([], [], 'r-', zorder=2)

RECT = plt.Rectangle(BOX.bounds[::2],
                     BOX.bounds[1] - BOX.bounds[0],
                     BOX.bounds[3] - BOX.bounds[2],
                     ec='none', lw=2, fc='none')
ax.add_patch(RECT)


def init():
    PART_1.set_data([], [])
    RECT.set_edgecolor('none')
    mb_dist.set_data([np.nan]*len(v_sq), [np.nan]*len(v_sq))
    ax_dist.clear()
    ax_dist.set(xticklabels=[], yticklabels=[])
    return [PART_1, RECT, mb_dist]

def animate(frame, patches):
    BOX.step(DT)
    PART_1.set_data(BOX.state[:, 0], BOX.state[:, 1])
    v_sq = (BOX.state[:, 2:4]**2).sum(axis=1)
    v_sq.sort()
    ax_dist.clear()
    n, bins, patches = ax_dist.hist(v_sq, bins=NOP, density=True)
    mb_dist.set_data(v_sq, maxwell_boltzmann(v_sq, 0.05))
    x_range = (0, bins.max())
    y_range = (0, max(mb_dist.get_data()[1].max(), n.max()))
    ax_dist.set(xlim=x_range, ylim=y_range,
                xticklabels=[], yticklabels=[])
    RECT.set_edgecolor('black')
    return [PART_1, RECT, *patches, mb_dist]

anim = animation.FuncAnimation(fig, animate, frames=600, interval=10,
                               blit=True, init_func=init, fargs=(patches,))
plt.show()
