import numpy as N
from transforms import *

c = N.cos(0.01*N.pi)
s = N.sin(0.01*N.pi)

class Frame():
    def __init__(self):
        self.forward = N.array((0,0,-1),dtype=N.float32)
        self.up = N.array((0,1,0),dtype=N.float32)
        self.position = N.array((0.0, 2.0, 0.0),dtype=N.float32)
        self.rotation = N.identity(4, dtype=N.float32)
        self.translation = N.identity(4, dtype=N.float32)
        self.updateRotation()
        self.updateTranslation()
        self.updateMatrix()

    def move(self, amount):
        self.position += amount*self.forward
        self.updateTranslation()
        self.updateMatrix()

    def strafe(self, amount):
        right = N.cross(self.forward, self.up)
        self.position -= amount*right
        self.updateTranslation()
        self.updateMatrix()

    def rotate(self, sgn):
        up,forward = self.up, self.forward
        right = N.cross( forward, up)
        self.forward = c*forward - sgn*s*right
        self.updateRotation()
        self.updateMatrix()

    def tilt(self, sgn):
        up,forward = self.up, self.forward
        if (sgn > 0.0 and forward[1] < 0.99) or (sgn < 0.0 and forward[1] > -0.99):
            self.forward = c*forward + sgn*s*up
        self.updateRotation()
        self.updateMatrix()

    def inverseXZTranslation(self):
        m = N.copy(self.translation)
        m[2][0] *= -1
        m[2][2] *= -1
        return m

    def updateRotation(self):
        forward, up, position = self.forward, self.up, self.position
        right = N.cross(forward, up)
        up = N.cross(right, forward)
        rot = self.rotation
        rot[0][0] = right[0]
        rot[0][1] = right[1]
        rot[0][2] = right[2]
        rot[1][0] = up[0]
        rot[1][1] = up[1]
        rot[1][2] = up[2]
        rot[2][0] = -forward[0]
        rot[2][1] = -forward[1]
        rot[2][2] = -forward[2]

    def updateTranslation(self):
        trans, position = self.translation, self.position
        trans[0][3] = -position[0]
        trans[1][3] = -position[1]
        trans[2][3] = -position[2]

    def updateMatrix(self):
        self.matrix = N.dot(self.rotation, self.translation)
        
if __name__ == '__main__':
    f = Frame()
    original = N.copy(f.matrix)
    print N.round(f.matrix, 2)
    f.move(1)
    print N.round(f.matrix, 2)
    for i in range(100):
        f.rotate(1.0)
    print N.round(f.matrix, 2)
    f.move(1)
    print N.round(f.matrix, 2)
    print N.round(original - f.matrix, 2)
