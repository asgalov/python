from quaternion import Quaternion
import math


class ComplimentaryFilter:
    def __init__(self, k=0.5):
        self.q = Quaternion(1, 0, 0, 0)
        self.t = 0
        self.k = k

    def update(self, msr):
        t = msr['t']
        dt = t - self.t
        self.t = t
        w = Quaternion(0, msr['gyro.x'], msr['gyro.y'], msr['gyro.z'])
        q_fqa = fqa(msr)
        dq_static = q_fqa.add((self.q.scalar_multiply(-1))).scalar_multiply(1/dt)
        dq_dynamic = w.multiply(self.q).scalar_multiply(0.5)
        dq = dq_static.scalar_multiply(self.k).add(dq_dynamic.scalar_multiply(1 - self.k))
        self.q = self.q.add(dq.scalar_multiply(dt))
        self.q = Quaternion.normalize(self.q)


def fqa(msr):
    ax = msr['accel.x']
    ay = msr['accel.y']
    az = msr['accel.z']
    norm = math.sqrt(ax*ax + ay*ay + az*az)
    # estimation of elevation quaternion (around y axes)
    sin_theta_a = (ax / norm)
    cos_theta_a = math.sqrt(1 - sin_theta_a ** 2)
    sin_half_theta = math.copysign(1, sin_theta_a) * math.sqrt((1 - cos_theta_a) / 2)
    cos_half_theta = math.sqrt((1 + cos_theta_a) / 2)
    q_e = Quaternion(cos_half_theta, 0, sin_half_theta, 0)
    # estimation of roll quaternion (around x axis)
    sin_phi = (-ay / norm) / cos_theta_a
    cos_phi = (-az / norm) / cos_theta_a
    sin_half_phi = half_sin(sin_phi, cos_phi)
    cos_half_phi = half_cos(sin_phi, cos_phi)
# TODO singularity avoidance!!!
    q_r = Quaternion(cos_half_phi, sin_half_phi, 0, 0)
    # estimation of azimuth quaternion (around z axis)
    mx = msr['mag.x']
    my = msr['mag.y']
    mz = msr['mag.z']
    norm = math.sqrt(mx*mx + my*my + mz*mz)
    qm = Quaternion(0, mx / norm, my / norm, mz / norm)
    qm_a = q_e.multiply(q_r).multiply(qm).multiply(q_r.inverse()).multiply(q_e.inverse())
    Quaternion.normalize(qm_a)
    cos_zeta = qm_a.c
    sin_zeta = qm_a.b
    sin_half_zeta = half_sin(sin_zeta, cos_zeta)
    cos_half_zeta = half_cos(sin_zeta, cos_zeta)
    q_a = Quaternion(cos_half_zeta, 0, 0, sin_half_zeta)
    q_fqa = q_a.multiply(q_e).multiply(q_r)
    return q_fqa


def half_sin(sin, cos):
    # assert abs(cos) <= 1, 'cos = %r' % cos
    # assert abs(sin) <= 1, 'sin = %r' % sin
    sin_half = math.copysign(1, sin) * math.sqrt((1 - cos + 0.0000001) / 2) 
    return sin_half


def half_cos(sin, cos):
    cos_half = math.sqrt((1 + cos+ 0.0000001) / 2)
    return cos_half

