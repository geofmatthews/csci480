
from vectors import *
import numpy as N

class Quad():
    def __init__(self, points, color, normal = None):
        self.points = points
        if normal != None:
            self.normal = normal
        else:
            v1 = points[1] - points[0]
            v2 = points[len(points)-1] - points[0]
            self.normal = normalize(cross(v1,v2))
        self.color = N.clip(makeArray(color), 0.0, 1.0)
        self.shadedColor = self.color

    def __repr__(self):
        return "Quad:"+repr(self.points)

    def centerZ(self):
        return sum([p[2] for p in self.points])/float(len(self.points))
