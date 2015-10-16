from vectors import *

class AbstractRay():
    def pointAt(self, distance):
        """return the point at distance along the ray"""
        return (0,0,0)
    def closestHit(self, scene):
        """return (dist,point,normal,obj)"""
        return (None, None, None, None)
    def anyHit(self, scene, light):
        return False

class Ray(AbstractRay):
    def __init__(self, point, vector, depth=0):
        self.point = vec(point)
        self.vector = normalize(vec(vector))
        self.depth = depth

    def __repr__(self):
        return "Ray: " + repr(self.point) + ":" + repr(self.vector)

    def pointAt(self, distance):
        return self.point + distance * self.vector

    def closestHit(self, scene):
        dist, point, norm, obj = None, None, None, None  
        for o in scene.objects:
            hit = o.hit(self)
            if hit[0] != None:
                if dist == None:
                    dist,point,norm,obj = hit
                elif hit[0] < dist:
                    dist,point,norm,obj = hit
        return (dist,point,norm,obj)

    def anyHit(self, scene, light):
        for obj in scene.objects:
            dist,point,n,o = obj.hit(self)
            if dist != None and obj.castShadows():
                return True
        return False
             
if __name__ == "__main__":
    r = Ray((2,0,0),(-1,0,0))
    print r
