
import numpy as N

# Module to create vertex arrays for parametric surfaces.
# point is a function(s,t) -> (x,y,z,1)
# normal is a function(s,t) -> (x,y,z,0)
# tangent is a function(s,t) -> (x,y,z,0)
# binormal is computed assuming normal and tangent are orthonormal
# texture is a function(s,t) -> (u,v)
# s and t use N.linspace to generate num points min <= x <= max

# returns the vertex array with each vertex:
# x,y,z,1,    # position
# x,y,z,0,    # normal
# x,y,z,0,    # tangent
# x,y,z,0,    # binormal = normal x tangent
# u,v,        # texture
# and the elements array with each quad forming two
# triangles with correct winding
def pSurface(point, normal, tangent, 
             texture, smin, smax, snum, tmin, tmax, tnum):
    verts = []
    for s in N.linspace(smin, smax, snum):
        for t in N.linspace(tmin, tmax, tnum):
            p00 = point(s,t)            
            n00 = normal(s,t)
            t00 = tangent(s,t)
            b00 = list(N.cross(N.array(n00[0:3],dtype=N.float32), 
                               N.array(t00[0:3],dtype=N.float32))) + [0]
            uv00 = texture(s,t)           
            verts.extend(p00+n00+t00+b00+uv00)
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

def sphereTangent(longangle, latangle):
    clong = N.cos(longangle)
    slong = N.sin(longangle)
    return [-slong, 0, -clong, 0]

def sphereTexture(longangle, latangle):
    return [0.5*longangle/N.pi, latangle/N.pi+0.5]

def sphere(radius, nlongs, nlats):
    twopi = 2.0*N.pi
    halfpi = 0.5*N.pi
    return pSurface(lambda s,t:spherePoint(radius,s,t),
                    sphereNormal,
                    sphereTangent,
                    sphereTexture,
                    0.0, twopi, nlongs,
                    -halfpi, halfpi, nlats)
        
def torusPoint(majorRadius, minorRadius, s, t):
    clong = N.cos(s)
    slong = N.sin(s)
    clat = N.cos(t)
    slat = N.sin(t)
    # find point on major circle:
    mcp = majorRadius * N.array((clong, slong, 0.0), dtype=N.float32)
    # find curve normal
    n = N.array((clong, slong, 0.0), dtype=N.float32)
    # find curve binormal
    b = N.array((0.0, 0.0, 1.0), dtype=N.float32)
    # find point on torus
    p = mcp + minorRadius*clat*n + minorRadius*slat*b
    # return homogeneous point
    return list(p) + [1.0] 

def torusNormal(s, t):
    clong = N.cos(s)
    slong = N.sin(s)
    clat = N.cos(t)
    slat = N.sin(t)
    # find curve normal
    n = N.array((clong, slong, 0.0), dtype=N.float32)
    # find curve binormal
    b = N.array((0.0, 0.0, 1.0), dtype=N.float32)
    # find vector
    v = clat*n + slat*b
    v /= N.linalg.norm(v)
    return list(v) + [0.0]

def torusTangent(s, t):
    clong = N.cos(t)
    slong = N.sin(t)
    v = [-slong, clong, 0.0, 0.0]
    return v

def torusTexture(s, t):
    return [0.5*0.5*s/N.pi,0.25*0.5*t/N.pi]    

def torus(majorRadius, minorRadius, nlongs, nlats):
    twopi = 2.0*N.pi
    return pSurface(lambda s,t:torusPoint(majorRadius, minorRadius, s, t),
                    torusNormal,
                    torusTangent,
                    torusTexture,
                    0.0, twopi, nlongs,
                    0.0, twopi, nlats)

if __name__ == "__main__":
    s = sphere(1.0, 2, 2)
    for i in range(0,len(s[0]-1),18):
        for j in range(i,i+4):
            print s[0][j],
        print
        for j in range(i+4, i+8):
            print s[0][j],
        print
        for j in range(i+8, i+12):
            print s[0][j],
        print
        for j in range(i+12, i+16):
            print s[0][j],
        print
        for j in range(i+16, i+18):
            print s[0][j],
        print
    print "Vertices:", len(s[0])/18
    print "Triangles:", len(s[1])/3
