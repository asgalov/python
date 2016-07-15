import math
import matplotlib.pyplot as plt

class Pendulum:
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
        keys=['t_sec', 'ax', 'ay', 'az', 'wx', 'wy', 'wz', 'mx', 'my', 'mz']
        t = 0  # initial time
        for i in range(0, int(self.total_time_sec / self.tick_sec)):
            t += self.tick_sec
            theta = self.theta0 * math.cos(math.sqrt(self.g/self.l) * t)
            theta_v = -self.theta0 * math.sqrt(self.g/self.l) * math.sin(math.sqrt(self.g/self.l) * t)
            theta_a = -self.theta0 * (self.g/self.l) * math.cos(math.sqrt(self.g/self.l) * t) 

            # generate acceleration measurements:
            ax = self.l * theta_a + self.g * math.sin(theta)  
            ay = 0
            az = -self.l * theta_v**2 - self.g * math.cos(theta)

            # generate angular rate measurements:
            wx = 0
            wy = theta_v
            wz = 0

            # generate magnetometer measurements:
            mx = self.B * math.cos(self.beta + theta) 
            my = 0
            mz = self.B * math.sin(self.beta + theta)

            values = [t,ax,ay,az,wx,wy,wz,mx,my,mz]
            msrlist.append(dict(zip(keys, values)))
        return msrlist

def print_to_file(filename, msrlist):
    with open(filename, 'w') as f:
        f.write("t_sec ax ay az wx wy wz mx my mz \n")
        for msr in msrlist:
            msrstr = ''
            for v in msr.itervalues():   
                msrstr += str(v) + ' '
            f.write(msrstr[:-1] + '\n')
    f.close()

def plot_measurements(msrlist):
    plt.plot(msrlist)
    plt.show()


pend = Pendulum()
msrlist = pend.generate_measurements()
print_to_file('imu_sim_data.csv', msrlist)
