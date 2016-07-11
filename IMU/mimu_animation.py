import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


fig = plt.figure()
ax = fig.gca(projection='3d', xlim=(-3, 3), ylim=(-3, 3), zlim=(-3,3))
v = (0,0,0,1,1,1) 


def init_v():
    return ax.quiver(v[0], v[1], v[2], v[3], v[4], v[5], length=1,pivot="tail",color="w")

def plot_v(i):
    return ax.quiver(v[0], v[1], v[2], v[3] + 2*i, v[4], v[5], length=1, pivot="tail", color="b")

anim = animation.FuncAnimation(fig, plot_v, init_func=init_v, frames=20, interval=50, blit=True)
plt.show()
