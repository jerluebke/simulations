# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from set_box import foreign_particles


DT = 1/30
BOX = foreign_particles(1000, nofp=3, fpm=.5, speed=(5, 1),
                        bounds=[-10, 10, -10, 10])
NOFP = 3
# P[forgein particle][coordinate (0:x, 1:y)]
PATH_DATA = BOX.state[:NOFP, :2].reshape(NOFP, 2, 1).tolist()


fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(BOX.bounds[0]-.4, BOX.bounds[1]+.4),
                     ylim=(BOX.bounds[2]-.4, BOX.bounds[3]+.4),
                     xticks=[], yticks=[],
                     xticklabels=[], yticklabels=[])

PART_F, = ax.plot([], [], 'yo', ms=10, zorder=1)   # foreign
PART_N, = ax.plot([], [], 'bo', ms=4, zorder=2)   # normal
# paths of foreign particles
PATHS = [ax.plot([], [], 'k-', lw=0.5, zorder=3)[0] for _ in range(NOFP)]

RECT = plt.Rectangle(BOX.bounds[::2],
                     BOX.bounds[1] - BOX.bounds[0],
                     BOX.bounds[3] - BOX.bounds[2],
                     ec='none', lw=2, fc='none')
ax.add_patch(RECT)


def init():
    PART_F.set_data([], [])
    PART_N.set_data([], [])
    for i in range(NOFP):
        PATHS[i].set_data([], [])
    RECT.set_edgecolor('none')
    return [PART_F, PART_N, *PATHS, RECT]

def animate(frame):
    BOX.step(DT)
    for i in range(NOFP):
        PATH_DATA[i][0].append(BOX.state[i][0])
        PATH_DATA[i][1].append(BOX.state[i][1])
        PATHS[i].set_data(*PATH_DATA[i])
        #  PATHS[i].set_zorder(3)
    PART_F.set_data(BOX.state[:NOFP, 0], BOX.state[:NOFP, 1])
    PART_N.set_data(BOX.state[NOFP:, 0], BOX.state[NOFP:, 1])
    #  PART_F.set_zorder(1)
    #  PART_N.set_zorder(2)
    RECT.set_edgecolor('black')
    return [PART_F, PART_N, *PATHS, RECT]


anim = animation.FuncAnimation(fig, animate, frames=600, interval=10,
                               blit=True, init_func=init)
plt.show()
