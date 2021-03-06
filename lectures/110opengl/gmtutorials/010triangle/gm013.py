# Add a rotation matrix

from ctypes import c_void_p

from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram

import pygame
from pygame.locals import *
import numpy as N

# We will be sending C objects to the graphics card, so we need
# some help making sure python sends the right thing.
# The ctypes module provides a way to create a null pointer:
null = c_void_p(0)

# Sizes in OpenGL are bytes.  Since we're going to use 32 bit
# floats, provided by numpy, we'll need to tell OpenGL how big
# they are:
sizeOfFloat = 4

# The vertex shader has one input, the position of the vertex.
# It needs to have one output, also the position of the vertex.
# This is a simple passthrough shader.
strVertexShader = """
#version 330
in vec4 position;
uniform mat4 rotation;
void main()
{
   gl_Position = rotation * position;
}
"""

# The fragment shader needs to have one output, the color
# of the fragment.  Here we set it to white.
strFragmentShader = """
#version 330
out vec4 outputColor;
void main()
{
   outputColor = vec4(1.0f, 1.0f, 1.0f, 1.0f);
}
"""

# Use PyOpenLG's compile shader programs, which simplify this task.
# Assign the compiled program to theShaders.
def initializeShaders():
    global theShaders, positionAttrib, rotationAttrib
    theShaders = compileProgram(
        compileShader(strVertexShader, GL_VERTEX_SHADER),
        compileShader(strFragmentShader, GL_FRAGMENT_SHADER)
    )
    positionAttrib = glGetAttribLocation(theShaders, "position")
    rotationAttrib = glGetUniformLocation(theShaders, "rotation")
    print "Attribs:", positionAttrib, rotationAttrib

# Vertex Data
#
# Three vertices of a triangle, with an x,y,z & w for each.
vertexPositions = N.array([
    0.0, 0.75, 0.0, 1.0,
    -0.75, -0.75, 0.0, 1.0,
    0.75, -0.75, 0.0, 1.0], dtype=N.float32) 

# number of components per point,  4 since we're using homogeneous
# 3d points.  This helps figuring out how many triangles we're
# drawing, with len(vertexPositions)/vertexComponents
vertexComponents = 4


def initializeVertexBuffer():
    global positionBufferObject
    positionBufferObject = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, positionBufferObject)
    glBufferData(GL_ARRAY_BUFFER, vertexPositions, GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

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
    glUniformMatrix4fv(rotationAttrib, # attrib location
                       1,              # how many are we sending?
                       GL_TRUE,        # row-major?
                       rot             # the array
                       )

    # Use the buffered data
    glBindBuffer(GL_ARRAY_BUFFER, positionBufferObject)
    
    # Tell the shader program which attribute to use for this buffer
    glEnableVertexAttribArray(positionAttrib)
    
    # Tell the shader program what the data in the buffer look like
    glVertexAttribPointer(positionAttrib,   # attrib location
                          vertexComponents, # elements per vertex
                          GL_FLOAT,         # type of element
                          GL_FALSE,         # normalize 0-256 to 0.0-1.0?
                          0,                # stride
                          c_void_p(0)       # offset
                          )
    
    # Use that data to draw triangles
    glDrawArrays(GL_TRIANGLES, 0, len(vertexPositions) / vertexComponents)
    
    # Stop using that buffered data
    glDisableVertexAttribArray(0)

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

