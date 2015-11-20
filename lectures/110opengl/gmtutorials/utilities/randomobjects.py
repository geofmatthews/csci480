
import os,sys

from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram

import numpy as N

sys.path.insert(0, os.path.join("..","utilities"))
from psurfaces import torus, sphere
from polyhedra import tetrahedron
from obj import readOBJ
from meshes import *

def readShader(filename):
    with open(os.path.join("..","shaders", filename)) as fp:
        return fp.read()

def makeShader(vertfile, fragfile):
    return compileProgram(
        compileShader(readShader(vertfile), GL_VERTEX_SHADER),
        compileShader(readShader(fragfile), GL_FRAGMENT_SHADER)
        )

def makeObjects(n=32, area = 20):
    theMeshes = []
    phongshader = makeShader("phongshader.vert","phongshader.frag")
    verts, elements = torus(1,0.25,64,16)
    torusVerts = getArrayBuffer(verts)
    torusElements = getElementBuffer(elements)
    torusNum = len(elements)
    verts, elements = sphere(1,64,32)
    sphereVerts = getArrayBuffer(verts)
    sphereElements = getArrayBuffer(elements)
    sphereNum = len(elements)
    verts, elements = tetrahedron(2)
    tetraVerts = getArrayBuffer(verts)
    tetraElements = getElementBuffer(elements)
    tetraNum = len(elements)
    verts, elements = readOBJ("suzanne.obj")
    suzanneVerts = getArrayBuffer(verts)
    suzanneElements = getElementBuffer(elements)
    suzanneNum = len(elements)
    for i in range(n):
        if i % 4 == 0:
            verts, elements, num = torusVerts, torusElements, torusNum
        elif i % 4 == 1:
            verts,elements, num = sphereVerts, sphereElements, torusNum
        elif i % 4 == 2:
            verts, elements, num = suzanneVerts, suzanneElements, torusNum
        else:
            verts, elements = tetraVerts, tetraElements
        newmesh = coloredMesh(N.array((N.random.random(),
                                       N.random.random(),
                                       N.random.random(),
                                       1.0), dtype=N.float32),
                              verts,
                              elements,
                              num,
                              phongshader)
        x = N.random.random()*area - 0.5*area
        y = N.random.random()*area - 0.5*area
        z = N.random.random()*area - 0.5*area
        newmesh.moveRight(x)
        newmesh.moveUp(y)
        newmesh.moveBack(z)
        newmesh.pitch(x)
        newmesh.yaw(y)
        newmesh.roll(z)
        theMeshes.append(newmesh)
    return theMeshes
