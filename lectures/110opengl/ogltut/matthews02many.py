# -*- coding: utf-8 -*-
import os
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import pygame
from pygame.locals import *
import numpy as N
from ctypes import c_void_p

from transforms import *
from controls import *
from texture import loadTexture
from shaders import loadProgram
from psurfaceindexed import *
from drawable import *

def main ():
    # pygame initialization
    pygame.init()
    screen = pygame.display.set_mode((640,480), OPENGL|DOUBLEBUF)
    clock = pygame.time.Clock()

    # OpenGL initializations
    glClearColor(0.0,0.0,0.4,0.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    # cull triangles facing away from camera
    #glEnable(GL_CULL_FACE)
 
    # make vertex array
    VertexArrayID = glGenVertexArrays(1)
    glBindVertexArray(VertexArrayID)
   
    # compile shaders
    programID = loadProgram(
        os.path.join("shaders","shader05.vert"),
        os.path.join("shaders","shader05.frag")
        )
    print "programID:", programID
    # get handle for "MVP" uniform
    ViewMatrixID = glGetUniformLocation(programID, "V")
    ModelMatrixID = glGetUniformLocation(programID, "M")
    ProjectionMatrixID = glGetUniformLocation(programID, "P")
    print "P,V,M:",ProjectionMatrixID,ViewMatrixID,ModelMatrixID
    # texture
    Texture01 = loadTexture(os.path.join("images","texture_earth_clouds.jpg"))
    Texture02 = loadTexture(os.path.join("images","grid.png"))
    # get a handle
    TextureID = glGetUniformLocation(programID, "myTextureSampler")
    print "TextureID:", TextureID

    # vertex, normal, and texture uv data:
    vertNormUVData, vertNormUVIndices = sphere(1,32,64)
    # 4 point coords, 4 norm coords, 2 uvs:
    numberOfVertices = len(vertNormUVIndices)
    print "N Triangles:", numberOfVertices/3
    
    # vertex buffer for points, norms, uvs
    vertNormUVBuffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertNormUVBuffer)
    glBufferData(GL_ARRAY_BUFFER, vertNormUVData, GL_STATIC_DRAW)
    # vertex buffer for indices
    vertNormUVIndexBuffer = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, vertNormUVIndexBuffer)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, vertNormUVIndices, GL_STATIC_DRAW)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    # get handle for light position
    glUseProgram(programID)
    LightID = glGetUniformLocation(programID, "lightDirection")
    print "LightID:", LightID

    # get attribute locations
    PositionID = glGetAttribLocation(programID, "positionBuffer")
    NormalID = glGetAttribLocation(programID, "normalBuffer")
    uvID = glGetAttribLocation(programID, "uvBuffer")
    print "pos, norm, uv:", PositionID, NormalID, uvID

    # control object
    eye = vec((1,2,3))
    focus = vec((0,0,0))
    control = Control(pos=eye,
                      fwd=focus-eye)

    # drawable objects
    globe = Drawable(control,
                     programID,
                     ProjectionMatrixID,
                     ViewMatrixID,
                     ModelMatrixID,
                     TextureID,
                     Texture01,
                     vertNormUVBuffer,
                     vertNormUVIndexBuffer,
                     PositionID,
                     NormalID,
                     uvID,
                     LightID,
                     numberOfVertices)
    
    ball = Drawable(control,
                     programID,
                     ProjectionMatrixID,
                     ViewMatrixID,
                     ModelMatrixID,
                     TextureID,
                     Texture02, # different texture, all else the same here
                     vertNormUVBuffer,
                     vertNormUVIndexBuffer,
                     PositionID,
                     NormalID,
                     uvID,
                     LightID,
                     numberOfVertices)
                     
    
    lightDirection = normalize(vec((5,5,1,0)))
    time = 0.0
    running = True
    while running:
        clock.tick(30)
        time += 0.0333
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYUP and event.key == K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                control.handleMouseButton(event.button)
        control.handleMouseMotion()
        control.handleKeyboard()

        # draw into opengl context
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # compute MVP
        ProjectionMatrix = control.getProjectionMatrix()
        ViewMatrix = control.getViewMatrix()
        ModelMatrix = control.getModelMatrix()

        # draw my objects
        globe.Draw(ModelMatrix,
                   ViewMatrix,
                   ProjectionMatrix,
                   time,
                   lightDirection)
        ball.Draw(translationMatrix(1,1,-1), # static model matrix
                  ViewMatrix,
                  ProjectionMatrix,
                  time,
                  lightDirection)
        
        # swap buffers
        pygame.display.flip()
        
    glDeleteProgram(programID)

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
