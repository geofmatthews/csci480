
import numpy as N

# Module to create vertex arrays for polyhedra

# returns the vertex array with each vertex:
# x,y,z,1,    # position
# x,y,z,0,    # normal
# x,y,z,0,    # tangent
# x,y,z,0,    # bitangent = normal x tangent
# u,v,        # texture
# and the elements array 

def tetrahedron(size = 1.0):
    v0 = (0.35*size,  0.5*size, 0.0,      1.0)
    v1 = (0.35*size, -0.5*size, 0.0,      1.0)
    v2 = (-0.35*size, 0.0,      0.5*size, 1.0)
    v3 = (-0.35*size, 0.0,     -0.5*size, 1.0)
    
    n0 = ( 0.5,  0.0,    0.866, 0.0)
    t0 = ( 0.866,  0.0,   -0.5, 0.0)
    b0 = ( 0.000,  1.0,    0.000, 0.0)
    n1 = ( 0.5,  0.0,   -0.866, 0.0)
    t1 = (-0.707,  0.0,   -0.707, 0.0)
    b1 = ( 0.0,    1.0,    0.0,   0.0)
    n2 = (-0.866,  0.5,  0.0,   0.0)
    t2 = ( 0.0,    0.0,    1.0,   0.0)
    b2 = ( 0.5,  0.866,  0.0,   0.0)
    n3 = (-0.866, -0.5,  0.0,   0.0)
    t3 = ( 0.0,    0.0,    1.0,   0.0)
    b3 = (-0.5,  0.866,  0.0,   0.0)

    uvll = (0,0)
    uvlr = (1,0)
    uvul = (0,1)
    uvur = (1,1)

    verts = N.array(
        v0 + n0 + t0 + b0 + uvul +
        v2 + n0 + t0 + b0 + uvll +
        v1 + n0 + t0 + b0 + uvlr +
        v0 + n1 + t1 + b1 + uvul +
        v1 + n1 + t1 + b1 + uvlr +
        v3 + n1 + t1 + b1 + uvur +
        v0 + n2 + t2 + b2 + uvur +
        v3 + n2 + t2 + b2 + uvul +
        v2 + n2 + t2 + b2 + uvlr +
        v1 + n3 + t3 + b3 + uvll +
        v2 + n3 + t3 + b3 + uvlr +
        v3 + n3 + t3 + b3 + uvul, dtype=N.float32)

    indices = N.array((0,1,2,
                       3,4,5,
                       6,7,8,
                       9,10,11), dtype=N.float32)

    return (N.array(verts, dtype=N.float32),
            N.array(indices,dtype=N.uint16))

