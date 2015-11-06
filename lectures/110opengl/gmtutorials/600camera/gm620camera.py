#camera controls
# using camera class

import os,sys
from ctypes import c_void_p

from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram

import pygame
from pygame.locals import *
import numpy as N

sys.path.insert(0, os.path.join("..","utilities"))
from psurfaces import torus
from transforms import *
from loadtexture import loadTexture
from frames import Camera

null = c_void_p(0)
sizeOfFloat = 4
sizeOfShort = 2

def readShader(filename):
    with open(os.path.join("..","shaders", filename)) as fp:
        return fp.read()
strVertexShader = readShader("bumpmap.vert")
strFragmentShader = readShader("knot.frag")

def check(name, val):
    if val < 0:
        print "Warning:", name, "has value", val
        
# Use PyOpenLG's compile shader programs, which simplify this task.
# Assign the compiled program to theShaders.
def initializeShaders():
    global theShaders, positionAttrib, normalAttrib, tangentAttrib,\
        binormalAttrib, uvAttrib, \
        modelUnif, viewUnif, projUnif, lightUnif, \
        colorSamplerUnif, bumpSamplerUnif, scaleuvUnif, colorUnif
    theShaders = compileProgram(
        compileShader(strVertexShader, GL_VERTEX_SHADER),
        compileShader(strFragmentShader, GL_FRAGMENT_SHADER)
    )
    positionAttrib = glGetAttribLocation(theShaders, "position")
    normalAttrib = glGetAttribLocation(theShaders, "normal")
    tangentAttrib = glGetAttribLocation(theShaders, "tangent")
    binormalAttrib = glGetAttribLocation(theShaders, "binormal")
    uvAttrib = glGetAttribLocation(theShaders, "uv")
    
    lightUnif = glGetUniformLocation(theShaders, "light")
    modelUnif = glGetUniformLocation(theShaders, "model")
    viewUnif = glGetUniformLocation(theShaders, "view")
    projUnif = glGetUniformLocation(theShaders, "projection")
    colorSamplerUnif = glGetUniformLocation(theShaders, "colorsampler")
    bumpSamplerUnif = glGetUniformLocation(theShaders, "bumpsampler")
    scaleuvUnif = glGetUniformLocation(theShaders, "scaleuv")
    colorUnif = glGetUniformLocation(theShaders, "color")

    check("positionAttrib", positionAttrib)
    check("normalAttrib", normalAttrib)
    check("tangentAttrib", tangentAttrib)
    check("binormalAttrib", binormalAttrib)
    check("uvAttrib", uvAttrib)
    
    check("modelUnif", modelUnif)
    check("viewUnif", viewUnif)
    check("projUnif", projUnif)
    check("lightUnif", lightUnif)
    check("scaleuvUnif", scaleuvUnif)
    check("colorUnif", colorUnif)

# Vertex Data, positions and normals and texture coords
mytorus = torus(0.5, 0.2, 32, 16)
torusVertices = mytorus[0]
torusElements = mytorus[1]
vertexComponents = 18 # 4 position, 4 normal, 4 tangent, 4 binormal, 2 texture

# Ask the graphics card to create a buffer for our vertex data
def getFloatBuffer(arr):
    buff = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, buff)
    glBufferData(GL_ARRAY_BUFFER, arr, GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    return buff

def getElementBuffer(arr):
    buff = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buff)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, arr, GL_STATIC_DRAW)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
    return buff

# Get a buffers for vertices and elements
def initializeVertexBuffer():
    global vertexBuffer, elementBuffer
    vertexBuffer = getFloatBuffer(torusVertices)
    elementBuffer = getElementBuffer(torusElements)

# Ask the graphics card to create a VAO object.
# A VAO object stores one or more vertex buffer objects.
def initializeVAO():
    n = 1
    vaoArray = N.zeros(n, dtype=N.uint)
    vaoArray = glGenVertexArrays(n)
    glBindVertexArray( vaoArray )

# Called once at application start-up.
# Must be called after we have an OpenGL context, i.e. after the pygame
# window is created
def init():
    initializeShaders()
    initializeVertexBuffer()
    initializeVAO()
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)

