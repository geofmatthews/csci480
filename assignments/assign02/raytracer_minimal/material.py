
import numpy as N
import pygame
import os

import ray
from ray import *
from vectors import *

class Material():
    def colorAt(self, point, normal, ray, world):
        return vec(1,1,1)
        
class Flat(Material):
    def __init__(self, color = (0.25, 0.5, 1.0)):
        self.color = color
                     
    def colorAt(self, point, normal, ray, world):
        return self.color
        
class Phong(Material):
    def __init__(self,
                 color=(0.25, 0.5, 1.0),
                 specularColor=(1,1,1),
                 ambient = 0.4,
                 diffuse = 1.0,
                 specular = 0.5,
                 shiny = 32):
        self.color = vec(color)
        self.specularColor = vec(specularColor)
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shiny = shiny

    def __repr__(self):
        c,a,d,sp,sh,shd = (self.color,self.ambient,self.diffuse,self.specular,self.shiny,self.shadows)
        return "Phong: %s %s %s %s %s %s" % (c,a,d,sp,sh,shd)

    def phongAt(self,
                color,
                specularColor,
                point,
                normal,
                ray,
                world):
        lights = world.lights
        eyeVector = -ray.vector
        c = self.ambient*color
        if N.dot(normal,eyeVector) < 0:
            normal = -normal
        for light in lights:
            lightVector = normalize(light.direction(point) )
            shadowRay = Ray(point, lightVector)
            if shadowRay.anyHit(world, light):
                continue
            ambientAndDiffuse = color*light.color()
            spec = specularColor*light.color()
            reflectedLight = reflect(lightVector, normal)
            c += self.diffuse * posDot(normal, lightVector) * ambientAndDiffuse
            c += self.specular * posDot(eyeVector, reflectedLight)**self.shiny * spec
        return clamp(c, 0.0, 1.0)

    def colorAt(self,
                point,
                normal,
                ray,
                world):
        return self.phongAt(self.color,
                            self.specularColor,
                            point,
                            normal,
                            ray,
                            world)
  
class Reflector(Phong):
    def __init__(self, color = vec((1,1,1))):
        Phong.__init__(self, color)
    def colorAt(self, point, normal, ray, world):
        pass
                        
class Image(Phong):
    def __init__(self,
                 imageName = os.path.join('images','tilecloud.png'),
                 imageScale = 10, #how big the image is in world space
                 phong=False,
                 specularColor = (1,1,1),
                 ambient = 0.2,
                 diffuse = 1.0,
                 specular = 0.0,
                 shiny = 0):
        Phong.__init__(self, (1,1,1), specularColor, ambient, diffuse, specular,shiny)
        self.imageName = imageName
        self.image = pygame.image.load(imageName)
        self.size = self.image.get_size()
        self.width, self.height = self.size
        self.scale = (self.width)/float(imageScale)
        self.phong = phong

    def colorAt(self,
                point,
                normal,
                ray,
                scene):
        pass
    
if __name__ == '__main__':
    p = Phong()
    ray = Ray((0,0,10),(0,0,-1))
    print ray
    world = World([Sphere()],[Light()],Camera())
    print(p.colorAt((0,0,1),(0,0,1),ray,world))
