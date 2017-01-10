import copy

import matplotlib.animation as animation
import matplotlib.pyplot as plt

import quaternion


class Mimu:
    def __init__(self, qi_0=quaternion.Quaternion(0, 1, 0, 0), qj_0=quaternion.Quaternion(0, 0, 1, 0),
                 qk_0=quaternion.Quaternion(0, 0, 0, 1), x0=0, y0=0, z0=0):
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


class Animator:
    """animate rotation of MIMU board with given quaternion sequence
    Parameters
    ----------
    quaternions: list of quaternions for rotation
    """
    def __init__(self, quaternions):
        self.fig = plt.figure()
        self.ax = self.fig.gca(projection='3d', xlim=(-3, 3), ylim=(-3, 3), zlim=(-3,3))
        self.ox, = self.ax.plot([], [], lw=2)
        self.oy, = self.ax.plot([], [], lw=2)
        self.oz, = self.ax.plot([], [], lw=2)
        self.attitude = []
        for q in quaternions:
            mimu = Mimu()
            mimu.rotate(q)
            self.attitude.append(copy.deepcopy(mimu))

    def plot_v(self, n):
        mimu = self.attitude[n % len(self.attitude)]
        self.plot_attitude(mimu)
        return self.ox, self.oy, self.oz

    def plot_attitude(self, mimu):
        plot_vector(self.ox, mimu.x0, mimu.y0, mimu.z0, mimu.qi)
        plot_vector(self.oy, mimu.x0, mimu.y0, mimu.z0, mimu.qj)
        plot_vector(self.oz, mimu.x0, mimu.y0, mimu.z0, mimu.qk)

    def animate(self):
        anim = animation.FuncAnimation(self.fig, self.plot_v, interval=5, blit=True)
        plt.show()


def plot_vector(ox, x0, y0, z0, q):
    ox.set_data([x0, x0 + q.b], [y0, y0 + q.c])
    ox.set_3d_properties([z0, z0 + q.d])
