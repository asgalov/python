import numpy as np

class Noise:
    keys=['t_sec', 'ax', 'ay', 'az', 'wx', 'wy', 'wz', 'mx', 'my', 'mz']

    def __init__(self,
                 acc_dev = 0.001,
                 gyro_dev = 0.001,
                 mag_dev = 0.001,
                 acc_x_bias = 0,
                 acc_y_bias = 0,
                 acc_z_bias = 0,
                 gyro_x_bias = 0,
                 gyro_y_bias = 0,
                 gyro_z_bias = 0,
                 mag_x_bias = 0,
                 mag_y_bias = 0,
                 mag_z_bias = 0):

        self.acc_dev = acc_dev
        self.gyro_dev = gyro_dev
        self.mag_dev = mag_dev
        self.acc_x_bias = acc_x_bias
        self.acc_y_bias = acc_y_bias
        self.acc_z_bias = acc_z_bias
        self.gyro_x_bias = gyro_x_bias
        self.gyro_y_bias = gyro_y_bias
        self.gyro_z_bias = gyro_z_bias
        self.mag_x_bias = mag_x_bias
        self.mag_y_bias = mag_y_bias
        self.mag_z_bias = mag_z_bias

    def add_noise(self, measurements):
        noisy_measurements = []
        for msr in measurements:
            noisy_msr = [msr["t_sec"],
                         msr["ax"] + np.random.normal(0, self.acc_dev) + self.acc_x_bias,
                         msr["ay"] + np.random.normal(0, self.acc_dev) + self.acc_y_bias,
                         msr["az"] + np.random.normal(0, self.acc_dev) + self.acc_z_bias,
                         msr["wx"] + np.random.normal(0, self.gyro_dev) + self.gyro_x_bias,
                         msr["wy"] + np.random.normal(0, self.gyro_dev) + self.gyro_y_bias,
                         msr["wz"] + np.random.normal(0, self.gyro_dev) + self.gyro_z_bias,
                         msr["mx"] + np.random.normal(0, self.mag_dev) + self.mag_x_bias,
                         msr["my"] + np.random.normal(0, self.mag_dev) + self.mag_y_bias,
                         msr["mz"] + np.random.normal(0, self.mag_dev) + self.mag_z_bias]
            noisy_measurements.append(dict(zip(Noise.keys, noisy_msr)))
        return noisy_measurements
