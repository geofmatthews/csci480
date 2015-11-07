# Lots of objects

import os,sys

from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram

import pygame
from pygame.locals import *
import numpy as N

sys.path.insert(0, os.path.join("..","utilities"))
from psurfaces import torus, sphere
from polyhedra import tetrahedron
from transforms import *
from loadtexture import loadTexture
from camera import Camera
from meshes import coloredMesh

def readShader(filename):
    with open(os.path.join("..","shaders", filename)) as fp:
        return fp.read()

def makeShader(vertfile, fragfile):
    return compileProgram(
        compileShader(readShader(vertfile), GL_VERTEX_SHADER),
        compileShader(readShader(fragfile), GL_FRAGMENT_SHADER)
        )

def initializeVAO():
    n = 1
    vaoArray = N.zeros(n, dtype=N.uint)
    vaoArray = glGenVertexArrays(n)
    glBindVertexArray( vaoArray )

# Called once at application start-up.
# Must be called after we have an OpenGL context, i.e. after the pygame
# window is created
def init():
    global theMeshes, theLight, theCamera, theScreen
    initializeVAO()
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    # Add our objects
    # LIGHT
    theLight = N.array((0.577, 0.577, 0.577, 0.0),dtype=N.float32)
    # OBJECTS
    theMeshes = []
    phongshader = makeShader("phongshader.vert","phongshader.frag")
    for i in range(100):
        if i % 3 == 0:
            major = N.random.random()*2
            minor = major*0.25
            verts = torus(major, minor, 32, 8)
        elif i % 3 == 1:
            radius = N.random.random()*2
            verts = sphere(radius, 32, 16)
        else:
            size = N.random.random()*4
            verts = tetrahedron(size)            
        newmesh = coloredMesh(N.array((N.random.random(),
                                       N.random.random(),
                                       N.random.random(),
                                       1.0), dtype=N.float32),
                              verts,
                              phongshader)
        x = N.random.random()*20-10
        y = N.random.random()*20-10
        z = N.random.random()*20-10
        newmesh.moveRight(x)
        newmesh.moveUp(y)
        newmesh.moveBack(z)
        newmesh.pitch(x)
        newmesh.yaw(y)
        newmesh.roll(z)
        theMeshes.append(newmesh)
    # CAMERA
    width, height = theScreen.get_size()
    aspectRatio = float(width)/float(height)
    near = 0.01
    far = 100.0
    lens = 4.0  # "longer" lenses mean more telephoto
    theCamera = Camera(lens, near, far, aspectRatio)

# Called to redraw the contents of the window
def display(time):
    global theMesh, theLight, theCamera
    # Clear the display
    glClearColor(0.1, 0.2, 0.3, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)

    # Set the shader program
    for mesh in theMeshes:
        mesh.display(theCamera.view(),
                     theCamera.projection(),
                     N.dot(Yrot(time), theLight))

def main():
    global theCamera, theScreen
    
    pygame.init()
    pygame.mouse.set_cursor(*pygame.cursors.broken_x)

    width, height = 1024,768
    theScreen = pygame.display.set_mode((width, height), OPENGL|DOUBLEBUF)

    init()
    clock = pygame.time.Clock()
    time = 0.0
    while True:
        clock.tick(30)
        time += 0.01
        # Event queued input
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYUP and event.key == K_ESCAPE:
                return
        # Polling input is better for a real time camera
        pressed = pygame.key.get_pressed()

        # keys for zoom:
        if pressed[K_z]:
            theCamera.zoomIn(1.015)
        if pressed[K_x]:
            theCamera.zoomOut(1.015)

        # arrow keys for movement:
        movespeed = 0.05
        if pressed[K_LSHIFT]:
            movespeed *= 4
        if pressed[K_d] | pressed[K_RIGHT]:
            theCamera.moveRight(movespeed)
        if pressed[K_a] | pressed[K_LEFT]:
            theCamera.moveRight(-movespeed)
        if pressed[K_w] | pressed[K_UP]:
            theCamera.moveBack(-movespeed)
        if pressed[K_s] | pressed[K_DOWN]:
            theCamera.moveBack(movespeed)
        # mouse for rotation
        rotspeed = 0.1
        mousespeed = 0.5*rotspeed
        x,y = pygame.mouse.get_pos()
        if (x > 0) & (y > 0):
            xDisplacement = x - 0.5*width
            yDisplacement = y - 0.5*height
            # normalize:
            xNormed = xDisplacement/width
            yNormed = -yDisplacement/height
            newx = int(x - xDisplacement*mousespeed)
            newy = int(y - yDisplacement*mousespeed)
            if (newx != x) | (newy != y):
                theCamera.pan(-xNormed * rotspeed)
                theCamera.tilt(-yNormed * rotspeed)
                pygame.mouse.set_pos((newx,newy))

        display(time)
        pygame.display.flip()

if __name__ == '__main__':
    try:
        main()
    except RuntimeError, err:
        for s in err:
            print s
        raise RuntimeError(err)
    finally:
        pygame.quit()

