#Tetrahedron
# perspective camera

from ctypes import c_void_p

from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram

import pygame
from pygame.locals import *
import numpy as N

null = c_void_p(0)
sizeOfFloat = 4
sizeOfShort = 2

strVertexShader = """
#version 330
in vec4 position;
in vec4 vertexColor;
out vec4 fragmentColor;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
void main()
{
  vec4 offset;
  float x,y,z; 
  if (gl_InstanceID % 2 == 0) {
    z = 0.5;
  } else {
    z = -0.5;
  }
  if ((gl_InstanceID / 2) % 2 == 0 ) {
    y = 0.5;
  } else {
    y = -0.5;
  }
  if ((gl_InstanceID / 4) % 2 == 1) {
    x = 0.5;
  } else {
    x = -0.5;
  }
  offset = vec4(x,y,z,0);
  fragmentColor = vertexColor;
  gl_Position = projection * view * (model * position + offset);
}
"""

strFragmentShader = """
#version 330
in vec4 fragmentColor;
out vec4 outputColor;
void main()
{
   outputColor = fragmentColor;
}
"""

# Some global variables to be filled in later:

# Integer handle identifying our compiled shader program
theShaders = None
# Handle to the position attribute in the vertex shader:
positionAttrib = None
rotationAttrib = None

# Use PyOpenLG's compile shader programs, which simplify this task.
# Assign the compiled program to theShaders.
def initializeShaders():
    global theShaders, positionAttrib, colorAttrib, modelUnif, viewUnif, projUnif
    theShaders = compileProgram(
        compileShader(strVertexShader, GL_VERTEX_SHADER),
        compileShader(strFragmentShader, GL_FRAGMENT_SHADER)
    )
    positionAttrib = glGetAttribLocation(theShaders, "position")
    colorAttrib = glGetAttribLocation(theShaders, "vertexColor")
    modelUnif = glGetUniformLocation(theShaders, "model")
    viewUnif = glGetUniformLocation(theShaders, "view")
    projUnif = glGetUniformLocation(theShaders, "projection")
    print "Attribs:", positionAttrib, colorAttrib
    print "Uniforms:", modelUnif, viewUnif, projUnif

# Vertex Data
tetraVertices = N.array([
    0.35, 0.5, 0.0, 1.0,
    1.0, 0.0, 0.0, 1.0,
    0.35, -0.5, 0.0, 1.0,
    0.0, 1.0, 0.0, 1.0,
    -0.35, 0.0, 0.5, 1.0,
    0.0, 0.0, 1.0, 1.0,
    -0.35, 0.0, -0.5, 1.0,
    1.0, 1.0, 0.0, 1.0], dtype=N.float32)

vertexComponents = 8

# 3 indices into the buffer per triangle
# use unsigned short (16 bit) integers, usually plenty
tetraElements = N.array((0,2,1,
                         0,1,3,
                         0,3,2,
                         1,2,3),dtype=N.uint16)

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

# Get a buffer for positions and colors
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
    global camera
    initializeShaders()
    initializeVertexBuffer()
    initializeVAO()
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)

# Called to redraw the contents of the window
def display(time):
    
    # Clear the display
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)

    # Set the shader program
    glUseProgram(theShaders)

    # compute camera matrix
    # Leave the objects in the +-1 cube
    # Make the camera circle around the +-1 cube
    
    # move the camera in positive z
    tran = N.array(((1,0,0,0),
                    (0,1,0,0),
                    (0,0,1,-3),
                    (0,0,0,1)), dtype=N.float32)
    
    # rotate the camera around y
    s = N.sin(time)
    c = N.cos(time)
    rot = N.array(((c,0,-s,0),
                   (0,1,0,0),
                   (s,0,c,0),
                   (0,0,0,1)), dtype=N.float32)
    view = N.dot(tran, rot)
    
    # send matrix to the graphics card
    glUniformMatrix4fv(viewUnif, 1, GL_TRUE, view)
    
    # compute projection
    n = 1.0
    f = 100.0
    r = 0.5*n
    t = 0.5*n

    # we're using row-major order, so if we're not doing any
    # matrix manipulation here, we can lay out the matrix as
    # a single dimensional array.  Otherwise, numpy has to know
    # the shape of the array, so don't do this in general
    proj = N.array((n/r, 0, 0, 0,
                    0, n/t, 0, 0,
                    0, 0, -(f+n)/(f-n), -2*f*n/(f-n),
                    0, 0, -1, 0), dtype=N.float32)
                    
    # send projection to the graphics card
    glUniformMatrix4fv(projUnif, 1, GL_TRUE, proj)
       
    # compute model rotation matrix:
    s = N.sin(time)
    c = N.cos(time)
    zrot = N.array(((c,-s,0,0),
                    (s,c,0,0),
                    (0,0,1,0),
                    (0,0,0,1)),dtype = N.float32)
    yrot = N.array(((c,0,-s,0),
                    (0,1,0,0),
                    (s,0,c,0),
                    (0,0,0,1)), dtype=N.float32)
    xrot = N.array(((1,0,0,0),
                    (0,c,-s,0),
                    (0,s,c,0),
                    (0,0,0,1)), dtype=N.float32)
    rot = N.dot(zrot, N.dot(yrot, xrot))
    # send model matrix 
    glUniformMatrix4fv(modelUnif, 1, GL_TRUE, rot)
    
#BUFFERS
    # Use the tirangle data
    glBindBuffer(GL_ARRAY_BUFFER, vertexBuffer)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, elementBuffer)
#POSITION    
    # Tell the shader program which attribute to use for this buffer
    glEnableVertexAttribArray(positionAttrib)
    
    # Tell the shader program what the data in the buffer look like
    glVertexAttribPointer(positionAttrib,
                          4,
                          GL_FLOAT,
                          GL_FALSE,
                          vertexComponents*sizeOfFloat,
                          c_void_p(0))
#COLOR
    # Tell the shader program which attribute to use for this buffer
    glEnableVertexAttribArray(colorAttrib)

    # Tell the shader what the data in the buffer look like
    glVertexAttribPointer(colorAttrib,
                          4,
                          GL_FLOAT,
                          GL_FALSE,
                          vertexComponents*sizeOfFloat,
                          c_void_p(4*sizeOfFloat))
#DRAW    
    # Use that data and the elements to draw triangles
    glDrawElementsInstanced(
        GL_TRIANGLES, len(tetraElements)*sizeOfShort,
        GL_UNSIGNED_SHORT, c_void_p(0),
        8)
    

    # Stop using the shader program
    glUseProgram(0)

def main():
    global screen
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

