import math
import pdb
import matplotlib.pyplot as plt

class Pendulum:
    keys=['t_sec', 'ax', 'ay', 'az', 'wx', 'wy', 'wz', 'mx', 'my', 'mz']

    def __init__(self,
                 theta0 = math.pi / 6,              # initial angle 
                 l = 0.5,                           # pendulum length                           
                 g = 9.8,                           # gravity acceleration
                 B = 0.48,                          # magnetic flux density
                 beta = 60.483 * math.pi / 180,     # angle of magnetic field inclination
                 tick_sec = 0.01,                   # sampling period in sec
                 total_time_sec = 60):              # time of pendulum motion
        # set initial parameters of pendulum motion:
        self.theta0 = theta0 
        self.l = l 
        self.g = g
        self.B = B
        self.beta = beta
        self.tick_sec = tick_sec
        self.total_time_sec = total_time_sec

    def generate_measurements(self):
        msrlist = []
        attitude = []
        vel = []
        times = []
        # initial values 
        theta = math.pi / 6
        w_theta = 0
        t = 0  
        for i in range(0, int(self.total_time_sec / self.tick_sec)):
            t += self.tick_sec
            theta, w_theta = self.kutta(t, theta, w_theta) 
            msr = self.generate_msr(t, theta, w_theta, 0)
            #pdb.set_trace()
            msrlist.append(dict(zip(Pendulum.keys, msr)))
            attitude.append(180 * theta / math.pi)
            vel.append(180 * w_theta / math.pi)
            times.append(t)
        return msrlist, attitude, vel,times

    def kutta(self, t, theta, w_theta):
        h = self.tick_sec
        k_0 = h * self.f(t, theta, w_theta)
        l_0 = h * self.z(t, theta, w_theta)
        k_1 = h * self.f(t + 0.5 * h, theta + 0.5 * k_0, w_theta + 0.5 * l_0)
        l_1 = h * self.z(t + 0.5 * h, theta + 0.5 * k_0, w_theta + 0.5 * l_0)
        k_2 = h * self.f(t + 0.5 * h, theta + 0.5 * k_1, w_theta + 0.5 * l_1)
        l_2 = h * self.z(t + 0.5 * h, theta + 0.5 * k_1, w_theta + 0.5 * l_1)
        k_3 = h * self.f(t + h, theta + k_2, w_theta + l_2)
        l_3 = h * self.z(t + h, theta + k_2, w_theta + l_2)
        k_step = (1.0/6.0) * (k_0 + 2 * k_1 + 2 * k_2 + k_3)
        l_step = (1.0/6.0) * (l_0 + 2 * l_1 + 2 * l_2 + l_3)
        theta = theta + k_step 
        w_theta = w_theta + l_step
        #pdb.set_trace()
        return (theta, w_theta) 

    def z(self, h, theta, w_theta):
        return (-self.g / self.l) * math.sin(theta) 

    def f(self, h, theta, w_theta):
        return w_theta 

    def generate_msr(self, t, theta, w_theta, a_theta):
        # generate acceleration measurements:
        ax = self.l * a_theta + self.g * math.sin(theta)  
        ay = 0
        az = -self.l * w_theta**2 - self.g * math.cos(theta)
        # generate angular rate measurements:
        wx = 0
        wy = w_theta
        wz = 0
        # generate magnetometer measurements:
        mx = self.B * math.cos(self.beta + theta) 
        my = 0
        mz = self.B * math.sin(self.beta + theta)
        return [t,ax,ay,az,wx,wy,wz,mx,my,mz]

def print_to_file(filename, msrlist):
    with open(filename, 'w') as f:
        f.write("t_sec ax ay az wx wy wz mx my mz \n")
        for msr in msrlist:
            #pdb.set_trace()
            msrstr = ''
            for k in Pendulum.keys:
                msrstr += str(msr.get(k)) + ' '
            f.write(msrstr[:-1] + '\n')
            print msrstr
    f.close()

def read_msr_from_file(filename):
    msrlist = []
    with open(filename, 'r') as f:
        keys = next(f).split()
        for line in f:
            values = map(float, line.split())
            msrlist.append(dict(zip(keys, values)))
    f.close()
    return msrlist

def plot_measurements(msrlist):
    plt.plot(msrlist)
    plt.show()

#pend = Pendulum()
#msrlist, attitude, vel, times = pend.generate_measurements()
#print_to_file('imu_sim_data.csv', msrlist)
#    
#plt.plot(times, vel)
#plt.show()
