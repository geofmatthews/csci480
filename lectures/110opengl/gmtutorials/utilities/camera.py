import numpy as N
from frames import Frame, project
from transforms import projection

class CameraFrame(Frame):
    """Not allowing rolling for this camera
       Not allowing forward to be straight up or down"""

    def renormalize(self):
        """Gram-Schmidt process, and reset up to +y"""
        
        # Move any vertical vectors slightly off
        # Note that moving "through" vertical will cause
        # the camera to snap back to looking down neg z
        # Not optimal, but if you want a camera capable
        # of that, just use an ordinary frame.
        
        epsilon = 0.000001
        if (N.abs(N.dot(self.back, (0,1,0,0))) == 1.0):
            self.back += N.array((0,0,epsilon,0),dtype=N.float32)
        self.back /= N.linalg.norm(self.back)
        self.up = N.array((0,1,0,0),dtype=N.float32)
        self.up -= project(self.up,self.back)
        self.up /= N.linalg.norm(self.up)
        self.right -= project(self.right,self.back) + \
                      project(self.right, self.up)
        self.right /= N.linalg.norm(self.right)

    def roll(self):
        pass
                          
class Camera(CameraFrame):
    def __init__(self,
                 lens = 4.0,
                 near = 0.1,
                 far = 1000.0,
                 aspectRatio = 1.0
                 ):
        CameraFrame.__init__(self)
        self.lens = lens
        self.near = near
        self.far = far  
        self.aspectRatio = aspectRatio
        self.changeLens(lens)

    def changeLens(self, lens):
        self.lens = lens
        self.yRatio = 1.0/lens
        self.xRatio = self.aspectRatio*self.yRatio
        right = self.near*self.xRatio
        top = self.near*self.yRatio
        self.proj = projection(self.near, self.far,
                               right, top)

    def onlyRotation(self):
        rot = N.array((self.right,
                       self.up,
                       self.back,
                       N.array((0.0, 0.0, 0.0, 1.0),dtype=N.float32)),
                      dtype=N.float32)
        return rot

    def projection(self):
        return self.proj

    def zoomIn(self, factor):
        self.changeLens(self.lens * factor)

    def zoomOut(self, factor):
        self.changeLens(self.lens/factor)

    # Camera specialized vocabulary:

    def pan(self, factor):
        self.yaw(factor * self.xRatio)

    def tilt(self, factor):
        self.pitch(factor * self.yRatio)

    def dolly(self, displacement):
        self.moveBack(-displacement)

    def truck(self, displacement):
        self.moveRight(displacement)

    def pedestal(self, displacement):
        self.moveUp(displacement)

if __name__ == "__main__":
    f = CameraFrame()
    f.moveBack(10)
    f.pitch(1)
    v = N.array((0,1,0,0))
    p = N.array((0,0,0,1))
    print f
    print N.dot(f.transform(), v)
    print N.dot(f.inverseTransform(), v)
    print N.dot(f.inverseTransform(), N.dot(f.transform(), v))
    print N.dot(f.transform(), p)
    print N.dot(f.inverseTransform(), p)
    print N.dot(f.inverseTransform(), N.dot(f.transform(), p))
    g = CameraFrame()
    for i in range(8):
        g.pitch(1.0)
    print "g:\n", g
    print N.dot(g.transform(),N.array((0,1,1,0), dtype=N.float32))
    g = CameraFrame()
    for i in range(8):
        g.yaw(1.0)
    print "g:\n", g
    print N.dot(g.transform(),N.array((1,0,1,0), dtype=N.float32))
    c = Camera()
