import math
import copy
from noise import Noise
from animation import Animator
from quaternion import Quaternion
from pendulum import Pendulum
from complimentary_filter import ComplimentaryFilter

pend = Pendulum(theta0 = math.pi / 6, l = 1)
msrlist, attitude, vel, times = pend.generate_measurements()

quaternions = []
cp = ComplimentaryFilter()
n = Noise(0.1, 0.1, 0.001, 0, 0, 0, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9)
noisy_msrlist = n.add_noise(msrlist)
for msr in noisy_msrlist:
    cp.update(msr)
    quaternions.append(cp.fqa(msr))

animator = Animator(quaternions)
animator.animate()
