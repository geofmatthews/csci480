
import numpy as N
from transforms import *

def pSurface(point, normal, texture, srange, trange):
    sinc = srange[1] - srange[0]
    tinc = trange[1] - trange[0]
    verts = []
    for s in srange:
        for t in trange:
            p00 = point(s,t)            
            n00 = normal(s,t)            
            t00 = texture(s,t)           
            verts.extend(p00+n00+t00)
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
    return pSurface(point, normal, texture, srange, trange)

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
    return [0.5*longangle/N.pi, latangle/N.pi+0.5]

def sphere(radius, nlongs, nlats):
    # remember to include the extra step in the ranges:
    sinc = 2.0*N.pi/nlongs
    srange = N.arange(0.0, 2.0*N.pi+sinc, sinc)
    tinc = N.pi/nlats
    trange = N.arange(-0.5*N.pi, 0.5*N.pi+tinc, tinc)
    return pSurface(lambda s,t:spherePoint(radius,s,t),
                    lambda s,t:sphereNormal(radius,s,t),
                    lambda s,t:sphereTexture(radius,s,t),
                    srange, trange)
        
