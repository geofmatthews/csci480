# -*- coding: utf-8 -*-
import os
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import compileShader, compileProgram
import pygame
from pygame.locals import *
import numpy as N
from ctypes import c_void_p

from transforms import *

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
    vertexShader = loadFile(os.path.join("shaders","SimpleTransform.vertexshader"))
    fragmentShader = loadFile(os.path.join("shaders","SingleColor.fragmentshader"))
    programID = compileShaderProgram(vertexShader, fragmentShader)

    # get handle for "MVP" uniform
    MatrixID = glGetUniformLocation(programID, "MVP")
    # projection matrix
    Projection = perspective(45.0, 4.0/3.0, 0.1, 100.0)
    #Projection = N.identity(4,dtype=N.float32)
    # view matrix
    View = lookAt((4,3,3), (0,0,0), (0,1,0))
    #View = lookAt((0,0,1), (0,0,0), (0,1,0))
    #View = N.identity(4,dtype=N.float32)
    # Model matrix
    Model = N.identity(4,dtype=N.float32)

    MVP = N.dot(Projection, N.dot(View, Model))
    MVP = N.array(MVP, dtype=N.float32)

    # make vertex array
    VertexArrayID = glGenVertexArrays(1)
    glBindVertexArray(VertexArrayID)

    # fill data array
    g_vertex_buffer_data = N.array((-1,-1,0,
                                    1,-1,0,
                                    0.5,1,0),dtype=N.float32)
    g_element_buffer_data = N.array((0,1,2),dtype=N.short)
    
    # vertex buffer
    vertexbuffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer)
    glBufferData(GL_ARRAY_BUFFER, g_vertex_buffer_data, GL_STATIC_DRAW)

    # find IDs for buffers
    positionID = glGetAttribLocation(programID, "vertexPosition_modelspace")
    
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
        # send our transform to the shader
        glUniformMatrix4fv(MatrixID, 1, GL_TRUE, MVP)
        # GL_TRUE: transpose the matrix for opengl column major order
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