#tetrahedron

import os, sys
from ctypes import c_void_p

from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram

import pygame
from pygame.locals import *
import numpy as N

sys.path.append(os.path.join("..","utilities"))
from polyhedra import tetrahedron
from transforms import *
from loadtexture import loadTexture

null = c_void_p(0)
sizeOfFloat = 4
sizeOfShort = 2

def readShader(filename):
    with open(os.path.join("..","shaders", filename)) as fp:
        return fp.read()
strVertexShader = readShader("bumpmap.vert")
strFragmentShader = readShader("bumpmap.frag")

def check(name, val):
    if val < 0:
        print "Warning:", name, "has value", val
        
# Use PyOpenLG's compile shader programs, which simplify this task.
# Assign the compiled program to theShaders.
def initializeShaders():
    global theShaders, positionAttrib, normalAttrib, tangentAttrib,\
        bitangentAttrib, uvAttrib, \
        modelUnif, viewUnif, projUnif, lightUnif, \
        colorSamplerUnif, normalSamplerUnif, makeBumpUnif
    theShaders = compileProgram(
        compileShader(strVertexShader, GL_VERTEX_SHADER),
        compileShader(strFragmentShader, GL_FRAGMENT_SHADER)
    )
    positionAttrib = glGetAttribLocation(theShaders, "position")
    normalAttrib = glGetAttribLocation(theShaders, "normal")
    tangentAttrib = glGetAttribLocation(theShaders, "tangent")
    bitangentAttrib = glGetAttribLocation(theShaders, "bitangent")
    uvAttrib = glGetAttribLocation(theShaders, "uv")
    
    lightUnif = glGetUniformLocation(theShaders, "light")
    modelUnif = glGetUniformLocation(theShaders, "model")
    viewUnif = glGetUniformLocation(theShaders, "view")
    projUnif = glGetUniformLocation(theShaders, "projection")
    colorSamplerUnif = glGetUniformLocation(theShaders, "colorsampler")
    normalSamplerUnif = glGetUniformLocation(theShaders, "normalsampler")
    makeBumpUnif = glGetUniformLocation(theShaders, "usenormals")

    check("positionAttrib", positionAttrib)
    check("normalAttrib", normalAttrib)
    check("tangentAttrib", tangentAttrib)
    check("bitangentAttrib", bitangentAttrib)
    check("uvAttrib", uvAttrib)
    
    check("modelUnif", modelUnif)
    check("viewUnif", viewUnif)
    check("projUnif", projUnif)
    check("lightUnif", lightUnif)
    check("colorSamplerUnif", colorSamplerUnif)
    check("normalSamplerUnif", normalSamplerUnif)
    check("makeBumpUnif", makeBumpUnif)

# Vertex Data, positions and normals and texture coords
mytetra = tetrahedron(1.5)
tetraVertices = mytetra[0]
tetraElements = mytetra[1]
vertexComponents = 18 # 4 position, 4 normal, 4 tangent, 4 bitangent, 2 texture

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
    vertexBuffer = getFloatBuffer(tetraVertices)
    elementBuffer = getElementBuffer(tetraElements)

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
    global colorTexture, normalTexture
    initializeShaders()
    initializeVertexBuffer()
    initializeVAO()
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    # this has to be done here because we need an opengl context.
    # reading the file could be done without the context,
    # but loadTexture bundles reading the file and creating
    # a texture all in one.
    colorTexture = loadTexture("brickwork-texture.jpg")
    normalTexture = loadTexture("brickwork_normal-map.jpg")
    #colorTexture = loadTexture("grid.png")

# Called to redraw the contents of the window
def display(time):
    global makebumps;

    # Clear the display
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)

    # Set the shader program
    glUseProgram(theShaders)

    # decide to use bumps
    glUniform1i(makeBumpUnif, makebumps)

    # move the camera in positive z
    view = translation(0,0,-2)
    #rotate the camera around x
    view = N.dot(view,Xrot(45.0*N.pi/180.0))
    
    # send matrix to the graphics card
    glUniformMatrix4fv(viewUnif, 1, GL_TRUE, view)
    
    # compute projection
    n = 1.0
    f = 100.0
    r = 0.5*n
    t = 0.5*n
    proj = projection(n,f,r,t)
                    
    # send projection to the graphics card
    glUniformMatrix4fv(projUnif, 1, GL_TRUE, proj)
       
    # compute model rotation matrix:
    xrot = Xrot(time)
    yrot = Yrot(time)
    zrot = Zrot(time)
    tilt = Zrot(0.4)
    rot = N.dot(zrot, N.dot(yrot, xrot))
    # send model matrix 
    glUniformMatrix4fv(modelUnif, 1, GL_TRUE, rot)

    # Instead of sending a single color,
    # or using colors from a vertex buffer, 
    # we bind to a texture unit
    # and then tell our sampler to use that unit

    # bind our color texture units
    colorUnit = 0
    glActiveTexture(GL_TEXTURE0 + colorUnit)
    glBindTexture(GL_TEXTURE_2D, colorTexture)
    glUniform1i(colorSamplerUnif, colorUnit)

    # bind our normal texture units
    normalUnit = 1
    glActiveTexture(GL_TEXTURE0 + normalUnit)
    glBindTexture(GL_TEXTURE_2D, normalTexture)
    glUniform1i(normalSamplerUnif, normalUnit)
    
    # send light direction
    light = N.array((0,0,1,0), dtype=N.float32)
    light = N.dot(Yrot(time*0.5), light)
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
#NORMAL, TANGENT, BITANGENT
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
    glEnableVertexAttribArray(bitangentAttrib)
    glVertexAttribPointer(bitangentAttrib,
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
        GL_TRIANGLES, len(tetraElements)*sizeOfShort,
        GL_UNSIGNED_SHORT, c_void_p(0))
    
    # Stop using the shader program
    glUseProgram(0)

def main():
    global screen, makebumps
    makebumps = 0
    pygame.init()
    screen = pygame.display.set_mode((512,512), OPENGL|DOUBLEBUF)
    clock = pygame.time.Clock()
    init()
    time = 0.0
    while True:
        clock.tick(30)
        time += 0.02
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYUP and event.key == K_ESCAPE:
                return
            if event.type == KEYDOWN and event.key == K_SPACE:
                makebumps = (makebumps + 1) % 2
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

