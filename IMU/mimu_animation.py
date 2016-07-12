import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

with open('accel_data.txt','r') as f:
    read_data = map(float, f.readlines())

f.close()

fig = plt.figure()
ax = fig.gca(projection='3d', xlim=(-3, 3), ylim=(-3, 3), zlim=(-3,3))
ox, = ax.plot([], [], lw=2)
oy, = ax.plot([], [], lw=2)
oz, = ax.plot([], [], lw=2)

x0,y0,z0 = 0,0,0
i = [1,0,0]
j = [0,1,0]
k = [0,0,1]

def set_vector(ox, i):
    ox.set_data([x0, x0 + i[0]], [y0, y0 + i[1]])
    ox.set_3d_properties([z0, z0 + i[2]])


def rotate_around_z(i, alpha):
    x = i[0] * np.cos(alpha) + i[1] * np.sin(alpha) 
    y = i[1] * np.cos(alpha) - i[0] * np.sin(alpha)
    z = i[2]
    i[0] = x
    i[1] = y
    i[2] = z


def init_v():
    ox.set_data([], [])
    ox.set_3d_properties([])
    oy.set_data([], [])
    oy.set_3d_properties([])
    oz.set_data([], [])
    oz.set_3d_properties([])
    return ox, oy, oz


def plot_v(n):
    rnd = read_data[n % len(read_data)]
    print read_data[n % len(read_data)]
    global i,j,k
    alpha = np.pi*rnd
    rotate_around_z(i, alpha)
    rotate_around_z(j, alpha)
    rotate_around_z(k, alpha)

    set_vector(ox, i)
    set_vector(oy, j)
    set_vector(oz, k)

    return ox,oy,oz


anim = animation.FuncAnimation(fig, plot_v, init_func=init_v, interval=10, blit=True)

plt.show()
