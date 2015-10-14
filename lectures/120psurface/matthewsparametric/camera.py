
from transform import *
from vectors import *
from quad import Quad

EPSILON = 0.0001

class Camera():
    def __init__(self, 
                 distance = 10.0,
                 width = 20.0,
                 height = 15.0,
                 transform = identity()):
        self.distance = distance
        self.width = width
        self.height = height
        self.xscale = 2.0*distance/float(width)
        self.yscale = 2.0*distance/float(height)
        self.transform = N.dot(translation(0,0,-self.distance),
                               transform)

    def dollyZoom(self, distance):
        self.distance += distance
        self.xscale = 2.0*self.distance/float(self.width)
        self.yscale = 2.0*self.distance/float(self.height)
        self.transform = N.dot(translation(0,0,-distance),self.transform)
        
    def setWidthHeight(self, width, height):
        self.width = width
        self.height = height
        self.xscale = 2.0*distance/float(self.width)
        self.yscale = 2.0*distance/float(self.height)

    def leftMultiply(self, trans):
        self.transform = N.dot(trans, self.transform)

    def rightMultiply(self, trans):
        self.transform = N.dot(self.transform, trans)

    def rigidTransformPoint(self, point):
        return N.dot(self.transform, point)

    def rigidTransform(self, quad):
        return Quad([N.dot(self.transform,p) for p in quad.points],
                    quad.color,
                    N.dot(self.transform,quad.normal))
    
    def project(self, point):
        x,y,z,w = point
        if N.abs(z) < EPSILON:
            return None
        pp = (x*self.xscale/-z, y*self.yscale/-z)
        return pp
        
