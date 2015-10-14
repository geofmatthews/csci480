
import numpy as N
from transforms import *

def pSurface(point, normal, texture, srange, trange):
    sinc = srange[1] - srange[0]
    tinc = trange[1] - trange[0]
    verts = []
    for s in srange:
        for t in trange:
            p00 = point(s,t)
            p01 = point(s,t+tinc)
            p10 = point(s+sinc, t)
            p11 = point(s+sinc, t+tinc)
            
            n00 = normal(s,t)
            n01 = normal(s,t+tinc)
            n10 = normal(s+sinc, t)
            n11 = normal(s+sinc, t+tinc)
            
            t00 = texture(s,t)
            t01 = texture(s,t+tinc)
            t10 = texture(s+sinc, t)
            t11 = texture(s+sinc, t+tinc)
            
            verts.extend(p00+n00+t00)
            verts.extend(p10+n10+t10)
            verts.extend(p01+n01+t01)

            verts.extend(p10+n10+t10)
            verts.extend(p11+n11+t11)
            verts.extend(p01+n01+t01)
    return N.array(verts, dtype=N.float32)

def triangle():
    return N.array([-1,-1,0,1,
                    0,0,1,0,
                    0,0,
                    1,-1,0,1,
                    0,0,1,0,
                    1,0,
                    0,1,0,1,
                    0,0,1,0,
                    .5,1], dtype=N.float32)

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

def sphereTexture(radius, longangle, latangle):
    return [0.5*longangle/N.pi, 0.5*latangle/N.pi]

def sphere(radius, nlongs, nlats):
    sinc = 2.0*N.pi/nlongs
    srange = N.arange(0.0, 2.0*N.pi, sinc)
    tinc = N.pi/nlats
    trange = N.arange(-0.5*N.pi, 0.5*N.pi, tinc)
    return pSurface(lambda s,t:spherePoint(radius,s,t),
                    lambda s,t:sphereNormal(radius,s,t),
                    lambda s,t:sphereTexture(radius,s,t),
                    srange, trange)
        
