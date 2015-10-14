import numpy as N
from vectors import *
from quad import Quad
from transform import *

class RSphere():
    def __init__(self, color=(1,1,1), recursion=2, transform=scaleU(5)):
        self.color = color
        self.recursion = recursion
        self.transform = transform
        self.generateQuads()

    def moreDetail(self):
        self.recursion += 1
        self.generateQuads()

    def lessDetail(self):
        self.recursion = max(0, self.recursion-1)
        self.generateQuads()

    def generateQuads(self):
        color = self.color
        recursion = self.recursion
        points = [makeVector(p) for p in
                  [(0,1,0,0),
                   (1,0,0,0),
                   (0,0,-1,0),
                   (-1,0,0,0),
                   (0,0,1,0),
                   (0,-1,0,0)]]
        self.quads = [Quad([points[a],points[b],points[c]], color) for
                 a,b,c in [(0,1,2),
                           (0,2,3),
                           (0,3,4),
                           (0,4,1),
                           (5,2,1),
                           (5,3,2),
                           (5,4,3),
                           (5,1,4)]]
        for r in range(recursion):
            self.quads = self.expand(self.quads)
        for quad in self.quads:
            for i,point in enumerate(quad.points):
                point[3] = 1
                quad.points[i] = N.dot(self.transform, point)

    def expand(self, oldquads):
        newquads = []
        for quad in oldquads:
            a,b,c = quad.points
            ab = normalize(0.5*(a+b))
            bc = normalize(0.5*(b+c))
            ca = normalize(0.5*(c+a))
            newquads.extend([Quad([x,y,z],quad.color) for
                             x,y,z in [(a,ab,ca),
                                       (b,bc,ab),
                                       (c,ca,bc),
                                       (ab,bc,ca)]
                             ])
        return newquads
               
