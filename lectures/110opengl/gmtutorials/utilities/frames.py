import numpy as N

def project(v, u):
    """Project v onto u"""
    return (N.dot(v,u)/N.dot(u,u))*u

class Frame():
    def __init__(self):
        self.position = N.array((0,0,0,1), dtype=N.float32) # origin
        self.right = N.array((1,0,0,0), dtype=N.float32)    # x
        self.up = N.array((0,1,0,0), dtype=N.float32)       # y
        self.back = N.array((0,0,1,0), dtype=N.float32)     # z
        self.postTransform = N.identity(4, dtype=N.float32)
        
    def __str__(self):
        return str(self.transform()) + "\n" + str(self.inverseTransform())

    # Note that because of the way we construct these matrices,
    # they are always "rotate then move", so the rotation never
    # affects the translation.
    
    def transform(self):
        return N.dot(self.postTransform,
                     N.transpose(N.array((self.right,
                                          self.up,
                                          self.back,
                                          self.position),dtype=N.float32)))

    def inverseTransform(self):
        rot = N.array((self.right,
                       self.up,
                       self.back,
                       N.array((0.0, 0.0, 0.0, 1.0),dtype=N.float32)),
                      dtype=N.float32)
        newpos = -self.position
        newpos[3] = 1.0
        tran = N.transpose(N.array(((1.0, 0.0, 0.0, 0.0),
                                    (0.0, 1.0, 0.0, 0.0),
                                    (0.0, 0.0, 1.0, 0.0),
                                    newpos),
                                   dtype=N.float32))
        return N.dot(rot, tran)

    def moveRight(self, displacement):
        self.position += displacement*self.right

    def moveUp(self, displacement):
        self.position += displacement*self.up

    def moveBack(self, displacement):
        self.position += displacement*self.back

    def setPosition(self, position):
        self.position = position

    def renormalize(self):
        """Gram-Schmidt process, start from self.back"""
        self.back /= N.linalg.norm(self.back)
        self.up -= project(self.up,self.back)
        self.up /= N.linalg.norm(self.up)
        self.right -= project(self.right,self.back) + \
                      project(self.right, self.up)
        self.right /= N.linalg.norm(self.right)

    def renormalizeFromUp(self):
        """Gram-Schmidt process, start from self.up"""
        self.up /= N.linalg.norm(self.up)
        self.back -= project(self.back,self.up)
        self.back /= N.linalg.norm(self.back)
        self.right -= project(self.right,self.back) + \
                      project(self.right, self.up)
        self.right /= N.linalg.norm(self.right)

    # this should not be used if we set forward to one of
    # up or right, Gram Schmidt will fail
    def setForward(self, forward):
        forward /= N.linalg.norm(forward)
        if N.abs(N.dot(forward,up)) == 1.0:
            print "Warning, attempt to set forward parallel to up"
            return
        if N.abs(N.dot(forward,back)) == 1.0:
            print "Warning, attempt to set forward parallel to back"
            return
        self.back = -forward
        self.renormalize()
     
    # using offsets instead of rotation angles guarantees
    # we don't have rotations more than 90 degrees,
    # so Gram-Schmidt will always work.
    # It also seems a bit more intuitive, and helps figuring
    # out the correct angle for a mouse movement on screen.        
    def pitch(self, displacement):
        self.back += displacement*self.up
        self.renormalize()

    def yaw(self, displacement):
        self.back += displacement*self.right
        self.renormalize()

    def roll(self, displacement):
        self.up += displacement*self.right
        self.renormalizeFromUp()

    # Convenience names for objects and cameras:
    def model(self):
        return self.transform()
    def view(self):
        return self.inverseTransform()

if __name__ == "__main__":
    f = Frame()
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
    g = Frame()
    for i in range(8):
        g.pitch(1.0)
    print "g:\n", g
    print N.dot(g.transform(),N.array((0,1,1,0), dtype=N.float32))
    g = Frame()
    for i in range(8):
        g.yaw(1.0)
    print "g:\n", g
    print N.dot(g.transform(),N.array((1,0,1,0), dtype=N.float32))
        
