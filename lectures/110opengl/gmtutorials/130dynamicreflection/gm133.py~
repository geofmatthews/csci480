# Skybox with reflection of more objects using 6 cameras
# and framebuffers for the reflector's textures
# Note the self-reflections on the OUTSIDE of the torus.

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
from randomobjects import makeObjects
from transforms import *
from loadtexture import loadTexture
from camera import Camera
from meshes import *
from framebuffer import getFramebuffer

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
    global theMeshes, theBox, theLight, theCamera, theCameras, \
        theScreen, theTextures,\
        nonReflectors, theFramebuffers
    initializeVAO()
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    # REFLECTOR CAMERAS AND FRAMEBUFFERS
    theFramebuffers = [getFramebuffer(512) for x in range(6)]
    theCameras = [Camera(1.0, 0.01, 1000.0, 1.0) for x in range(6)]
    # X
    theCameras[0].yaw(-1)
    theCameras[0].yaw(-1)
    theCameras[1].yaw(+1)
    theCameras[1].yaw(+1)
    # Y
    theCameras[2].pitch(-1)
    theCameras[2].pitch(-1)
    theCameras[3].pitch(+1)
    theCameras[3].pitch(+1)
    # Z
    theCameras[4].yaw(1)
    theCameras[4].yaw(1)
    theCameras[4].yaw(1)
    theCameras[4].yaw(1)
    # negZ camera already pointed

    # LIGHT
    # put the light in a direction to agree with the skybox
    theLight = N.array((0.707, 0.707, 0.0, 0.0),dtype=N.float32)
    # we need the textures to define our reflecting objects

    # NONREFLECTING OBJECTS
    nonReflectors = makeObjects(32)

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
    

    # REFLECTING OBJECTS
    theMeshes = []
    verts,elements = torus(2.0, 0.75, 64, 16)
    theMeshes.append(
        reflectorMesh(theTextures[0][0],
                      theTextures[0][1],
                      theTextures[0][2],
                      theTextures[0][3],
                      theTextures[0][4],
                      theTextures[0][5],
                      getArrayBuffer(verts),
                      getElementBuffer(elements),
                      len(elements),
                      makeShader("reflector.vert",
                                 "reflector.frag")
                  )
    )
    verts,elements = sphere(2.0, 64, 32)
    theMeshes.append(
        reflectorMesh(theTextures[0][0],
                      theTextures[0][1],
                      theTextures[0][2],
                      theTextures[0][3],
                      theTextures[0][4],
                      theTextures[0][5],
                      getArrayBuffer(verts),
                      getElementBuffer(elements),
                      len(elements),
                      makeShader("reflector.vert",
                                 "reflector.frag")
                  )
    )
    verts,elements = tetrahedron(4.0)
    theMeshes.append(
        reflectorMesh(theTextures[0][0],
                      theTextures[0][1],
                      theTextures[0][2],
                      theTextures[0][3],
                      theTextures[0][4],
                      theTextures[0][5],
                      getArrayBuffer(verts),
                      getElementBuffer(elements),
                      len(elements),
                      makeShader("reflector.vert",
                                 "reflector.frag")
                  )
    )
    verts,elements = readOBJ("suzanne.obj")
    theMeshes.append(
        reflectorMesh(theTextures[0][0],
                      theTextures[0][1],
                      theTextures[0][2],
                      theTextures[0][3],
                      theTextures[0][4],
                      theTextures[0][5],
                      getArrayBuffer(verts),
                      getElementBuffer(elements),
                      len(elements),
                      makeShader("reflector.vert",
                                 "reflector.frag")
                  )
    )

    # SKYBOX
    boxsize = 100.0
    skyboxShader = makeShader("flattextured.vert","flattextured.frag")
    verts,elements = rectangle(boxsize, boxsize)
    vertBuff = getArrayBuffer(verts)
    elemBuff = getElementBuffer(elements)
    numElems = len(elements)
    posx = flatTexturedMesh(theTextures[0][0],
                            vertBuff,
                            elemBuff,
                            numElems,
                            skyboxShader,
                            N.array((1.0,1.0),dtype=N.float32))
    negx = flatTexturedMesh(theTextures[0][1],
                            vertBuff,
                            elemBuff,
                            numElems,
                            skyboxShader,
                            N.array((1.0,1.0),dtype=N.float32))
    posy = flatTexturedMesh(theTextures[0][2],
                            vertBuff,
                            elemBuff,
                            numElems,
                            skyboxShader,
                            N.array((1.0,1.0),dtype=N.float32))
    negy = flatTexturedMesh(theTextures[0][3],
                            vertBuff,
                            elemBuff,
                            numElems,
                            skyboxShader,
                            N.array((1.0,1.0),dtype=N.float32))
    posz =  flatTexturedMesh(theTextures[0][4],
                            vertBuff,
                            elemBuff,
                            numElems,
                             skyboxShader,
                             N.array((1.0,1.0),dtype=N.float32))
    negz =  flatTexturedMesh(theTextures[0][5],
                            vertBuff,
                            elemBuff,
                            numElems,
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
    global theScreen, theCamera, theFramebuffers, theCameras, \
        theMeshes, whichMesh
    # do stuff in the scene
    for nr in nonReflectors:
        x,y,z,w = nr.position*time*0.5
        nr.postTransform =  N.dot(Zrot(z),
                                  N.dot(Yrot(y),
                                        Xrot(x)))
    meshspeed = 0.01
    theMesh = theMeshes[whichMesh]
    if whichMesh == 1:  # sphere
        theMesh.moveRight(meshspeed*10)
        theMesh.yaw(meshspeed*10)
    else:
        theMesh.pitch(meshspeed)
        theMesh.yaw(meshspeed*1.1)
        theMesh.roll(meshspeed*1.2)

    # draw our six reflected images
    for fb in range (6):
        displayFB(time,
                  theFramebuffers[fb], 512, 512,
                  theCameras[fb])
    # copy the textures to the reflector object
    theMesh.posxTexture = theFramebuffers[0]
    theMesh.negxTexture = theFramebuffers[1]
    theMesh.posyTexture = theFramebuffers[2]
    theMesh.negyTexture = theFramebuffers[3]
    theMesh.poszTexture = theFramebuffers[4]
    theMesh.negzTexture = theFramebuffers[5]
    # draw the scene
    width,height = theScreen.get_size()
    displayFB(time, 0, width, height, theCamera)

# Here we parameterize the display routine with a framebuffer
# and a camera
def displayFB(time, framebuffer, width, height, camera):
    global theMeshes, theBox, theLight, theCamera, whichMesh, \
        nonReflectors, theFramebuffers
    view = camera.view()
    proj = camera.projection()
    onlyrot = camera.onlyRotation()
    
    glBindFramebuffer(GL_FRAMEBUFFER, framebuffer)
    glViewport(0,0,width,height)
    # Clear the display
    glClearColor(0.1, 0.2, 0.3, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)

    glDisable(GL_DEPTH_TEST)
    for mesh in theBox:
        mesh.display(onlyrot, proj, None)
    glEnable(GL_DEPTH_TEST)
    # display nonreflectors
    for nr in nonReflectors:
        nr.display(view, proj, theLight)
    # display the mesh
    theMeshes[whichMesh].display(view, proj, theLight)

def main():
    global theCamera, theScreen, theMeshes, theTextures, theBox, whichMesh
    
    pygame.init()
    pygame.mouse.set_cursor(*pygame.cursors.broken_x)

    width, height = 1024,768
    theScreen = pygame.display.set_mode((width, height), OPENGL|DOUBLEBUF)

    init()
    clock = pygame.time.Clock()
    whichTexture = 0
    whichMesh = 0
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
            if event.type == KEYDOWN and event.key == K_SPACE:
                whichTexture += 1
                whichTexture %= 4
                for i,mesh in enumerate(theBox):
                    mesh.texture = theTextures[whichTexture][i]
                # change texture on object, too
                for theMesh in theMeshes:
                    theMesh.posxTexture = theTextures[whichTexture][0]
                    theMesh.negxTexture = theTextures[whichTexture][1]
                    theMesh.posyTexture = theTextures[whichTexture][2]
                    theMesh.negyTexture = theTextures[whichTexture][3]
                    theMesh.poszTexture = theTextures[whichTexture][4]
                    theMesh.negzTexture = theTextures[whichTexture][5]
            if event.type == KEYDOWN and event.key == K_F1:
                whichMesh += 1
                whichMesh %= 4

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

