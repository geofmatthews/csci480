
import numpy as N

def Xrot(ang):
    s = N.sin(ang)
    c = N.cos(ang)
    return N.array(((1, 0, 0, 0),
                    (0, c,-s, 0),
                    (0, s, c, 0),
                    (0, 0, 0, 1)), dtype=N.float32)

def Yrot(ang):
    s = N.sin(ang)
    c = N.cos(ang)
    return N.array(((c, 0,-s, 0),
                    (0, 1, 0, 0),
                    (s, 0, c, 0),
                    (0, 0, 0, 1)), dtype=N.float32)

def Zrot(ang):
    s = N.sin(ang)
    c = N.cos(ang)
    return N.array(((c,-s, 0, 0),
                    (s, c, 0, 0),
                    (0, 0, 1, 0),
                    (0, 0, 0, 1)), dtype=N.float32)

def translation(x,y,z):
    return N.array(((1,0,0,x),
                    (0,1,0,y),
                    (0,0,1,z),
                    (0,0,0,1)), dtype=N.float32)


def projection(n,f,r,t):
    return N.array((n/r, 0, 0, 0,
                    0, n/t, 0, 0,
                    0, 0, -(f+n)/(f-n), -2*f*n/(f-n),
                    0, 0, -1, 0), dtype=N.float32)

