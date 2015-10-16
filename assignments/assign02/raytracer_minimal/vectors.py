
import numpy as N

def lerp(a,b,pct):
    return (1.0-pct)*a + pct*b

def vec(x, y=None, z=None):
    if y != None and z != None:
        return N.array((x,y,z), dtype=N.float32)
    else:
        return N.array(x, dtype=N.float32)

def magnitude(v):
    return N.sqrt(N.dot(v,v))

def normalize(v):
    mag = magnitude(v)
    if mag == 0.0:
        return vec(1,0,0)
    else:
        return v/mag
    
def reflect(v, normal):
    if N.dot(v, normal) < 0:
        normal = -normal
    scale = 2*N.dot(v, normal)
    return (scale*normal) - v

def clamp(v, lo, hi):
    v = [max(lo,x) for x in v]
    v = [min(hi,x) for x in v]
    return vec(v)

def posDot(v,w):
    dot = N.dot(v,w)
    return max(0.0, dot)

if __name__ == "__main__":
    print (clamp(vec((0,1,2,3)), 0.5, 2.5))
    print (reflect(vec(2,2,0), vec(0,1,0)))
    print (magnitude(normalize(vec(1,1,1))))
    
