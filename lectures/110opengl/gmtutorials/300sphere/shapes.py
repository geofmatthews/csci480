
import numpy as N

# Module to create vertex arrays for parametric surfaces.
# point is a function(s,t) -> (x,y,z,1)
# normal is a function(s,t) -> (x,y,z,0)
# texture is a function(s,t) -> (u,v)
# s and t use N.arange to generate points min <= x < max

# returns the vertex array with each vertex:
# x,y,z,1,    # position
# x,y,z,0,    # normal
# u,v,        # texture
# and the elements array with each quad forming two
# triangles with correct winding
def pSurface(point, normal, texture, smin, smax, snum, tmin, tmax, tnum):
    verts = []
    for s in N.linspace(smin, smax, snum):
        for t in N.linspace(tmin, tmax, tnum):
            p00 = point(s,t)            
            n00 = normal(s,t)            
            t00 = texture(s,t)           
            verts.extend(p00+n00+t00)
    jump = tnum
    indices = []
    for row in range(snum-1):
        for col in range(tnum-1):
            index = row*jump + col
            i00 = index
            i01 = index+1
            i10 = index+jump
            i11 = index+jump+1
            indices.extend([i00,i10,i01,i10,i11,i01])
    return (N.array(verts, dtype=N.float32),
            N.array(indices,dtype=N.uint16))

# Example using a sphere
def spherePoint(radius, longangle, latangle):
    clat = N.cos(latangle)
    slat = N.sin(latangle)
    clong = N.cos(longangle)
    slong = N.sin(longangle)
    x = radius*clong*clat
    y = radius*slat
    z = -radius*slong*clat
    return [x,y,z,1.0] # return homogeneous point

def sphereNormal(longangle, latangle):
    norm = spherePoint(1.0, longangle, latangle)
    norm[3] = 0.0
    return norm # return homogeneous vector

def sphereTexture(longangle, latangle):
    return [0.5*longangle/N.pi, latangle/N.pi+0.5]

def sphere(radius, nlongs, nlats):
    # remember to include the extra step in the ranges:
    twopi = 2.0*N.pi
    halfpi = 0.5*N.pi
    return pSurface(lambda s,t:spherePoint(radius,s,t),
                    sphereNormal,
                    sphereTexture,
                    0.0, twopi, nlongs,
                    -halfpi, halfpi, nlats)
        
