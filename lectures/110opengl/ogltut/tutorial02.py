import os
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import pygame
from pygame.locals import *
import numpy as N
from ctypes import c_void_p

def loadFile(filename):
    with open(os.path.join(os.getcwd(), filename)) as fp:
        return fp.read()

def compileShaderProgram(vertexShader, fragmentShader):
    """
    Instead of calling OpenGL's shader compilation functions directly
    (glShaderSource, glCompileShader, etc), we use PyOpenGL's wrapper
    functions, which are much simpler to use.
    """
    myProgram = compileProgram(
        compileShader(vertexShader, GL_VERTEX_SHADER),
        compileShader(fragmentShader, GL_FRAGMENT_SHADER)
    )
    return myProgram


def main ():
    # pygame initialization
    pygame.init()
    screen = pygame.display.set_mode((1024,768), OPENGL|DOUBLEBUF)
    clock = pygame.time.Clock()

    # OpenGL initializations
    glClearColor(0.0,0.0,0.4,0.0)
    glEnable(GL_DEPTH_TEST)

    # compile shaders
    vertexShader = loadFile(os.path.join("shaders","SimpleVertexShader.vertexshader"))
    fragmentShader = loadFile(os.path.join("shaders","SimpleFragmentShader.fragmentshader"))
    programID = compileShaderProgram(vertexShader, fragmentShader)

    # Use a VAO
    # stores how vertex attributes are stored in the VBO's
    # useful if you want to rebind them again later
    VertexArrayID = glGenVertexArrays(1)
    glBindVertexArray(VertexArrayID)

    # fill data array
    g_vertex_buffer_data = N.array((-1,-1,0,
                                    1,-1,0,
                                    0.5,1,0),dtype=N.float32)
    # vertex buffer
    vertexbuffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer)
    glBufferData(GL_ARRAY_BUFFER, g_vertex_buffer_data, GL_STATIC_DRAW)

    running = True
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYUP and event.key == K_ESCAPE:
                running = False

        # draw into opengl context
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # use our shader
        glUseProgram(programID)
        # 1st attribute buffer:  vertices
        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer)
        glVertexAttribPointer(
            0,             # attrib 0, no reason
            3,             # size
            GL_FLOAT,      # type
            GL_FALSE,      # normalized?
            0,             # stride
            c_void_p(0)    # array buffer offset
            )
        # draw the triangle
        glDrawArrays(GL_TRIANGLES, 0, 3) # 3 indices starting at 0
        glDisableVertexAttribArray(0)

        # swap buffers
        pygame.display.flip()
        
    # vbo's and vao's are autodeleted by pyopengl
    glDeleteProgram(programID)

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()

