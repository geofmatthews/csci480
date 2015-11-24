# Using framebuffers to make a tv monitor.
# lots of objects

import os,sys

from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram

import pygame
from pygame.locals import *
import numpy as N

sys.path.insert(0, os.path.join("..","utilities"))
from obj import readOBJ
from psurfaces import *
from polyhedra import *
from specials import rectangle
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
    global theMeshes, theTV, theTV2, theLight, theCamera, \
           theScreen, theTVCamera, theFramebuffer, theFramebuffer2,\
           resolution
    initializeVAO()
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)

    # FRAMEBUFFER
    # create a frame buffer and bind to it
    resolution = 512
    theFramebuffer = getFramebuffer(resolution)    
    theFramebuffer2 = getFramebuffer(resolution)    

    # Add our objects
    # LIGHT
    theLight = N.array((-0.577, 0.577, 0.577, 0.0),dtype=N.float32)
    # OBJECTS
    theMeshes = []
    phongshader = makeShader("phongshader.vert","phongshader.frag")
    verts, elements = torus(2.0,0.2,64,16)
    torusVerts = getArrayBuffer(verts)
    torusElements = getElementBuffer(elements)
    torusNum = len(elements)
    verts, elements = sphere(2.0,64,32)
    sphereVerts = getArrayBuffer(verts)
    sphereElements = getArrayBuffer(elements)
    sphereNum = len(elements)
    verts, elements = tetrahedron(4)
    tetraVerts = getArrayBuffer(verts)
    tetraElements = getElementBuffer(elements)
    tetraNum = len(elements)
    verts, elements = readOBJ("suzanne.obj")
    suzanneVerts = getArrayBuffer(verts)
    suzanneElements = getElementBuffer(elements)
    suzanneNum = len(elements)
    for i in range(16):
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
        x = N.random.random()*10-5
        y = N.random.random()*10-5
        z = N.random.random()*10-5
        newmesh.moveRight(x)
        newmesh.moveUp(y)
        newmesh.moveBack(z)
        newmesh.pitch(x)
        newmesh.yaw(y)
        newmesh.roll(z)
        theMeshes.append(newmesh)    

    # TVs
    width, height = theScreen.get_size()
    aspectRatio = float(width)/float(height)
    verts, elements = rectangle(20*aspectRatio,20)
    arrayBuffer = getArrayBuffer(verts)
    elementBuffer = getElementBuffer(elements)
    numElements = len(elements)
    texturedShader = makeShader("flattextured.vert", "flattextured.frag")
    texture = loadTexture("grid.png")
    theTV = flatTexturedMesh(texture,
                             arrayBuffer,
                             elementBuffer,
                             numElements,
                             texturedShader,
                             fade=0.9)
    
    theTV.moveRight(10)
    theTV.yaw(-1)
    theTV2 = flatTexturedMesh(texture,
                              arrayBuffer,
                              elementBuffer,
                              numElements,
                              texturedShader,
                              fade=0.9)
    
    theTV2.moveRight(-10)
    theTV2.yaw(1)
    
    # CAMERA
    near = 0.01
    far = 100.0
    lens = 4.0  # "longer" lenses mean more telephoto
    theCamera = Camera(lens, near, far, aspectRatio)
    theCamera.moveBack(50)

    # TV CAMERA
    theTVCamera = Camera(lens, near, far, float(width)/float(height))
    theTVCamera.yaw(-0.5)
    theTVCamera.moveBack(50)

# Called to redraw the contents of the window
def display(time):
    global theMeshes, theTV, theLight, theCamera, \
    theTVCamera, theFramebuffer, theFramebuffer2, \
    theScreen, whichCamera, whichTVCamera, \
    resolution
    
    # do stuff in the scene:
    for theMesh in theMeshes:
        x,y,z,w = theMesh.position*time
        theMesh.postTransform =  N.dot(Zrot(z),
                                       N.dot(Yrot(y),
                                             Xrot(x)))

    # first draw the tv cameras

    for i,fb in enumerate((theFramebuffer, theFramebuffer2)):
        # bind to our framebuffer
        glBindFramebuffer(GL_FRAMEBUFFER, fb)
        # draw on the whole framebuffer
        glViewport(0,0,resolution,resolution)
        # draw
        # Clear the display
        glClearColor(0.1, 0.2, 0.3, 0.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glClear(GL_DEPTH_BUFFER_BIT)

        if i == 0:
            view = theTVCamera.view()
            proj = theTVCamera.projection()
        else:
            view = theCamera.view()
            proj = theCamera.projection()
        for theMesh in theMeshes:
            theMesh.display(view, proj, theLight)
        theTV.display(view, proj, theLight)
        theTV2.display(view, proj, theLight)

    # now set the texture of our tv to the rendered texture
    theTV.texture = theFramebuffer
    theTV2.texture = theFramebuffer2

    # now draw the regular camera to the default framebuffer
    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    width, height = theScreen.get_size()
    glViewport(0,0,width,height)
    # draw
    # Clear the display
    glClearColor(0.1, 0.2, 0.3, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)

    if whichCamera == 0:
        view = theCamera.view()
        proj = theCamera.projection()
    else:
        view = theTVCamera.view()
        proj = theTVCamera.projection()

    for theMesh in theMeshes:
        theMesh.display(view, proj, theLight)
    theTV.display(view, proj, theLight)
    theTV2.display(view, proj, theLight)

def main():
    global theCamera, theScreen, whichCamera, whichTVCamera
    
    pygame.init()
    pygame.mouse.set_cursor(*pygame.cursors.broken_x)

    width, height = 1024,768
    theScreen = pygame.display.set_mode((width, height), OPENGL|DOUBLEBUF)

    init()
    clock = pygame.time.Clock()
    time = 0.0
    whichCamera = 0
    whichTVCamera = 0
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
                whichCamera += 1
                whichCamera %= 2
            if event.type == KEYDOWN and event.key == K_F1:
                whichTVCamera += 1
                whichTVCamera %= 2
            
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

