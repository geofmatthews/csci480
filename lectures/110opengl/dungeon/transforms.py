import numpy as N

def projectionMatrix(n,f,w,h):
    return N.array(((2.0*n/w, 0, 0, 0),
                    (0, 2.0*n/h, 0, 0),
                    (0, 0, -(f+n)/(f-n), -2.0*f*n/(f-n)),
                    (0, 0, -1, 0)), dtype = N.float32)

def translationMatrix(x,y,z):
    return N.array(((1, 0, 0, x),
                    (0, 1, 0, y),
                    (0, 0, 1, z),
                    (0, 0, 0, 1)), dtype = N.float32)

def rotationXMatrix(angle):
    s = N.sin(angle)
    c = N.cos(angle)
    return N.array(((1.0, 0.0, 0.0, 0.0),
                    (0.0,   c,  -s, 0.0),
                    (0.0,   s,   c, 0.0),
                    (0.0, 0.0, 0.0, 1.0)), dtype = N.float32)
def rotationYMatrix(angle):
    s = N.sin(angle)
    c = N.cos(angle)
    return N.array(((  c, 0.0,  -s, 0.0),
                    (0.0, 1.0, 0.0, 0.0),
                    (  s, 0.0,   c, 0.0),
                    (0.0, 0.0, 0.0, 1.0)), dtype = N.float32)
def rotationZMatrix(angle):
    s = N.sin(angle)
    c = N.cos(angle)
    return N.array(((  c,  -s, 0.0, 0.0),
                    (  s,   c, 0.0, 0.0),
                    (0.0, 0.0, 1.0, 0.0),
                    (0.0, 0.0, 0.0, 1.0)), dtype = N.float32)
