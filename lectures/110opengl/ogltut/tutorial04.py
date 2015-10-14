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
    glDepthFunc(GL_LESS)
 
    # make vertex array
    VertexArrayID = glGenVertexArrays(1)
    glBindVertexArray(VertexArrayID)
   
    # compile shaders
    vertexShader = loadFile(os.path.join("shaders","TransformVertexShader04.vertexshader"))
    fragmentShader = loadFile(os.path.join("shaders","ColorFragmentShader.fragmentshader"))
    programID = compileShaderProgram(vertexShader, fragmentShader)

    # get handle for "MVP" uniform
    MatrixID = glGetUniformLocation(programID, "MVP")
    # projection matrix
    Projection = perspective(45.0, 4.0/3.0, 0.1, 100.0)
    # view matrix
    View = lookAt((4,3,-3), (0,0,0), (0,1,0))
    # model matrix
    Model = N.identity(4,dtype=N.float32)

    MVP = N.dot(Projection, N.dot(View, Model))
    MVP = N.array(MVP, dtype=N.float32)

    # fill data array
    g_vertex_buffer_data = N.array((-1,-1,0,
                                    1,-1,0,
                                    0.5,1,0),dtype=N.float32)
    b,l,f = -1,-1,-1
    t,r,n = 1,1,1
    bln = [b,l,n]
    blf = [b,l,f]
    brn = [b,r,n]
    brf = [b,r,f]
    tln = [t,l,n]
    tlf = [t,l,f]
    trn = [t,r,n]
    trf = [t,r,f]
    bot = bln+blf+brn + brn+blf+brf
    top = tln+tlf+trn + trn+tlf+trf
    left = bln+blf+tlf + bln+tlf+tln
    right = brn+trf+brf + brn+trn+trf
    front = bln+tln+trn + bln+trn+brn
    back = blf+trf+tlf + blf+brf+trf
    
    g_vertex_buffer_data = vec(bot+top+front+back+left+right)   
    g_color_buffer_data = vec([N.random.random() for x in range(len(g_vertex_buffer_data))])
    g_color_buffer_data = N.copy(g_vertex_buffer_data)*0.5 + 0.5
    
    # vertex buffer
    vertexbuffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer)
    glBufferData(GL_ARRAY_BUFFER, g_vertex_buffer_data, GL_STATIC_DRAW)
    # color buffer
    colorbuffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, colorbuffer)
    glBufferData(GL_ARRAY_BUFFER, g_color_buffer_data, GL_STATIC_DRAW)

    
    # find IDs for buffers
    positionID = glGetAttribLocation(programID, "vertexPosition_modelspace")
    colorID = glGetAttribLocation(programID, "vertexColor")
    print "positionID, colorID:", positionID, colorID

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

        # don't need to bind this VAO, since it's the
        # only one in the whole program, but the next
        # command requires some VAO, so it's nice to
        # document which one it is
        glBindVertexArray(VertexArrayID)
        # disable after drawing command
        glEnableVertexAttribArray(positionID)
        glEnableVertexAttribArray(colorID)

        # 1st attribute buffer: vertices
        glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer)
        glVertexAttribPointer(
            positionID,             # attrib 0, no reason
            3,             # size
            GL_FLOAT,      # type
            GL_FALSE,      # normalized?
            0,             # stride
            c_void_p(0)    # array buffer offset
            )
        # 2nd attribute buffer: colors
        glBindBuffer(GL_ARRAY_BUFFER, colorbuffer)
        glVertexAttribPointer(
            colorID,
            3,
            GL_FLOAT,
            GL_FALSE,
            0,
            c_void_p(0))
        # draw the triangle
        glDrawArrays(GL_TRIANGLES, 0, 12*3) # 3 indices starting at 0
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)

        # swap buffers
        pygame.display.flip()
        
    glDeleteProgram(programID)
    

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
