import numpy as np
import math
import copy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from quaternion import Quaternion
import pendulum
from complimentary_filter import ComplimentaryFilter

class Mimu:
    def __init__(self, qi_0 = Quaternion(0,1,0,0),
                       qj_0 = Quaternion(0,0,1,0),
                       qk_0 = Quaternion(0,0,0,1),
                       x0 = 0,
                       y0 = 0,
                       z0 = 0):
        self.qi = qi_0
        self.qj = qj_0
        self.qk = qk_0
        self.x0 = x0 
        self.y0 = y0
        self.z0 = z0

    def rotate(self, q):
        self.qi = q.conjugate().multiply(self.qi).multiply(q)
        self.qj = q.conjugate().multiply(self.qj).multiply(q)
        self.qk = q.conjugate().multiply(self.qk).multiply(q)


# read IMU measurements in the following format:
# 't_sec', 'ax', 'ay', 'az', 'wx', 'wy', 'wz', 'mx', 'my', 'mz'
msrlist = []
msrlist = pendulum.read_msr_from_file('imu_sim_data.csv')

# calc MIMU board attitude for each measurements
attitude = []
cp = ComplimentaryFilter()
for msr in msrlist:
    cp.update(msr)
    mimu = Mimu()
    mimu.rotate(cp.q)
    attitude.append(copy.deepcopy(mimu))

# plow MIMU attitude
fig = plt.figure()
ax = fig.gca(projection='3d', xlim=(-3, 3), ylim=(-3, 3), zlim=(-3,3))
ox, = ax.plot([], [], lw=2)
oy, = ax.plot([], [], lw=2)
oz, = ax.plot([], [], lw=2)

def plot_v(n):
    mimu = attitude[n % len(attitude)]
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

anim = animation.FuncAnimation(fig, plot_v, interval=5, blit=True)
plt.show()
