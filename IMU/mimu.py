from quaternion import Quaternion

class Mimu:
    def __init__(self, qi_0 = Quaternion(0,1,0,0),
                       qj_0 = Quaternion(0,0,1,0),
                       qk_0 = Quaternion(0,0,0,1),
                       x0 = 0,
                       y0 = 0,
                       z0 = 0):
        self.qi = qi_0
        self.qj = qj_0
        self.qk = qk_0
        self.x0 = x0 
        self.y0 = y0
        self.z0 = z0

    def rotate(self, q):
        self.qi = q.conjugate().multiply(self.qi).multiply(q)
        self.qj = q.conjugate().multiply(self.qj).multiply(q)
        self.qk = q.conjugate().multiply(self.qk).multiply(q)

