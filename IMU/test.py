import matplotlib.pyplot as plt
from complimentary_filter import ComplimentaryFilter
# from ggplot import *
# TODO use ggplot and pandas for plotting in python


def read_msr_from_file(filename):
    msr = []
    with open(filename, 'r') as f:
        keys = next(f).split()
        for line in f:
            values = map(float, line.split())
            msr.append(dict(zip(keys, values)))
    f.close()
    return msr


msr_list = read_msr_from_file("imu.dat")

quaternions = []
pitch = []
times = []
cf = ComplimentaryFilter()
for m in msr_list:
    cf.update(m)
    pitch.append(cf.q.d)
    times.append(m['t'])

plt.plot(times, pitch)
plt.show()