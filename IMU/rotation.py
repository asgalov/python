import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

class Quaternion:
    def __init__(self, qa, qb, qc, qd):
        self.a = qa
        self.b = qb
        self.c = qc
        self.d = qd
        
    def multiply(self, q):
        return q
        
class MIMUBoard:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.i = (1,0,0)
        self.j = (0,1,0)
        self.k = (0,0,1)

def plot_board(ax, b):
    ax.quiver(b.x, b.y, b.z, b.i[0], b.i[1], b.i[2], length=1,pivot="tail",color="r")
    ax.quiver(b.x, b.y, b.z, b.j[0], b.j[1], b.j[2], length=1,pivot="tail",color="b")
    ax.quiver(b.x, b.y, b.z, b.k[0], b.k[1], b.k[2], length=1,pivot="tail",color="g")

def plot_random_vector(q):
    ax.quiver(random.randrange(0, 5), random.randrange(0, 5), random.randrange(0, 5), 1, 1, 2, length=1,pivot="tail",color="r")


q = Quaternion(1,1,1,1)
q.counter = 123
y = q.multiply(Quaternion(0,0,0,0))
print y.a, y.b

fig = plt.figure()
ax = fig.gca(projection='3d')
b = MIMUBoard()
max_ax_val = 3
min_ax_val = -3
ax.set_xlim(min_ax_val, max_ax_val)
ax.set_ylim(min_ax_val, max_ax_val)
ax.set_zlim(min_ax_val, max_ax_val)
num_of_frames = 25
frame_interval_ms = 50
array_of_function_parameters = ()
plot_board(ax, b)
#line_ani = animation.FuncAnimation(fig, plot_board, num_of_frames, fargs=(array_of_function_parameters), interval=frame_interval_ms, blit=False)
line_ani = animation.FuncAnimation(fig, plot_random_vector, num_of_frames, interval=frame_interval_ms, blit=False)
plt.show()
