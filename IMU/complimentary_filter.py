from quaternion import Quaternion
import math

class ComplimentaryFilter:
    def __init__(self):
        self.q = Quaternion(1,0,0,0)
        self.t = 0

    def update(self, msr):
        t = msr['t_sec']
        dt = t - self.t
        self.t = t
        w = Quaternion(0, msr['wx'], msr['wy'], msr['wz'])
        #q_fqa = fqa(msr)
        self.q = self.q.add(w.multiply(self.q).scalar_multiply(dt/2)) 
        self.q = Quaternion.normalize(self.q)

    def fqa(self, msr):
        ax = msr['ax']
        ay = msr['ay']
        az = msr['az']
        norm = math.sqrt(ax*ax + ay*ay + az*az) 
        #estimation of elevation quaternion (around y axes)
        sin_theta_a = (ax / norm)
        cos_theta_a = math.sqrt(1 - sin_theta_a ** 2)
        sin_half_theta = math.copysign(1, sin_theta_a) * math.sqrt((1 - cos_theta_a) / 2) 
        cos_half_theta = math.sqrt((1 + cos_theta_a) / 2)
        q_e = Quaternion(cos_half_theta, 0, sin_half_theta, 0)
        #estimation of roll quaternion (around x axis)
        sin_phi = (-ay / norm) / cos_theta_a
        cos_phi = (-az / norm) / cos_theta_a
        sin_half_phi = half_sin(sin_phi, cos_phi)
        cos_half_phi = half_cos(sin_phi, cos_phi)
#TODO singularity avoidance!!!
        q_r = Quaternion(cos_half_phi, sin_half_phi, 0, 0)
        #estimation of azimuth quaternion (around z axis)
        mx = msr['mx']
        my = msr['my']
        mz = msr['mz']
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
    #assert abs(cos) <= 1, 'cos = %r' % cos
    #assert abs(sin) <= 1, 'sin = %r' % sin 
    sin_half = math.copysign(1, sin) * math.sqrt((1 - cos + 0.0000001) / 2) 
    return sin_half

def half_cos(sin, cos):
    cos_half = math.sqrt((1 + cos+ 0.0000001) / 2)
    return cos_half

