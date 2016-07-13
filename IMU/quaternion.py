import math

class Quaternion:
    def __init__(self, qa, qb, qc, qd):
        self.a = qa
        self.b = qb
        self.c = qc
        self.d = qd
        
    def multiply(self, q):
        a = self.a * q.a - self.b * q.b - self.c * q.c - self.d * q.d
        b = self.b * q.a + self.a * q.b - self.d * q.c + self.c * q.d
        c = self.c * q.a + self.d * q.b + self.a * q.c - self.b * q.d
        d = self.d * q.a - seld.c * q.b + self.b * q.c + selq.a * q.d
        return Quaternion(a,b,c,d)

    def conjugate(self):
        return Quaternion(self.a, -self.b, -self.c, -self.d)
    
    def norm(self):
        return math.sqrt(self.a ** 2 + self.b ** 2 + self.c ** 2 + self.d ** 2)

    def inverse(self):
        q = self.conjugate()
        n2 = self.norm() ** 2
        return Quaternion(q.a / n2, q.b / n2, q.c / n2, q.d / n2) 

    def get_normalized(q):
        return Quaternion(q.a / q.norm(), q.b / q.norm(),
                          q.c / q.norm(), q.d / q.norm) 
