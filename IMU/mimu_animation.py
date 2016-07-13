import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from quaternion import Quaternion

with open('accel_data.txt','r') as f:
    read_data = map(float, f.readlines())

f.close()

fig = plt.figure()
ax = fig.gca(projection='3d', xlim=(-3, 3), ylim=(-3, 3), zlim=(-3,3))
ox, = ax.plot([], [], lw=2)
oy, = ax.plot([], [], lw=2)
oz, = ax.plot([], [], lw=2)

x0,y0,z0 = 0,0,0
qi = Quaternion(0,1,0,0)
qj = Quaternion(0,0,1,0)
qk = Quaternion(0,0,0,1)

def plot_v(n):
    rnd = read_data[n % len(read_data)]
    global qi,qj,qk
    alpha = np.sign(0.5 - random.random()) * np.pi * rnd / 10.0
    qz = Quaternion(np.cos(alpha / 2), 0, 0, np.sin(alpha / 2))
    qz = Quaternion.normalize(qz)
    qx = Quaternion(np.cos(alpha / 2), np.sin(alpha / 2), 0, 0)
    qx = Quaternion.normalize(qx)
    print alpha
    qi = qx.conjugate().multiply(qz.conjugate()).multiply(qi).multiply(qz).multiply(qx)
    qj = qx.conjugate().multiply(qz.conjugate()).multiply(qj).multiply(qz).multiply(qx)
    qk = qx.conjugate().multiply(qz.conjugate()).multiply(qk).multiply(qz).multiply(qx)
    set_quaternion(ox, qi) 
    set_quaternion(oy, qj) 
    set_quaternion(oz, qk) 
    return ox,oy,oz

def set_quaternion(ox, q):
    ox.set_data([x0, x0 + q.b], [y0, y0 + q.c])
    ox.set_3d_properties([z0, z0 + q.d])

def set_vector(ox, i):
    ox.set_data([x0, x0 + i[0]], [y0, y0 + i[1]])
    ox.set_3d_properties([z0, z0 + i[2]])

anim = animation.FuncAnimation(fig, plot_v, interval=10, blit=True)

plt.show()
