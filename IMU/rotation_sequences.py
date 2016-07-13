import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from quaternion import Quaternion

def set_quaternion(ox, q):
    ox.set_data([x0, x0 + q.b], [y0, y0 + q.c])
    ox.set_3d_properties([z0, z0 + q.d])

fig = plt.figure()
ax = fig.gca(projection='3d', xlim=(-3, 3), ylim=(-3, 3), zlim=(-3,3))

x0,y0,z0 = 0,0,0
qi = Quaternion(0,1,0,0)
qj = Quaternion(0,0,1,0)
qk = Quaternion(0,0,0,1)

alpha = np.pi / 6
q = Quaternion(np.cos(alpha / 2), np.sin(alpha / 2), 0, 0)
q = Quaternion.normalize(q)

qi = q.conjugate().multiply(qi).multiply(q)
qj = q.conjugate().multiply(qj).multiply(q)
qk = q.conjugate().multiply(qk).multiply(q)
 
ox, = ax.plot([], [], lw=2)
oy, = ax.plot([], [], lw=2)
oz, = ax.plot([], [], lw=2)

set_quaternion(ox, qi) 
set_quaternion(oy, qj) 
set_quaternion(oz, qk) 

plt.show()
