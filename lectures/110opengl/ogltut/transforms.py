import numpy as N
from OpenGL.GLU import *

def vec(ns):
    return N.array(ns, dtype=N.float32)

def normalize(vec):
    vec = N.array(vec, dtype=N.float32)
    mag = N.sqrt(N.dot(vec,vec))
    return vec/mag

def newMatrix():
    return N.zeros((4,4),dtype=N.float32)

def setMatrix(m1, m2):
    m1[:,:] = m2

def projectionMatrix(n,f,w,h):
    return N.array(((2.0*n/w, 0, 0, 0),
                    (0, 2.0*n/h, 0, 0),
                    (0, 0, -(f+n)/(f-n), -2.0*f*n/(f-n)),
                    (0, 0, -1, 0)), dtype = N.float32)

def setProjection(m,n,f,w,h):
    m[:,:] = 0.0
    m[0,0] = 2.0*n/w
    m[1,1] = 2.0*n/h
    m[2,2] = -(f+n)/(f-n)
    m[2,3] = -2.0*f*n/(f-n)
    m[3,2] = -1.0

def perspective(fovy, ar, n, f):
    h = 2.0*n*N.tan(0.5*N.pi*fovy/180.0)
    w = ar*h
    return projectionMatrix(n, f, w, h)

def lookAt(cameraAt, lookAt, up):
    cameraAt = vec(cameraAt)
    trans = N.identity(4,dtype=N.float32)
    trans[0:3,3] = -cameraAt
    lookAt = vec(lookAt)
    fwd = normalize(lookAt - cameraAt)
    up = normalize(up)
    up = up - N.dot(up,fwd)*fwd
    rt = normalize(N.cross(fwd, up))
    rot = N.identity(4, dtype=N.float32)
    rot[0,0:3] = rt
    rot[1,0:3] = up
    rot[2,0:3] = -fwd
    return N.dot(rot, trans)

def viewFromFrame(pos, fwd, rt, up):
    # quick inverse of translation+rotation
    trans = N.identity(4,dtype=N.float32)
    trans[0:3,3] = -pos[0:3]
    rot = N.identity(4,dtype=N.float32)
    rot[0,0:3] = rt[0:3]
    rot[1,0:3] = up[0:3]
    rot[2,0:3] = -fwd[0:3]
    return N.dot(rot, trans)

def modelFromFrame(pos, fwd, rt, up):
    # translation+rotation
    model = N.identity(4,dtype=N.float32)
    model[0:3,3] = pos[0:3]
    model[0:3,0] = rt[0:3]
    model[0:3,1] = up[0:3]
    model[0:3,2] = -fwd[0:3]
    return model
def translationMatrix(x,y,z):
    return N.array(((1, 0, 0, x),
                    (0, 1, 0, y),
                    (0, 0, 1, z),
                    (0, 0, 0, 1)), dtype = N.float32)

def setTranslation(m,x,y,z):
    m[:,:] = N.eye(4, dtype=N.float32)
    m[:,3] = (x,y,z,1)
    
def rotationXMatrix(angle):
    s = N.sin(angle)
    c = N.cos(angle)
    return N.array(((1.0, 0.0, 0.0, 0.0),
                    (0.0,   c,  -s, 0.0),
                    (0.0,   s,   c, 0.0),
                    (0.0, 0.0, 0.0, 1.0)), dtype = N.float32)

def setRotationX(m,angle):
    s = N.sin(angle)
    c = N.cos(angle)
    m[:,:] = N.eye(4, dtype=N.float32)
    m[1,1] = c
    m[2,2] = c
    m[1,2] = -s
    m[2,1] = s

def rotationYMatrix(angle):
    s = N.sin(angle)
    c = N.cos(angle)
    return N.array(((  c, 0.0,  -s, 0.0),
                    (0.0, 1.0, 0.0, 0.0),
                    (  s, 0.0,   c, 0.0),
                    (0.0, 0.0, 0.0, 1.0)), dtype = N.float32)

def setRotationY(m,angle):
    s = N.sin(angle)
    c = N.cos(angle)
    m[:,:] = N.eye(4, dtype=N.float32)
    m[0,0] = c
    m[2,2] = c
    m[0,2] = -s
    m[2,0] = s
    
def rotationZMatrix(angle):
    s = N.sin(angle)
    c = N.cos(angle)
    return N.array(((  c,  -s, 0.0, 0.0),
                    (  s,   c, 0.0, 0.0),
                    (0.0, 0.0, 1.0, 0.0),
                    (0.0, 0.0, 0.0, 1.0)), dtype = N.float32)


def setRotationZ(m,angle):
    s = N.sin(angle)
    c = N.cos(angle)
    m[:,:] = N.eye(4, dtype=N.float32)
    m[0,0] = c
    m[1,1] = c
    m[0,1] = -s
    m[1,0] = s

if __name__ == '__main__':
    m = N.identity(4)
    rx = rotationXMatrix(N.pi*45.0/180.0)
    ry = rotationYMatrix(N.pi*45.0/180.0)
    rz = rotationZMatrix(N.pi*45.0/180.0)

    print rx
    print ry
    print rz
    print N.dot(ry, rx)
    print N.dot(rz, N.dot(ry,rx))
    
    

    

