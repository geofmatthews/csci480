# camera for ray tracer
# specify eye position and upper left, upper right,
# lower left, and lower right vectors

from ray import *
from vectors import *

class AbstractCamera():
    def ray(self, x, y):
        return Ray((0,0,0),(0,0,-1))

class Camera(AbstractCamera):
    def __init__(self,
                 eye = (0,0,10),
                 ul = (-10,10,-10),
                 ur = (10,10,-10),
                 ll = (-10,-10, -10),
                 lr = (10,-10,-10)):
        self.eye = vec(eye)
        self.ul = vec(ul)
        self.ur = vec(ur)
        self.ll = vec(ll)
        self.lr = vec(lr)
        
    def ray(self, x, y):
        """ given screen coords in [0,1]x[0,1] return ray from eye"""
        v1 = self.ul*(1-x) + self.ur*x
        v2 = self.ll*(1-x) + self.lr*x
        v = v1*(1-y) + v2*y
        return Ray(self.eye, normalize(v))

def lookAt(eye = (10,10,10),
           focus = (0,0,0),
           up = (0,1,0),
           fovy = 45.0,
           aspect = 4.0/3.0):
    pass
    
if __name__ == "__main__":
    c = Camera()
    print (c.ray(0.5,0.5))
