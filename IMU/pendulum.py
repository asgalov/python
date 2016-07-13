import math

# initial parameters of pendulum motion:
theta0 = math.pi / 6 # initial angle 
l = 0.5 # pendulum length
g = 9.8 # gravity acceleration
B = 0.48 # magnetic flux density
beta = 60.483 * math.pi / 180 # angle of magnetic field inclination
t = 0 # initial time
tick = 0.1 # sampling period in sec

print "t_sec ax ay az wx wy wz mx my mz"
for i in range(0, 1000):
    t += tick
    theta = theta0 * math.cos(math.sqrt(g/l) * t)
    theta_v = -theta0 * math.sqrt(g/l) * math.sin(math.sqrt(g/l) * t)
    theta_a = -theta0 * (g/l) * math.cos(math.sqrt(g/l) * t) 

    # generate acceleration measurements:
    ax = l * theta_a + g * math.sin(theta)  
    ay = 0
    az = -l * theta_v**2 - g * math.cos(theta)

    # generate angular rate measurements:
    wx = 0
    wy = theta_v
    wz = 0

    # generate magnetometer measurements:
    mx = B * math.cos(beta + theta) 
    my = 0
    mz = B * math.sin(beta + theta)

    print t,ax,ay,az,wx,wy,wz,mx,my,mz


        
