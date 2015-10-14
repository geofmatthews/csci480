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
    
def loadTexture(filename):
    surf = pygame.image.load(filename)
    data = pygame.image.tostring(surf, "RGBX", 1)
    textureID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textureID)
    # wrapmode            
    wrapMode = GL_REPEAT
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, wrapMode)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, wrapMode)
    # how to scale things
    minFilter = GL_LINEAR
    magFilter = GL_NEAREST
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, minFilter)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, magFilter)
    # send the data to the hardware
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
                 surf.get_width(),
                 surf.get_height(),
                 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    
    glBindTexture(GL_TEXTURE_2D, 0)
    return textureID

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
    vertexShader = loadFile(os.path.join("shaders","TransformVertexShader.vertexshader"))
    fragmentShader = loadFile(os.path.join("shaders","TextureFragmentShader.fragmentshader"))
    programID = compileShaderProgram(vertexShader, fragmentShader)

    # get handle for "MVP" uniform
    MatrixID = glGetUniformLocation(programID, "MVP")
    # projection matrix
    Projection = perspective(45.0, 4.0/3.0, 0.1, 100.0)
    # view matrix
    View = lookAt((4,3,3), (0,0,0), (0,1,0))
    # model matrix
    Model = N.identity(4,dtype=N.float32)

    MVP = N.dot(Projection, N.dot(View, Model))
    MVP = N.array(MVP, dtype=N.float32)
    
    # fill data array
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
    
    bl = [0,0]
    br = [1,0]
    tl = [0,1]
    tr = [1,1]
    bot = bl+tl+br + br+tl+tr
    top = bl+tl+tr + br+tr+tl
    left = br+bl+tl + br+tl+tr
    right = bl+tr+br + bl+tl+tr
    front = bl+tl+tr + bl+tr+br
    back = br+tl+tr + br+bl+tl
    g_uv_buffer_data = vec(bot+top+front+back+left+right)
    
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
    Texture = loadTexture(os.path.join("images","grid.png"))
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
        glVertexAttribPointer(
            positionID,             # attrib 0, no reason
            3,             # size
            GL_FLOAT,      # type
            GL_FALSE,      # normalized?
            0,             # stride
            c_void_p(0)    # array buffer offset
            )
        # 2nd attribute buffer: uvs
        glEnableVertexAttribArray(uvID)
        glBindBuffer(GL_ARRAY_BUFFER, uvbuffer)
        glVertexAttribPointer(
            uvID,
            2,
            GL_FLOAT,
            GL_FALSE,
            0,
            c_void_p(0))
        # draw the triangle
        glDrawArrays(GL_TRIANGLES, 0, 12*3) # 3 indices starting at 0
        
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
