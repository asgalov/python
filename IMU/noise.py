import numpy as np

class Noise:
    keys=['t_sec', 'ax', 'ay', 'az', 'wx', 'wy', 'wz', 'mx', 'my', 'mz']

    def __init__(self, acc_dev = 0.001, gyro_dev = 0.001, mag_dev = 0.001):
        self.acc_dev = acc_dev
        self.gyro_dev = gyro_dev
        self.mag_dev = mag_dev

    def add_noise(self, measurements):
        noisy_measurements = []
        for msr in measurements:
            noisy_msr = [msr["t_sec"],
                         msr["ax"] + np.random.normal(0, self.acc_dev),
                         msr["ay"] + np.random.normal(0, self.acc_dev),
                         msr["az"] + np.random.normal(0, self.acc_dev),
                         msr["wx"] + np.random.normal(0, self.gyro_dev),
                         msr["wy"] + np.random.normal(0, self.gyro_dev),
                         msr["wz"] + np.random.normal(0, self.gyro_dev),
                         msr["mx"] + np.random.normal(0, self.mag_dev),
                         msr["my"] + np.random.normal(0, self.mag_dev),
                         msr["mz"] + np.random.normal(0, self.mag_dev)]
            noisy_measurements.append(dict(zip(Noise.keys, noisy_msr)))
        return noisy_measurements
