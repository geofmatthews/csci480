#Use a single buffer for both positions and colors

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
uniform mat4 rotation;
void main()
{
   fragmentColor = vertexColor;
   gl_Position = rotation * position;
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

# Use PyOpenLG's compile shader programs, which simplify this task.
# Assign the compiled program to theShaders.
def initializeShaders():
    global theShaders, positionAttrib, rotationUniform, colorAttrib
    theShaders = compileProgram(
        compileShader(strVertexShader, GL_VERTEX_SHADER),
        compileShader(strFragmentShader, GL_FRAGMENT_SHADER)
    )
    positionAttrib = glGetAttribLocation(theShaders, "position")
    rotationUniform = glGetUniformLocation(theShaders, "rotation")
    colorAttrib = glGetAttribLocation(theShaders, "vertexColor")
    print "Attribs:", positionAttrib, colorAttrib
    print "Uniforms:", rotationUniform

# Vertex Data
#
# Put positions and colors in the same array, use a single buffer
triangleVertices = N.array([
    0.0, 0.75, 0.0, 1.0,
    1.0, 0.0, 0.0, 1.0,
    -0.75, -0.75, 0.0, 1.0,
    0.0, 1.0, 0.0, 1.0,
    0.75, -0.75, 0.0, 1.0,
    0.0, 0.0, 1.0, 1.0], dtype=N.float32)

vertexComponents = 8

# 3 indices into the buffer per triangle
# use unsigned short (16 bit) integers, usually plenty
triangleElements = N.array((0,1,2),dtype=N.uint16)

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
    vertexBuffer = getFloatBuffer(triangleVertices)
    elementBuffer = getElementBuffer(triangleElements)

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

# Called to redraw the contents of the window
def display(time):
    
    # Clear the display
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)

    # Set the shader program
    glUseProgram(theShaders)
    
    # compute rotation matrix:
    s = N.sin(time)
    c = N.cos(time)
    rot = N.array(((c,-s,0,0),
                    (s,c,0,0),
                    (0,0,1,0),
                    (0,0,0,1)), dtype=N.float32)
    # send rotation matrix to the shader program
    glUniformMatrix4fv(rotationUniform, 1, GL_TRUE, rot)
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
    glDrawElements(GL_TRIANGLES, len(triangleElements)*sizeOfShort,
                   GL_UNSIGNED_SHORT, c_void_p(0))
    

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
        time += 0.01
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

