
import numpy as N
from vectors import *

def identity():
    return N.array(((1,0,0,0),
                    (0,1,0,0),
                    (0,0,1,0),
                    (0,0,0,1)), dtype=float)

def translation(x,y,z):
    return N.array(((1,0,0,x),
                    (0,1,0,y),
                    (0,0,1,z),
                    (0,0,0,1)), dtype=float)

def scale(x,y,z):
    return N.array(((x,0,0,0),
                    (0,y,0,0),
                    (0,0,z,0),
                    (0,0,0,1)),dtype=float)

def scaleU(x):
    return scale(x,x,x)

def rotationZ(angle):
    sina = N.sin(angle)
    cosa = N.cos(angle)
    return N.array(((cosa, -sina,    0, 0),
                    (sina,  cosa,    0, 0),
                    (0   ,     0,    1, 0),
                    (0   ,     0,    0, 1)), dtype=float)

def rotationY(angle):
    sina = N.sin(angle)
    cosa = N.cos(angle)
    return N.array(((cosa,     0, -sina, 0),
                    (0   ,     1,     0, 0),
                    (sina,     0,  cosa, 0),
                    (0   ,     0,     0, 1)), dtype=float)

def rotationX(angle):
    sina = N.sin(angle)
    cosa = N.cos(angle)
    return N.array(((    1,    0,     0, 0),
                    (    0, cosa, -sina, 0),
                    (    0, sina,  cosa, 0),
                    (    0,     0,    0, 1)), dtype=float)

def rotationAxis(angle, axis):
    sina = N.sin(angle)
    cosa = N.cos(angle)
    cosa1 = 1.0 - cosa
    x,y,z,w = normalize(axis)
    return N.array(((   cosa+x*x*cosa1, x*y*cosa1-z*sina,  y*sina+x*z*cosa1, 0),
                    ( z*sina+x*y*cosa1,   cosa+y*y*cosa1, -x*sina+y*z*cosa1, 0),
                    (-y*sina+x*z*cosa1, x*sina+y*z*cosa1,    cosa+z*z*cosa1, 0),
                    (                0,                0,                 0, 1)))


if __name__ == "__main__":
    x = makeVector((1,0,0,0))
    y = makeVector((0,1,0,0))
    z = makeVector((0,0,1,0))
    o = makeVector((0,0,0,1))

    T = translation(2,3,4)
    R1 = rotationX(N.pi/4.0)
    R2 = rotationY(N.pi/4.0)

    bigT = N.dot(T, N.dot(R2, R1))

    print bigT
    print N.dot(bigT,x)
    print N.dot(bigT,y)
    print N.dot(bigT,z)
    print N.dot(bigT,o)
    
