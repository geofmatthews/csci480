import numpy as N


    
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
    return N.array(((  c, 0.0,  -s),
                    (0.0, 1.0, 0.0),
                    (  s, 0.0,   c), dtype = N.float32)
    
def rotationZMatrix(angle):
    s = N.sin(angle)
    c = N.cos(angle)
    return N.array(((  c,  -s, 0.0),
                    (  s,   c, 0.0),
                    (0.0, 0.0, 1.0), dtype = N.float32)


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
    
    

    

