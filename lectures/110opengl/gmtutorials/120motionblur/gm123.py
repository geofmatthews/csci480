# Using framebuffers to make motion blur.
# Use multiple framebuffers to render scene at different times,
# then blend them all with the motionblur.frag shader,
# used by the motionblurMesh object
# try changing the speed, and the size of the blur steps

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
    global theMesh,  theLight, theCamera, \
           theScreen,  theFramebuffers, \
           theSquare, resolution
    initializeVAO()
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)

    # FRAMEBUFFER
    # create a frame buffer and bind to it
    resolution = 512
    numBuffers = 8
    theFramebuffers = [getFramebuffer(resolution) for i in range(numBuffers)]

    # SQUARE IN NDC
    verts, elements = rectangle(2,2)
    arrayBuffer = getArrayBuffer(verts)
    elementBuffer = getElementBuffer(elements)
    numElements = len(elements)
    flatShader = makeShader("flattextured.vert", "motionblur.frag")
    texture = loadTexture("grid.png")
    textures = [texture for i in range(8)]
    theSquare = motionblurMesh(textures,
                               arrayBuffer,
                               elementBuffer,
                               numElements,
                               flatShader)

    # Add our object
    # LIGHT
    theLight = N.array((-0.577, 0.577, 0.577, 0.0),dtype=N.float32)
    # OBJECT
    phongshader = makeShader("phongshader.vert","phongshader.frag")
    verts, elements = readOBJ("suzanne.obj")
    suzanneVerts = getArrayBuffer(verts)
    suzanneElements = getElementBuffer(elements)
    suzanneNum = len(elements)
    theMesh = coloredMesh(N.array((1.0, 0.5, 1.0, 1.0), dtype=N.float32),
                          suzanneVerts,
                          suzanneElements,
                          suzanneNum,
                          phongshader)

    # CAMERA
    width,height = theScreen.get_size()
    aspectRatio = float(width)/float(height)
    near = 0.01
    far = 100.0
    lens = 4.0  # "longer" lenses mean more telephoto
    theCamera = Camera(lens, near, far, aspectRatio)
    theCamera.moveBack(6)

# Called to redraw the contents of the window
def display(time):
    global theMesh,  theLight, theCamera, \
        theFramebuffers, theSquare, \
        theScreen, resolution
    
    # do stuff in the scene
    meshSpeed = 0.6
    meshTime = 2.0*N.pi*time/meshSpeed
    theMesh.moveRight(meshSpeed*N.cos(meshTime))

    # bind to our framebuffers, and send them to the mesh
    blur = 0.5
    for fb in range(8):
        # advance time:
        adjust = N.sin(meshTime+blur*fb/8.0)
        theMesh.moveRight(adjust)

        # bind buffer
        glBindFramebuffer(GL_FRAMEBUFFER, theFramebuffers[fb])
        glViewport(0,0,resolution,resolution)

        # draw
        # Clear the display
        glClearColor(0.1, 0.2, 0.3, 0.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glClear(GL_DEPTH_BUFFER_BIT)

        view = theCamera.view()
        proj = theCamera.projection()

        theMesh.display(view, proj, theLight)
        
        # now send our texture to the square
        theSquare.textures[fb] = theFramebuffers[fb]

        # reset time:
        theMesh.moveRight(-adjust)

    # now bind the the default framebuffer
    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    width,height = theScreen.get_size()
    glViewport(0,0,width,height)
    # now draw just the square
    glClearColor(0.1, 0.2, 0.3, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)

    id = N.identity(4, dtype=N.float32)
    theSquare.display(id, id, 0)    

def main():
    global theCamera, theScreen
    
    pygame.init()
    pygame.mouse.set_cursor(*pygame.cursors.broken_x)

    width, height = 1024,194
    theScreen = pygame.display.set_mode((width, height), OPENGL|DOUBLEBUF)
    print glGetIntegerv(GL_MAX_RENDERBUFFER_SIZE)

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
            if event.type == KEYDOWN and event.key == K_SPACE:
                pass
            
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

#        # mouse for rotation
#        rotspeed = 0.1
#        mousespeed = 0.5*rotspeed
#        x,y = pygame.mouse.get_pos()
#        if (x > 0) & (y > 0):
#            xDisplacement = x - 0.5*width
#            yDisplacement = y - 0.5*height
#            # normalize:
#            xNormed = xDisplacement/width
#            yNormed = -yDisplacement/height
#            newx = int(x - xDisplacement*mousespeed)
#            newy = int(y - yDisplacement*mousespeed)
#            if (newx != x) | (newy != y):
#                theCamera.pan(-xNormed * rotspeed)
#                theCamera.tilt(-yNormed * rotspeed)
#                pygame.mouse.set_pos((newx,newy))

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

