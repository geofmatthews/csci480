
import numpy as N

def lerp(a,b,pct):
    return (1.0-pct)*a + pct*b

def makeVector(x, y=None, z=None, w = None):
    if y != None and z != None and w != None:
        return N.array((x,y,z,w), dtype=float)
    elif y != None and z != None:
        return N.array((x,y,z), dtype=float)
    elif y != None:
        return N.array((x,y), dtype=float)
    else:
        return N.array(x, dtype=float)

def magnitude(v):
    return N.sqrt(N.dot(v,v))

def normalize(v):
    mag = magnitude(v)
    if mag == 0.0:
        return makeVector(1,0,0,0)
    else:
        return v/mag

def clamp(vec, lo, hi):
    return N.clip(vec, lo, hi)

def cross(a,b):
    aa = a[0:3]
    bb = b[0:3]
    cc = N.cross(aa,bb)
    dd = makeVector(0,0,0,0)
    dd[0:3] = cc
    return dd
    
def posDot(v,w):
    dot = N.dot(v,w)
    return max(0.0, dot)

def identity():
    return N.array(((1,0,0,0),
                    (0,1,0,0),
                    (0,0,1,0),
                    (0,0,0,1)), dtype=float)

if __name__ == "__main__":
    v = makeVector
    print N.dot(identity(), v(1,2,3,4))
    print N.dot(v(1,2,3,4), v(4,3,2,1))
    print clamp(v((0,1,2,3)), 0.5, 2.5)
    print magnitude(normalize(v(1,1,1,1)))
    print cross(v(1,0,0,0), v(0,1,0,0))
    
