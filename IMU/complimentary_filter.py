from quaternion import Quaternion

class ComplimentaryFilter:
    def __init__(self):
        self.q = Quaternion(1,0,0,0)
        self.t = 0

    def update(self, msr):
        t = msr['t_sec']
        dt = t - self.t
        self.t = t
        w = Quaternion(0, msr['wx'], msr['wy'], msr['wz'])
        self.q = self.q.add(w.multiply(self.q).scalar_multiply(dt/2)) 
        self.q = Quaternion.normalize(self.q)

        

