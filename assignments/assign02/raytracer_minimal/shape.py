
from vectors import *
from ray import *
import numpy as N
from material import *
from rotations import *

EPSILON = 0.1

class GeometricObject():
    def hit(self, ray):
        """Returns (t, point, normal, object) if hit and t > EPSILON"""
        return (None, None, None, None)
    def castShadows(self):
        return False

class Sphere(GeometricObject):
    def __init__(self, point=(0,0,0), radius=1, material=None, shadows=True):
        if not(material):
            material = Phong()
        self.point = vec(point)
        self.radius = radius
        self.material = material
        self.shadows = shadows

    def __repr__(self):
        return "Sphere: " + repr(self.point) + repr(self.radius)
    def castShadows(self):
        return self.shadows

    def hit(self, ray):
        # assume sphere at origin, so translate ray:
        raypoint = ray.point - self.point
        a = N.dot(ray.vector, ray.vector)
        b = 2*N.dot(raypoint, ray.vector)
        c = N.dot(raypoint, raypoint) - self.radius*self.radius
        disc = b*b - 4*a*c
        if disc > 0.0:
            t = (-b-N.sqrt(disc))/(2*a)
            if t > EPSILON:
                p = ray.pointAt(t)
                n = normalize(self.normalAt(p))
                return (t, p, n, self)
            t = (-b+N.sqrt(disc))/(2*a)
            if t > EPSILON:
                p = ray.pointAt(t)
                n = normalize(self.normalAt(p))
                return (t, p, n, self)
        return (None, None, None, None)

    def normalAt(self, point):
        return normalize(point - self.point)


class Plane(GeometricObject):
    def __init__(self, normal, point, material, shadows=False):
        self.point = vec(point)
        self.normal = normalize(vec(normal))
        self.material = material
        self.shadows = shadows

    def __repr__(self):
        return "Plane: "+repr(self.normal)+repr(self.point)
    def castShadows(self):
        return self.shadows

    def hit(self, ray):
        pass
        
    def normalAt(self, point):
        return self.normal

class PlaneIntersection(GeometricObject):
    def __init__(self, planes):
        self.planes = planes
        self.shadows = True

    def castShadows(self):
        return self.shadows
            
    def hit(self, ray):
        pass

class Cube(PlaneIntersection):
    pass

class QuadricOfMyChoice(GeometricObject):
    pass

if __name__ == "__main__":
    s1 = Sphere(vec(0,0,0), 2, Phong())
    print( s1.normalAt(vec(0,0,2)))
    r = Ray(vec(-10,0,0), vec(1,0,0))
    print( s1.hit(r))
    
