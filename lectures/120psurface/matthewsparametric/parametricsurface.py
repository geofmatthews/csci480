import numpy as N
from vectors import *
from quad import Quad
from transform import *

class ParametricSurface():
    def __init__(self,
                 uSteps = (0.0, 1.0, 0.1),
                 vSteps = (0.0, 1.0, 0.1),
                 transform = identity(),
                 color = (1,1,1)):
        self.uSteps = makeVector(uSteps)
        self.vSteps = makeVector(vSteps)
        self.transform = transform
        self.color = makeVector(color)
        self.generateQuads()

    def __repr__(self):
        return "PSurf:"+repr(self.uSteps)+repr(self.vSteps)

    def function(self, u, v):
        return makeVector(u, v, 0.0, 1.0)

    def generateQuads(self, uSteps=None, vSteps=None):
        if uSteps != None:
            self.uSteps = uSteps
        if vSteps != None:
            self.vSteps = vSteps
        uStep = self.uSteps[2]
        vStep = self.vSteps[2]
        self.quads = []
        for u in N.arange(*self.uSteps):
            for v in N.arange(*self.vSteps):
                a = self.function(u      , v      )
                b = self.function(u+uStep, v      )
                c = self.function(u+uStep, v+vStep)
                d = self.function(u      , v+vStep)
                points = [N.dot(self.transform,p) for p in (a,b,c,d)]
                self.quads.append( Quad(points, self.color) )

    def moreDetail(self):
        self.uSteps[2] *= 0.5
        self.vSteps[2] *= 0.5
        self.generateQuads()

    def lessDetail(self):
        self.uSteps[2] *= 2.0
        self.vSteps[2] *= 2.0
        self.generateQuads()

class PGroup(ParametricSurface):
    def __init__(self, listOfPSurfs):
        self.psurfs = listOfPSurfs
        self.generateQuads()

    def generateQuads(self):
        self.quads = []
        for p in self.psurfs:
            self.quads.extend(p.quads)

    def moreDetail(self):
        for p in self.psurfs:
            p.moreDetail()
        self.generateQuads()

    def lessDetail(self):
        for p in self.psurfs:
            p.lessDetail()
        self.generateQuads()

class TinySurface(ParametricSurface):
    def __init__(self,
               uSteps=(-5,5,1),
               vSteps=(-5,5,1),
               transform=identity()):
        ParametricSurface.__init__(self, uSteps, vSteps, transform)

class PTajInset(ParametricSurface):
    def __init__(self,
                 uSteps = (0.001,14,1),
                 vSteps = (N.pi, 2*N.pi, 0.1*N.pi),
                 radius = 5
                 ):
        self.radius = radius
        self.height = 1.3*radius
        ParametricSurface.__init__(self, uSteps, vSteps)
        
    def function(self, u, v):
        radius = self.radius*(2.0/(1.0+N.exp(-u))- 1.0) # logistic function
        x = N.cos(v)*radius
        z = N.sin(v)*radius
        y = -self.height * (2.0*u/self.uSteps[1] - 1.0)
        return makeVector(x,y,z,1.0)

class PTajSurface(ParametricSurface):
    def __init__(self,
                 width = 10,
                 height = 10,
                 insetRadius = 4,
                 insetHeight = 8,
                 steps = 20):
        uSteps = (-width/2.0, width/2.0, width/float(steps))
        vSteps = (-height/2.0, height/2.0, height/float(steps))
        self.insetRadius = insetRadius
        self.insetHeight = insetHeight
        ParametricSurface.__init__(self, uSteps, vSteps)

    def function(self, u, v):
        uu = u+self.insetHeight/2.0
        insetRadius = self.insetRadius*(2.0/(1.0+N.exp(-uu))-1.0)
        absV = N.absolute(v)
        if absV > insetRadius:
            return makeVector(u, v, 0, 1)
        else:
            z = - N.sqrt(insetRadius*insetRadius - absV*absV)
            return makeVector(u, v, z, 1)

