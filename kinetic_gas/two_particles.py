# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from set_box import rectangle_one_kind_divided


DT = 1/30
BOX = rectangle_one_kind_divided(800, bounds=[-10, 10, -5, 5])
NOP = int(len(BOX.state)/2)


fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(BOX.bounds[0]-.4, BOX.bounds[1]+.4),
                     ylim=(BOX.bounds[2]-.4, BOX.bounds[3]+.4),
                     xticks=[], yticks=[],
                     xticklabels=[], yticklabels=[])

PART_1, PART_2, = ax.plot([], [], 'bo', [], [], 'ro', ms=6)

RECT = plt.Rectangle(BOX.bounds[::2],
                     BOX.bounds[1] - BOX.bounds[0],
                     BOX.bounds[3] - BOX.bounds[2],
                     ec='none', lw=2, fc='none')
ax.add_patch(RECT)


def init():
    PART_1.set_data([], [])
    PART_2.set_data([], [])
    RECT.set_edgecolor('none')
    return [PART_1, PART_2, RECT]

def animate(frame):
    BOX.step(DT)
    PART_1.set_data(BOX.state[:NOP, 0], BOX.state[:NOP, 1])
    PART_2.set_data(BOX.state[NOP:, 0], BOX.state[NOP:, 1])
    RECT.set_edgecolor('black')
    return PART_1, PART_2, RECT


anim = animation.FuncAnimation(fig, animate, frames=600, interval=10,
                               blit=True, init_func=init)
plt.show()
