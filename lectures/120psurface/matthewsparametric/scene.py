
import pygame
from pygame.locals import *
import numpy as N
from vectors import *

class Scene():
    def __init__(self, psurf, lights, camera, renderLines=True, sort=True, backgroundColor=(.25,.5,1.0)):
        self.psurf = psurf
        self.lights = lights
        self.camera = camera
        self.renderLines = renderLines
        self.backgroundColor = makeVector(backgroundColor)
        self.sortPolys = sort

    def render(self, surface, screen):
        surface.fill(self.backgroundColor*255)
        w,h = surface.get_size()
        w *= 0.5
        h *= 0.5
        camtrans = self.camera.transform
        quads = self.psurf.quads
        # Transform:
        quads = [self.camera.rigidTransform(quad) for quad in quads]
        # Shading:
        for quad in quads:
            normal = quad.normal
            quad.shadedColor = makeVector(0,0,0)
            for light in self.lights:
                lightVector = normalize(light.point - quad.points[0])
                cos = posDot(lightVector, normal)
                quad.shadedColor += cos*light.color
            quad.shadedColor *= quad.color
            quad.shadedColor = clamp(quad.shadedColor, 0,1)
        # Sort:
        if self.sortPolys:
            quads.sort(key=lambda q:q.centerZ())
        # Project:
        for quad in quads:
            color = N.array(quad.shadedColor*255, dtype=int)
            xypoints = [self.camera.project(p) for p in quad.points]
            if any([x==None for x in xypoints]):
                continue
            pypoints = [(int(w+ p[0]*w), int(h+(-p[1])*h)) for p in xypoints]
            pygame.draw.polygon(surface,
                                color,
                                pypoints,
                                0)
            if self.renderLines:
                pygame.draw.lines(surface,
                                  (0,0,0),
                                  True,
                                  pypoints,
                                  1)
        return len(quads)
