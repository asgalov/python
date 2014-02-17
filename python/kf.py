import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv


SYSTEM_NOISE = 0.1
MSR_NOISE = 100

class State:
    def __init__(self, x, cov, t):
    	self.x = x 
	self.cov = cov
	self.t = t

def next(state, p, t):
    if state is None:
        x = np.matrix([[p],[0]])
	cov = np.matrix([[MSR_NOISE, 0],[0, MSR_NOISE]])
	return State(x, cov, t)

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
    ns = State(x_corr, P_corr, t)
    return ns


data = np.genfromtxt('data.csv', delimiter=";")
state = None
filtered = []

for raw in data:
    t = raw[0]
    p = raw[1]
    state = next(state, p, t)
    filtered.append(state.x.item(0,0))


x = data[:,0]
y = data[:,1]
plt.plot(x,y, color="gray")
plt.plot(x,filtered, color="red")
plt.show()