class PCheckerBox(ParametricSurface):
    def __init__(self,
               uSteps=(-5,5,1),
               vSteps=(-5,5,1),
               transform=identity()):
        ParametricSurface.__init__(self, uSteps, vSteps, transform)

    def function(self, u, v):
        if ((int(0.5*u)+int(0.5*v)) % 2) == 0:
            return makeVector(u,v,1,1)
        else:
            return makeVector(u,v,0,1)



class PSphere(ParametricSurface):
    def __init__(self,
                 uSteps = (0, 2*N.pi, 0.125*N.pi),
                 vSteps = (-0.5*N.pi, 0.5*N.pi, 0.125*N.pi),
                 transform = scaleU(5)):
        ParametricSurface.__init__(self, uSteps, vSteps, transform)

    def function(self, u, v):
        return makeVector(N.cos(v)*N.cos(u), N.cos(v)*N.sin(u), N.sin(v),1.0)

class PTorus(ParametricSurface):
    def __init__(self,
                 uSteps = (0, 2*N.pi, 0.125*N.pi),
                 vSteps = (0, 2*N.pi, 0.25*N.pi),
                 transform=identity(),
                 majorRadius = 4,
                 minorRadius = 1
                 ):
        self.majorRadius = majorRadius
        self.minorRadius = minorRadius
        ParametricSurface.__init__(self, uSteps, vSteps, transform)

    def function(self, u, v):
        R = self.majorRadius
        r = self.minorRadius
        x = (R + r*N.cos(v))*N.cos(u)
        y = (R + r*N.cos(v))*N.sin(u)
        z = r * N.sin(v)
        return makeVector(x,y,z,1.0)
        
class PSinCos(ParametricSurface):
    def __init__(self,
                 uSteps=(-2*N.pi,2*N.pi,0.25*N.pi),
                 vSteps=(-2*N.pi,2*N.pi,0.25*N.pi),
                 transform=identity()):
        ParametricSurface.__init__(self, uSteps, vSteps, transform)

    def function(self, u, v):
        return makeVector(u, v, N.sin(u)*N.cos(v), 1.0)

class PCosDist(ParametricSurface):
    def __init__(self,
                 uSteps=(-5,5,.5),
                 vSteps=(-5,5,.5),
                 transform = identity()):
        ParametricSurface.__init__(self, uSteps, vSteps, transform)

    def function(self, u, v):
        sqdist = 0.25*(u*u + v*v)
        return makeVector(u,v, N.sin(sqdist), 1.0)

class PSinc(ParametricSurface):
    def __init__(self,
                 uSteps=(-4*N.pi, 4*N.pi, 0.5*N.pi),
                 vSteps=(-4*N.pi, 4*N.pi, 0.5*N.pi),
                 transform = scale(0.5,0.5,3)):
        ParametricSurface.__init__(self, uSteps, vSteps, transform)
        
    def function(self, u, v):
        dist = N.sqrt(u*u + v*v)
        if dist == 0.0:
            sinc = 1.0
        else:
            sinc = N.sin(dist)/dist
        return makeVector(u,v, sinc, 1.0)
                 

class PConchoid(ParametricSurface):
    def __init__(self,
                 uSteps = (N.pi,5*N.pi, 0.2*N.pi),
                 vSteps = (0,2*N.pi, 0.2*N.pi),
                 transform=translation(0,0,N.pi)):
        ParametricSurface.__init__(self, uSteps, vSteps, transform)

    def function(self, u, v):
        return makeVector(1.1**u * (1.0+N.cos(v)) * N.cos(u),
                          1.1**u * (1.0+N.cos(v)) * N.sin(u),
                          1.1**u * N.sin(v) - 1.5*1.1**u,
                          1.0)

if __name__ == "__main__":
    s = ParametricSurface(uSteps = (0,1,.5), vSteps = (0,1,.5))
    print s
    print s.quads
