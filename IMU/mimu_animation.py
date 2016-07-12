import matplotlib.pyplot as plt
import random
import copy
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


fig = plt.figure()
ax = fig.gca(projection='3d', xlim=(-3, 3), ylim=(-3, 3), zlim=(-3,3))
ox, = ax.plot([], [], lw=2)
oy, = ax.plot([], [], lw=2)
oz, = ax.plot([], [], lw=2)

def init_v():
    ox.set_data([], [])
    ox.set_3d_properties([])
    oy.set_data([], [])
    oy.set_3d_properties([])
    oz.set_data([], [])
    oz.set_3d_properties([])
    return ox, oy, oz

def plot_v(i):
    x = 0
    y = np.sin(2 * np.pi * (x - 0.01 * i))
    z = np.sin(2 * np.pi * (x - 0.01 * i))
    ox.set_data([x,x], [y,y+1])
    ox.set_3d_properties([z,z])
    oy.set_data([x,x+1], [y,y])
    oy.set_3d_properties([z,z])
    oz.set_data([x,x], [y,y])
    oz.set_3d_properties([z,z+1])
    return ox,oy,oz

anim = animation.FuncAnimation(fig, plot_v, init_func=init_v, frames=200, interval=10, blit=True)

plt.show()
