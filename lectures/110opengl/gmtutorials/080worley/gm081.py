# Worley noise
# Two objects (not moving) so the continuous texture can be seen in world space

import os,sys

from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram

import pygame
from pygame.locals import *
import numpy as N

sys.path.insert(0, os.path.join("..","utilities"))
from psurfaces import *
from transforms import *
from loadtexture import loadTexture
from camera import Camera
from meshes import *

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
    worleyShader = makeShader("worley.vert", "worley.frag")
    torusVerts, torusElements = torus(10.0, 4.0, 128, 32)
    sphereVerts, sphereElements = sphere(8.0, 128, 32)
    theMeshes = [proceduralMesh(N.array((1.0,0.5,0.25,1.0),dtype=N.float32),
                                100.0,
                                getArrayBuffer(torusVerts),
                                getElementBuffer(torusElements),
                                len(torusElements),
                                worleyShader
                            ),
                 proceduralMesh(N.array((1.0,0.5,0.25,1.0),dtype=N.float32),
                                100.0,
                                getArrayBuffer(sphereVerts),
                                getArrayBuffer(sphereElements),
                                len(sphereElements),
                                worleyShader
                            )]
    theMeshes[1].moveUp(-10.0)
                 
    # CAMERA
    width, height = theScreen.get_size()
    aspectRatio = float(width)/float(height)
    near = 0.01
    far = 100.0
    lens = 4.0  # "longer" lenses mean more telephoto
    theCamera = Camera(lens, near, far, aspectRatio)
    theCamera.moveBack(50)

# Called to redraw the contents of the window
def display(time):
    global theMeshes, theLight, theCamera
    # Clear the display
    glClearColor(0.1, 0.2, 0.3, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)

    meshspeed = 0.0
    for theMesh in theMeshes:
        theMesh.pitch(meshspeed)
        theMesh.yaw(meshspeed)
        theMesh.roll(meshspeed)
        theMesh.display(theCamera.view(),
                        theCamera.projection(),
                        theLight)
        
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

