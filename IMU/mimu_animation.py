import numpy as np
import copy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from quaternion import Quaternion
from mimu import Mimu

# read IMU measurements in the following format:
# 'n','t_sec', 'ax', 'ay', 'az', 'wx', 'wy', 'wz', 'mx', 'my', 'mz'
msrlist = []
with open('imu_sim_data.csv', 'r') as f:
    keys = next(f).split()
    for line in f:
        values = map(float, line.split())
        msrlist.append(dict(zip(keys, values)))

# calc MIMU board attitude for each measurements
mimu = Mimu()
attitude = []
for msr in msrlist:
    alpha = msr['wy']
    qz = Quaternion(np.cos(alpha / 2), 0, 0, np.sin(alpha / 2))
    qx = Quaternion(np.cos(alpha / 2), np.sin(alpha / 2), 0, 0)
    mimu.rotate(qz)
    mimu.rotate(qx)
    attitude.append(copy.deepcopy(mimu))
 
# plow MIMU attitude
fig = plt.figure()
ax = fig.gca(projection='3d', xlim=(-3, 3), ylim=(-3, 3), zlim=(-3,3))
ox, = ax.plot([], [], lw=2)
oy, = ax.plot([], [], lw=2)
oz, = ax.plot([], [], lw=2)

def plot_v(n):
    mimu = attitude[n]
    plot_attitude(mimu)
    return ox,oy,oz

def plot_attitude(mimu):
    global ox, oy, oz
    plot_vector(ox, mimu.x0, mimu.y0, mimu.z0, mimu.qi)
    plot_vector(oy, mimu.x0, mimu.y0, mimu.z0, mimu.qj)
    plot_vector(oz, mimu.x0, mimu.y0, mimu.z0, mimu.qk)

def plot_vector(ox, x0, y0, z0, q):
    ox.set_data([x0, x0 + q.b], [y0, y0 + q.c])
    ox.set_3d_properties([z0, z0 + q.d])

anim = animation.FuncAnimation(fig, plot_v, interval=10, blit=True)
plt.show()
