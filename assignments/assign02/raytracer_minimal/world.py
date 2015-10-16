import random, numpy

from vectors import *
from camera import *
from rotations import *

from light import *
from shape import *

EPSILON = 1.0e-10

class AbstractWorld():
    def colorAt(self, x, y):
        pass
    
class World(AbstractWorld):
    def __init__(self, 
                 objects=None, 
                 lights=None,
                 camera=None,
                 maxDepth = 5,
                 neutral = vec(.25,.5,1),
                 fogBegin = 1.0e10,
                 fogEnd = 1.0e10,
                 nsamples = 1):
        if not(objects):
            objects = [Sphere()]
        if not(lights):
            lights = [Light()]
        if not(camera):
            camera = Camera()

        self.objects = objects
        self.lights = lights
        self.camera = camera
        self.maxDepth = maxDepth
        self.neutral = vec(neutral)
        self.nsamples = nsamples
        self.fogBegin = fogBegin
        self.fogEnd = fogEnd

    def colorAt(self, x, y):
        ray = self.camera.ray(x,y)
        if ray.depth > self.maxDepth:
            return self.neutral
        else:
            return self.colorFromRay(ray)
        
    def colorFromRay(self, ray):
        if ray.depth > self.maxDepth:
            return self.neutral
        dist, point, normal, obj = ray.closestHit(self)
        if not(obj is None):
            if dist > self.fogEnd:
                return self.neutral
            elif dist < self.fogBegin:
                color = obj.material.colorAt(point,
                                             normal,
                                             ray,
                                             self)
                if color is None:
                    print "none color"
                    return self.neutral
                else:
                    return clamp(color, 0, 1)
            else:
                fogPortion = (dist-self.fogBegin)/(self.fogEnd-self.fogBegin)     
                color = obj.material.colorAt(point,
                                             normal,
                                             ray,
                                             self)
                if color is None:
                    print "none color"
                    return self.neutral
                finalColor = (1-fogPortion)*color + (fogPortion)*self.neutral
                return clamp(finalColor, 0, 1)
        else:
            return self.neutral
            
class ThreeSpheres(World):
    def __init__(self,
                 objects=None,
                 lights=None,
                 camera=None):
        if not(lights):
            lights = [Light((1,1,.5))]
        if not(objects):
            objects = [Sphere((2,2,-1),3,Phong(color=(1,0,0))),
                       Sphere((2,-2,-0),3,Phong(color=(0,1,0))),
                       Sphere((-2,0,1),3,Phong(color=(0,0,1)))]
        if not(camera):
            camera = Camera()
        World.__init__(self, objects, lights, camera)


if __name__ == "__main__":
    w = World([Sphere()],[Light()],Camera())
    print(w.neutral)

                    