# Called to redraw the contents of the window
def display(time):
    global proj
    # Clear the display
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)

    # Set the shader program
    glUseProgram(theShaders)

    glUniform2fv(scaleuvUnif, 1, N.array((32,8), dtype=N.float32))
    glUniform4fv(colorUnif, 1, N.array((0,1,0,1), dtype=N.float32))

    # moving the camera is in response to input
    # send camera view matrix to the graphics card
    glUniformMatrix4fv(viewUnif, 1, GL_TRUE, camera.view())
                    
    # send projection to the graphics card
    glUniformMatrix4fv(projUnif, 1, GL_TRUE, camera.projection())
       
    # static model:
    rot = N.identity(4,dtype=N.float32)
    # send model matrix 
    glUniformMatrix4fv(modelUnif, 1, GL_TRUE, rot)

    # send light direction
    light = N.array((0.577,0.577,0.577,0), dtype=N.float32)
    #light = N.dot(Yrot(time*0.5), light)
    glUniform4fv(lightUnif, 1, light)
    
#BUFFERS
    # Use the tirangle data
    glBindBuffer(GL_ARRAY_BUFFER, vertexBuffer)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, elementBuffer)
#POSITION    
    glEnableVertexAttribArray(positionAttrib)
    glVertexAttribPointer(positionAttrib,
                          4,
                          GL_FLOAT,
                          GL_FALSE,
                          vertexComponents*sizeOfFloat,
                          c_void_p(0))
#NORMAL, TANGENT, BINORMAL
    glEnableVertexAttribArray(normalAttrib)
    glVertexAttribPointer(normalAttrib,
                          4,
                          GL_FLOAT,
                          GL_FALSE,
                          vertexComponents*sizeOfFloat,
                          c_void_p(4*sizeOfFloat))
    glEnableVertexAttribArray(tangentAttrib)
    glVertexAttribPointer(tangentAttrib,
                          4,
                          GL_FLOAT,
                          GL_FALSE,
                          vertexComponents*sizeOfFloat,
                          c_void_p(8*sizeOfFloat))
    glEnableVertexAttribArray(binormalAttrib)
    glVertexAttribPointer(binormalAttrib,
                          4,
                          GL_FLOAT,
                          GL_FALSE,
                          vertexComponents*sizeOfFloat,
                          c_void_p(12*sizeOfFloat))
#UV coordinates
    glEnableVertexAttribArray(uvAttrib)
    glVertexAttribPointer(uvAttrib,
                          2,
                          GL_FLOAT,
                          GL_FALSE,
                          vertexComponents*sizeOfFloat,
                          c_void_p(16*sizeOfFloat))
#DRAW    
    # Use that data and the elements to draw triangles
    glDrawElements(
        GL_TRIANGLES, len(torusElements)*sizeOfShort,
        GL_UNSIGNED_SHORT, c_void_p(0))
    
    # Stop using the shader program
    glUseProgram(0)

def main():
    global camera, screen, proj
    
    pygame.init()

    pygame.mouse.set_cursor(*pygame.cursors.broken_x)

    width, height = 1024,768
    screen = pygame.display.set_mode((width, height), OPENGL|DOUBLEBUF)

    # compute projection
    aspectRatio = float(width)/float(height)
    near = 0.01
    far = 100.0
    lens = 4.0  # "longer" lenses mean more telephoto
    camera = Camera(lens, near, far, aspectRatio)
    camera.moveBack(3)

    clock = pygame.time.Clock()
    init()
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
            camera.zoomIn(1.015)
        if pressed[K_x]:
            camera.zoomOut(1.015)

        # arrow keys for movement:
        movespeed = 0.05
        if pressed[K_d] | pressed[K_RIGHT]:
            camera.moveRight(movespeed)
        if pressed[K_a] | pressed[K_LEFT]:
            camera.moveRight(-movespeed)
        if pressed[K_w] | pressed[K_UP]:
            camera.moveBack(-movespeed)
        if pressed[K_s] | pressed[K_DOWN]:
            camera.moveBack(movespeed)
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
                camera.yaw(-xNormed * aspectRatio * rotspeed)
                camera.pitch(-yNormed * 1 * rotspeed)
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

