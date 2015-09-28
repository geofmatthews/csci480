
import numpy as N
from transforms import *

def pSurface(point, normal, tangent, texture, srange, trange):
    sinc = srange[1] - srange[0]
    tinc = trange[1] - trange[0]
    verts = []
    for s in srange:
        for t in trange:
            p00 = point(s,t)            
            n00 = normal(s,t)
            t00 = tangent(s,t)
            b00 = list(N.cross(vec(n00[0:3]), vec(t00[0:3]))) + [0]
            uv00 = texture(s,t)           
            verts.extend(p00+n00+t00+b00+uv00)
    jump = len(trange)
    indices = []
    for row in range(len(srange)-1):
        for col in range(len(trange)-1):
            index = row*jump + col
            i00 = index
            i01 = index+1
            i10 = index+jump
            i11 = index+jump+1
            indices.extend([i00,i10,i01,i10,i11,i01])
    return (N.array(verts, dtype=N.float32),
            N.array(indices,dtype=N.uint16))

def rectangle(width, height, xblocks, yblocks):
    sinc = width/xblocks
    tinc = height/yblocks
    srange = N.arange(0,width+sinc,sinc)
    trange = N.arange(0,height+tinc,tinc)
    texture = lambda s,t: [s/width,t/height]
    point = lambda s,t: [s,t,0,1]
    normal = lambda s,t: [0,0,1,0]
    tangent = lambda s,t: [1,0,0,0]
    return pSurface(point, normal, tangent, texture, srange, trange)

def arrowPoint(length,  s, t):
    x = length *  [0.0,  0.8,  0.8,  1.0][s]
    y = [0.04, 0.04, 0.08, 0.0][s]
    z = [0.04, 0.04, 0.08, 0.0][s]
    if t == 1:
        z *= -1
    elif t == 2:
        y *= -1
        z *= -1
    elif t == 3:
        y *= -1
    return [x,y,z,1]

def arrowNormal(length, s, t):
    r2 = N.sqrt(2.0)
    if t == 0:
        return [0,r2,r2,0]
    elif t == 1:
        return [0,-r2,r2,0]
    elif t == 2:
        return [0,-r2,-r2,0]
    else:
        return [0, r2,-r2,0]

def arrowTangent(length, s, t):
    return [1,0,0,0]

def arrow(length=1):
    return pSurface(lambda s,t:arrowPoint(length,  s, t),
                    lambda s,t:arrowNormal(length,  s, t),
                    lambda s,t:arrowTangent(length,  s, t),
                    lambda s,t:[s,t],
                    range(4), range(5))

def spherePoint(radius, longangle, latangle):
    clat = N.cos(latangle)
    slat = N.sin(latangle)
    clong = N.cos(longangle)
    slong = N.sin(longangle)
    x = radius*clong*clat
    y = radius*slat
    z = -radius*slong*clat
    return [x,y,z,1.0] # return homogeneous point

def sphereNormal(radius, longangle, latangle):
    x,y,z,w = spherePoint(radius, longangle, latangle)
    norm = normalize((x,y,z))
    return [norm[0],norm[1],norm[2], 0.0] # return homogeneous vector

def sphereTangent(radius, longangle, latangle):
    clong = N.cos(longangle)
    slong = N.sin(longangle)
    return [-slong, 0, -clong, 0]

def sphereTexture(radius, longangle, latangle):
    return [0.5*longangle/N.pi, latangle/N.pi+0.5]

def sphere(radius, nlongs, nlats):
    # remember to include the extra step in the ranges:
    sinc = 2.0*N.pi/nlongs
    srange = N.arange(0.0, 2.0*N.pi+sinc, sinc)
    tinc = N.pi/nlats
    trange = N.arange(-0.5*N.pi, 0.5*N.pi+tinc, tinc)
    return pSurface(lambda s,t:spherePoint(radius,s,t),
                    lambda s,t:sphereNormal(radius,s,t),
                    lambda s,t:sphereTangent(radius,s,t),
                    lambda s,t:sphereTexture(radius,s,t),
                    srange, trange)

def saddlePoint(s, t):
    return [s, t, s*s - t*t, 1]

def saddleTangent(s, t):
    v = normalize(vec((1,0,2*s)))
    return [v[0], v[1], v[2], 0]

def saddleBitangent(s, t):
    v = normalize(vec((0, 1, -2*t)))
    return [v[0], v[1], v[2], 0]

def saddleNormal(s, t):
    tan = normalize(vec((1, 0, 2*s)))
    bitan = normalize(vec((0, 1, -2*t)))
    norm = N.cross(tan, bitan)
    return [norm[0], norm[1], norm[2], 0]

def saddleTexture(s, t):
    return [s, t]

def saddle(srange, trange):
    return pSurface(saddlePoint,
                    saddleNormal,
                    saddleTangent,
                    saddleTexture,
                    srange, trange);

if __name__ == "__main__":
    v,i = sphere(1, 4, 2)
    print N.round(v)
