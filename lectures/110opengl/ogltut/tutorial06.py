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
from controls import *
from texture import loadTexture
from shaders import loadProgram

    
def main ():
    # pygame initialization
    pygame.init()
    screen = pygame.display.set_mode((640,480), OPENGL|DOUBLEBUF)
    clock = pygame.time.Clock()

    # OpenGL initializations
    glClearColor(0.0,0.0,0.4,0.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
 
    # make vertex array
    VertexArrayID = glGenVertexArrays(1)
    glBindVertexArray(VertexArrayID)
   
    # compile shaders
    programID = loadProgram(
        os.path.join("shaders","TransformVertexShader.vertexshader"),
        os.path.join("shaders","TextureFragmentShader.fragmentshader")
        )

    # get handle for "MVP" uniform
    MatrixID = glGetUniformLocation(programID, "MVP")
    control = Control()
    # projection matrix
    Projection = control.getProjectionMatrix()
    # view matrix
    View = control.getViewMatrix()
    # model matrix
    Model = control.getModelMatrix()

    MVP = N.dot(Projection, N.dot(View, Model))
    MVP = N.array(MVP, dtype=N.float32)
    
    g_vertex_buffer_data = vec([ 
		-1.0,-1.0,-1.0,
		-1.0,-1.0, 1.0,
		-1.0, 1.0, 1.0,
		 1.0, 1.0,-1.0,
		-1.0,-1.0,-1.0,
		-1.0, 1.0,-1.0,
		 1.0,-1.0, 1.0,
		-1.0,-1.0,-1.0,
		 1.0,-1.0,-1.0,
		 1.0, 1.0,-1.0,
		 1.0,-1.0,-1.0,
		-1.0,-1.0,-1.0,
		-1.0,-1.0,-1.0,
		-1.0, 1.0, 1.0,
		-1.0, 1.0,-1.0,
		 1.0,-1.0, 1.0,
		-1.0,-1.0, 1.0,
		-1.0,-1.0,-1.0,
		-1.0, 1.0, 1.0,
		-1.0,-1.0, 1.0,
		 1.0,-1.0, 1.0,
		 1.0, 1.0, 1.0,
		 1.0,-1.0,-1.0,
		 1.0, 1.0,-1.0,
		 1.0,-1.0,-1.0,
		 1.0, 1.0, 1.0,
		 1.0,-1.0, 1.0,
		 1.0, 1.0, 1.0,
		 1.0, 1.0,-1.0,
		-1.0, 1.0,-1.0,
		 1.0, 1.0, 1.0,
		-1.0, 1.0,-1.0,
		-1.0, 1.0, 1.0,
		 1.0, 1.0, 1.0,
		-1.0, 1.0, 1.0,
		 1.0,-1.0, 1.0
        ])

    g_uv_buffer_data = vec([
		0.000059, 1.0-0.000004, 
		0.000103, 1.0-0.336048, 
		0.335973, 1.0-0.335903, 
		1.000023, 1.0-0.000013, 
		0.667979, 1.0-0.335851, 
		0.999958, 1.0-0.336064, 
		0.667979, 1.0-0.335851, 
		0.336024, 1.0-0.671877, 
		0.667969, 1.0-0.671889, 
		1.000023, 1.0-0.000013, 
		0.668104, 1.0-0.000013,  
		0.667979, 1.0-0.335851, 
		0.000059, 1.0-0.000004, 
		0.335973, 1.0-0.335903, 
		0.336098, 1.0-0.000071, 
		0.667979, 1.0-0.335851, 
		0.335973, 1.0-0.335903, 
		0.336024, 1.0-0.671877, 
		1.000004, 1.0-0.671847, 
		0.999958, 1.0-0.336064, 
		0.667979, 1.0-0.335851, 
		0.668104, 1.0-0.000013, 
		0.335973, 1.0-0.335903, 
		0.667979, 1.0-0.335851, 
		0.335973, 1.0-0.335903, 
		0.668104, 1.0-0.000013, 
		0.336098, 1.0-0.000071, 
		0.000103, 1.0-0.336048, 
		0.000004, 1.0-0.671870, 
		0.336024, 1.0-0.671877, 
		0.000103, 1.0-0.336048, 
		0.336024, 1.0-0.671877, 
		0.335973, 1.0-0.335903, 
		0.667969, 1.0-0.671889, 
		1.000004, 1.0-0.671847, 
		0.667979, 1.0-0.335851
	])

    # vertex buffer
    vertexbuffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer)
    glBufferData(GL_ARRAY_BUFFER, g_vertex_buffer_data, GL_STATIC_DRAW)
    # color buffer
    uvbuffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, uvbuffer)
    glBufferData(GL_ARRAY_BUFFER, g_uv_buffer_data, GL_STATIC_DRAW)
    # get IDs from program
    positionID = glGetAttribLocation(programID, "vertexPosition_modelspace")
    uvID = glGetAttribLocation(programID, "vertexUV")


    # texture
    Texture = loadTexture(os.path.join("images","uvtemplate.tga"))
    # get a handle
    TextureID = glGetUniformLocation(programID, "myTextureSampler")
    
    running = True
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYUP and event.key == K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                control.handleMouseButton(event.button)
        control.handleMouseMotion()
        control.handleKeyboard()

        # compute MVP
        Projection = control.getProjectionMatrix()
        View = control.getViewMatrix()
        Model = control.getModelMatrix()
        MVP = N.dot(Projection, N.dot(View, Model))
        MVP = N.array(MVP, dtype=N.float32)

        # draw into opengl context
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # use our shader
        glUseProgram(programID)
        # send our transform to the shader
        glUniformMatrix4fv(MatrixID, 1, GL_TRUE, MVP)       
        # GL_TRUE: transpose the matrix for opengl column major order
        
        # bind our texture to texture unit
        textureUnit = 4
        glActiveTexture(GL_TEXTURE0 + textureUnit)
        # use our texture data
        glBindTexture(GL_TEXTURE_2D, Texture)
        # set our sampler to use texture unit
        glUniform1i(TextureID, textureUnit)
        
        # 1st attribute buffer:  vertices
        glEnableVertexAttribArray(positionID)
        glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer)
        bytesPerFloat = 4
        glVertexAttribPointer(
            positionID,      # attrib 0, no reason
            3,               # size
            GL_FLOAT,        # type
            GL_FALSE,        # normalized?
            3*bytesPerFloat, # stride, can be 0 if nothing else in buffer
            c_void_p(0)      # array buffer offset
            )
        # 2nd attribute buffer: uvs
        glEnableVertexAttribArray(uvID)
        glBindBuffer(GL_ARRAY_BUFFER, uvbuffer)
        glVertexAttribPointer(
            uvID,
            2,
            GL_FLOAT,
            GL_FALSE,
            2*bytesPerFloat,
            c_void_p(0))
        # draw the triangle
        glDrawArrays(GL_TRIANGLES, 0, 12*3) 
        
        glDisableVertexAttribArray(positionID)
        glDisableVertexAttribArray(uvID)

        # swap buffers
        pygame.display.flip()
        
    glDeleteProgram(programID)

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
