import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv


SYSTEM_NOISE = 0.1
MSR_NOISE = 200

class State:
    def __init__(self, x, cov, v, z, t):
    	self.x = x 
	self.cov = cov
	self.v = v
	self.z = z
	self.t = t

def next(state, p, t):
    if state is None:
        x = np.matrix([[p],[0]])
	cov = np.matrix([[MSR_NOISE, 0],[0, MSR_NOISE]])
	return State(x, cov, 0, pow(MSR_NOISE, 0.5), t)

    A = np.matrix([[1, t - state.t], [0, 1]])
    Q = np.matrix([[SYSTEM_NOISE, 0], [0, SYSTEM_NOISE]])
    R = np.matrix([MSR_NOISE])
    x_pred = A * state.x 
    P_pred = A * state.cov * A.T + Q
    H = np.matrix([1, 0])
    Z = H * P_pred * H.T + R
    K = P_pred * H.T * np.linalg.inv(Z)
    v = np.matrix([p - x_pred.item(0,0)])
    x_corr = x_pred + K * v 
    P_corr = P_pred - K * H * P_pred
    ns = State(x_corr, P_corr, v.item(0,0), pow(MSR_NOISE,0.5), t)
    return ns


data = np.genfromtxt('data.csv', delimiter=";")
state = None
filtered = []
covariance = []
vv = []
zz = []
i = 0
for raw in data:
    i = i + 1
    t = raw[0]
    p = raw[1]
    state = next(state, p, t)
    filtered.append(state.x.item(0,0))
    covariance.append(state.cov.item(0,0))
    vv.append(state.v)
    zz.append(0.5*state.z)
    print i,',',p


x = data[:,0]
y = data[:,1]
#plt.plot(x,y, color="gray")
#plt.plot(x,filtered, color="red")

# Two subplots, the axes array is 1-d
f, axarr = plt.subplots(2, sharex=True)
axarr[0].plot(x, vv, color="gray")
axarr[0].plot(x, zz,color="red")
axarr[0].set_title('Sharing X axis')
axarr[1].plot(x, y, color="gray")
axarr[1].plot(x, filtered, color="red")

#plt.plot(x, covariance)
#plt.plot(x, vv)
plt.show()
