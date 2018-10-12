# -*- coding: utf-8 -*-

import numpy as np
import scipy.constants as sc
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from set_box import square_one_kind

mpl.rcParams['text.usetex'] = False


##############################################################################

# for animated text outside the axes bounding box
# see: https://stackoverflow.com/a/17562747/9133910
def _blit_draw(self, artists, bg_cache):
    # Handles blitted drawing, which renders only the artists given instead
    # of the entire figure.
    updated_ax = []
    for a in artists:
        # If we haven't cached the background for this axes object, do
        # so now. This might not always be reliable, but it's an attempt
        # to automate the process.
        if a.axes not in bg_cache:
            # bg_cache[a.axes] = a.figure.canvas.copy_from_bbox(a.axes.bbox)
            # change here
            bg_cache[a.axes] = a.figure.canvas.copy_from_bbox(a.figure.bbox)
        a.axes.draw_artist(a)
        updated_ax.append(a.axes)

    # After rendering all the needed artists, blit each axes individually.
    for ax in set(updated_ax):
        # and here
        # ax.figure.canvas.blit(ax.bbox)
        ax.figure.canvas.blit(ax.figure.bbox)


def _blit_clear(self, artists, bg_cache):
    # Get a list of the axes that need clearing from the artists that
    # have been drawn. Grab the appropriate saved background from the
    # cache and restore
    axes = set(a.axes for a in artists)
    for a in axes:
        if a in bg_cache:
            a.figure.canvas.restore_region(bg_cache[a])


# MONKEY PATCH!!
#  animation.Animation._blit_draw = _blit_draw
#  animation.Animation._blit_clear = _blit_clear

##############################################################################


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
ax_dist = fig.add_subplot(122, aspect='equal', autoscale_on=False,
                          xticklabels=[], yticklabels=[])

PART_1, = ax.plot([], [], 'bo', ms=6)

v_sq = (BOX.state[:, 2:4]**2).sum(axis=1)
v_sq.sort()

n, bins, patches = ax_dist.hist(v_sq, bins=NOP, density=True, color='b', zorder=1)
mb_dist, = ax_dist.plot([], [], 'r-', zorder=2)

RECT = plt.Rectangle(BOX.bounds[::2],
                     BOX.bounds[1] - BOX.bounds[0],
                     BOX.bounds[3] - BOX.bounds[2],
                     ec='none', lw=2, fc='none')
ax.add_patch(RECT)


X_RANGE = [0, bins.max()]
Y_RANGE = [0, n.max()]
#  ax_dist.set(xticklabels=np.arange(X_RANGE[1]),
#              yticklabels=np.arange(Y_RANGE[1]))

vel_text = ax_dist.text(0.2, 0.90, '', transform=ax_dist.transAxes)
dist_text = ax_dist.text(0.2, 0.85, '', transform=ax_dist.transAxes)


def init():
    PART_1.set_data([], [])
    RECT.set_edgecolor('none')
    mb_dist.set_data([np.nan]*len(v_sq), [np.nan]*len(v_sq))
    ax_dist.clear()
    ax_dist.set(xticklabels=[], yticklabels=[])
    #  ax_dist.set(xticklabels=np.arange(X_RANGE[1]),
    #              yticklabels=np.arange(Y_RANGE[1]))
    return [PART_1, RECT, mb_dist,]

def animate(frame, patches):
    BOX.step(DT)
    PART_1.set_data(BOX.state[:, 0], BOX.state[:, 1])
    v_sq = (BOX.state[:, 2:4]**2).sum(axis=1)
    v_sq.sort()
    ax_dist.clear()
    n, bins, patches = ax_dist.hist(v_sq, bins=NOP, density=True)
    mb_dist.set_data(v_sq, maxwell_boltzmann(v_sq, 0.05))

    if frame == 29:
        X_RANGE[1] = 0
        Y_RANGE[1] = 0
    x_new = bins.max()
    y_new = n.max()
    if not (frame+1)%30:
        if x_new > X_RANGE[1]:
            X_RANGE[1] = x_new
        if y_new > Y_RANGE[1]:
            Y_RANGE[1] = y_new

    ax_dist.set(xlim=X_RANGE, ylim=Y_RANGE,)
    #  xticklabels = ax_dist.set_xticklabels(np.arange(X_RANGE[1]))
    #  yticklabels = ax_dist.set_yticklabels(np.arange(Y_RANGE[1]))
    vel_text.set_text('max. velocity (x-axis): %f' % x_new)
    dist_text.set_text('max. density of states (normed, x-axis): '\
                       '%f' % y_new)
    RECT.set_edgecolor('black')

    return [PART_1, RECT, *patches, mb_dist,
            #  *xticklabels, *yticklabels
            dist_text, vel_text
           ]

anim = animation.FuncAnimation(fig, animate, frames=600, interval=10,
                               blit=True, init_func=init, fargs=(patches,))
plt.show()
