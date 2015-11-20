# Skybox without reflection
# Box stays centered on the camera by not using the view transform
# on the box.

import os,sys

from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram

import pygame
from pygame.locals import *
import numpy as N

sys.path.insert(0, os.path.join("..","utilities"))
from psurfaces import *
from polyhedra import *
from specials import rectangle
from obj import readOBJ
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
    global theMeshes, theBox, theLight, theCamera, theScreen, theTextures
    initializeVAO()
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    # Add our objects
    # OBJECTS
    theMeshes = []
    phongshader = makeShader("phong.vert","phong.frag")
    for i in range(16):
        if i % 4 == 0:
            major = N.random.random()*2
            minor = major*0.25
            verts,elements = torus(major, minor, 64, 16)
        elif i % 4 == 1:
            radius = N.random.random()*2
            verts,elements = sphere(radius, 64, 32)
        elif i % 4 == 2:
            verts,elements = readOBJ("suzanne.obj")
        else:
            size = N.random.random()*4
            verts,elements = tetrahedron(size)            
        newmesh = coloredMesh(N.array((N.random.random(),
                                       N.random.random(),
                                       N.random.random(),
                                       1.0), dtype=N.float32),
                              getArrayBuffer(verts),
                              getElementBuffer(elements),
                              len(elements),
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
    # LIGHT
    # put the light in a direction to agree with the skybox
    theLight = N.array((0.707, 0.707, 0.0, 0.0),dtype=N.float32)
    # TEXTURES
    theTextures = []
    images = ["figposx.png",
              "fignegx.png",
              "figposy.png",
              "fignegy.png",
              "figposz.png",
              "fignegz.png"]
    theTextures.append( [loadTexture(img,
                                     magFilter=GL_LINEAR,
                                     wrapMode=GL_CLAMP_TO_EDGE)
                         for img in images] )
    images = ["terragenposx.png",
              "terragennegx.png",
              "terragenposy.png",
              "terragennegy.png",
              "terragenposz.png",
              "terragennegz.png"]
    theTextures.append( [loadTexture(img,
                                     magFilter=GL_LINEAR,
                                     wrapMode=GL_CLAMP_TO_EDGE)
                         for img in images] )
    # these images have Z backwards from opengl
    images = ["goldengateposx.jpg",
              "goldengatenegx.jpg",
              "goldengateposy.jpg",
              "goldengatenegy.jpg",
              "goldengatenegz.jpg",
              "goldengateposz.jpg"]
    theTextures.append( [loadTexture(img,
                                     magFilter=GL_LINEAR,
                                     wrapMode=GL_CLAMP_TO_EDGE)
                         for img in images] )
    # these images have X backwards from opengl
    images = ["lancellottiposx.jpg",
              "lancellottinegx.jpg",
              "lancellottiposy.jpg",
              "lancellottinegy.jpg",
              "lancellottinegz.jpg",
              "lancellottiposz.jpg"]
    theTextures.append( [loadTexture(img,
                                     magFilter=GL_LINEAR,
                                     wrapMode=GL_CLAMP_TO_EDGE)
                         for img in images] )
    
    # SKYBOX
    boxsize = 1.0
    skyboxShader = makeShader("flattextured.vert","flattextured.frag")
    verts,elements = rectangle(boxsize,boxsize)
    vertBuff = getArrayBuffer(verts)
    elemBuff = getElementBuffer(elements)
    numElem = len(elements)
    posx = flatTexturedMesh(theTextures[0][0],
                            vertBuff,
                            elemBuff,
                            numElem,
                            skyboxShader,
                            N.array((1.0,1.0),dtype=N.float32))
    negx = flatTexturedMesh(theTextures[0][1],
                            vertBuff,
                            elemBuff,
                            numElem,
                            skyboxShader,
                            N.array((1.0,1.0),dtype=N.float32))
    posy = flatTexturedMesh(theTextures[0][2],
                            vertBuff,
                            elemBuff,
                            numElem,
                            skyboxShader,
                            N.array((1.0,1.0),dtype=N.float32))
    negy = flatTexturedMesh(theTextures[0][3],
                            vertBuff,
                            elemBuff,
                            numElem,
                            skyboxShader,
                            N.array((1.0,1.0),dtype=N.float32))
    posz =  flatTexturedMesh(theTextures[0][4],
                            vertBuff,
                            elemBuff,
                            numElem,
                             skyboxShader,
                             N.array((1.0,1.0),dtype=N.float32))
    negz =  flatTexturedMesh(theTextures[0][5],
                            vertBuff,
                            elemBuff,
                            numElem,
                             skyboxShader,
                             N.array((1.0,1.0),dtype=N.float32))

    backDistance = -boxsize*0.5

    posx.yaw(-1)
    posx.yaw(-1)
    posx.moveBack(backDistance)

    negx.yaw(1)
    negx.yaw(1)
    negx.moveBack(backDistance)

    for i in range(2):
        posy.pitch(-1)
    posy.moveBack(backDistance)

    for i in range(2):
        negy.pitch(1)
    negy.moveBack(backDistance)

    for i in range(4):
        posz.yaw(1)
    posz.moveBack(backDistance)

    negz.moveBack(backDistance)

    theBox = [posx, negx, posy, negy, posz, negz]

    # CAMERA
    width, height = theScreen.get_size()
    aspectRatio = float(width)/float(height)
    near = 0.01
    far = 1000.0
    lens = 2.0  # A wide lens will minimize pixels in the background
    theCamera = Camera(lens, near, far, aspectRatio)
    theCamera.moveBack(10)

# Called to redraw the contents of the window
def display(time):
    global theMeshes, theBox, theLight, theCamera
    # Clear the display
    glClearColor(0.1, 0.2, 0.3, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)

    glDisable(GL_DEPTH_TEST)
    for mesh in theBox:
        mesh.display(theCamera.onlyRotation(),
                     theCamera.projection(),
                     None)
    glEnable(GL_DEPTH_TEST)
    # display the meshes
    meshSpeed = 0.025
    for mesh in theMeshes:
        mesh.yaw(meshSpeed)
        mesh.pitch(meshSpeed)
        mesh.roll(meshSpeed)
        mesh.display(theCamera.view(),
                     theCamera.projection(),
                     theLight)
        
def main():
    global theCamera, theScreen, theTextures
    
    pygame.init()
    pygame.mouse.set_cursor(*pygame.cursors.broken_x)

    width, height = 1024,768
    theScreen = pygame.display.set_mode((width, height), OPENGL|DOUBLEBUF)

    init()
    clock = pygame.time.Clock()
    time = 0.0
    whichTexture = 0
    while True:
        clock.tick(30)
        time += 0.01
        # Event queued input
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYUP and event.key == K_ESCAPE:
                return
            if event.type == KEYDOWN and event.key == K_SPACE:
                whichTexture += 1
                whichTexture %= 4
                for i,mesh in enumerate(theBox):
                    mesh.texture = theTextures[whichTexture][i]

        # Polling input is better for a real time camera
        pressed = pygame.key.get_pressed()

        # keys for zoom:
        if pressed[K_z]:
            theCamera.zoomIn(1.015)
        if pressed[K_x]:
            theCamera.zoomOut(1.015)

        # arrow keys for movement:
        movespeed = 0.1
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

