
import numpy as N

# Module to create vertex arrays for miscellaneous stuff

# returns the vertex array with each vertex:
# x,y,z,1,    # position
# x,y,z,0,    # normal
# x,y,z,0,    # tangent
# x,y,z,0,    # bitangent = normal x tangent
# u,v,        # texture
# and the elements array 

def rectangle(width, height):
    """Returns a rectangle in the x-y plane facing +z"""
    halfwidth = width*0.5
    halfheight = height*0.5
    v00 = (-halfwidth, -halfheight, 0, 1)
    v01 = (-halfwidth, halfheight, 0, 1)
    v10 = (halfwidth, -halfheight, 0, 1)
    v11 = (halfwidth, halfheight, 0, 1)
    n = (0,0,1,0)
    t = (1,0,0,0)
    b = (0,1,0,0)

    verts = N.array(
        v00 + n + t + b + (0,0) +
        v11 + n + t + b + (1,1) +
        v01 + n + t + b + (0,1) +
        v00 + n + t + b + (0,0) +
        v10 + n + t + b + (1,0) +
        v11 + n + t + b + (1,1) ,
        dtype=N.float32)

    indices = N.array((0,1,2,
                       3,4,5), dtype=N.float32)

    return (N.array(verts, dtype=N.float32),
            N.array(indices,dtype=N.uint16))

