#Note:  since normals are flat across the cube, we don't interpolate
# surface normals (Phong-style) over the primitives.
# We DO interpolate the eye and light vectors for the frag shader

import os

from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram

import pygame
from pygame.locals import *

import numpy as N
from ctypes import c_void_p

from transforms import *
from databuffer import DataBuffer
from cylinder import Cylinder
from dome import Dome
from floor import Floor
from frame import Frame

def loadFile(filename):
    with open(os.path.join(os.getcwd(), filename)) as fp:
        return fp.read()

def display():
    global time, light, frame, cyl, dome, fogEnd, pillarSeparation, pillarN, pMatrix
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    vMatrix =  frame.matrix

    xoffset = pillarSeparation*N.floor(frame.translation[0][3]/pillarSeparation)
    zoffset = pillarSeparation*N.floor(frame.translation[2][3]/pillarSeparation)

    trans = translationMatrix(-xoffset,0,-zoffset)
    floor.draw({'time':time,
                'useKnot':0.0,
                'fogEnd':fogEnd},
               {},
               {'vMatrix':vMatrix,
                'pMatrix':pMatrix,
                'mMatrix':trans})
    for row in N.arange(-pillarN*pillarSeparation, pillarN*pillarSeparation, pillarSeparation):
        trans[0][3] = row-xoffset
        for col in N.arange(-pillarN*pillarSeparation, pillarN*pillarSeparation, pillarSeparation):
            trans[2][3] = col-zoffset
            cyl.draw({'time':time,
                      'useKnot':1.0,
                      'fogEnd':fogEnd},
                     {},
                     {'vMatrix':vMatrix,
                      'pMatrix':pMatrix,
                      'mMatrix':trans})
            dome.draw({'time':time, 'useKnot':0.0, 'fogEnd':fogEnd},
                     {},
                     {'vMatrix':vMatrix,
                      'pMatrix':pMatrix,
                      'mMatrix':trans})
            
def initializeVertexArray():
    # Must have a vertex array object to use vertex buffer objects.
    # Just one will do:
    global vao_array
    vao_array = N.zeros(1, dtype=N.uint)
    #glGenVertexArrays(1, vao_array)
    vao_array = glGenVertexArrays(1)
    glBindVertexArray(vao_array)


# Must be called after we have an OpenGL context, i.e. after the pygame
# window is created
def init():
    global  cubeBuffers,textureBuffers, cyl, dome, floor, pillarN, pillarSeparation, pMatrix

    pMatrix = projectionMatrix(0.1, 1000.0, .10, 0.075)
    pillarN = 6
    pillarSeparation = 20.0
    cyl = Cylinder()
    dome = Dome(width=pillarSeparation)
    floor = Floor()
    initializeVertexArray()    
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
       
def main():
    global window, time, light, inc, whichTex, frame, fogEnd
    pygame.init()
    screen = pygame.display.set_mode((640,480), OPENGL|DOUBLEBUF)#|FULLSCREEN)
    pygame.display.set_caption('The Jade Palace')

    screentoggle = False
    clock = pygame.time.Clock()
    time = 0.0
    light = N.array((10,10,10,0), dtype = N.float32)
    inc = 0.05
    whichTex = 0
    init()
    frame = Frame()
    fogEnd = 150.0
    while True:     
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYUP and event.key == K_ESCAPE:
                return
            if event.type == KEYDOWN:
                if event.key == K_s:
                    if inc == 0.0:
                        inc = 0.2
                    else:
                        inc = 0.0

        pressed = pygame.key.get_pressed()
        if pressed[K_UP]:
            frame.move(0.25)
        if pressed[K_DOWN]:
            frame.move(-0.25)
        if pressed[K_a]:
            frame.tilt(1.0)
        if pressed[K_z]:
            frame.tilt(-1.0)
        if pressed[K_LEFT]:
            if pressed[K_LSHIFT]:
                frame.strafe(0.25)
            else:
                frame.rotate(1.0)
        if pressed[K_RIGHT]:
            if pressed[K_LSHIFT]:
                frame.strafe(-0.25)
            else:
                frame.rotate(-1.0)
        if pressed[K_f]:
            fogEnd *= 1.1
        if pressed[K_v]:
            fogEnd *= 0.9
            
        clock.tick(30)
        time += inc
        display()
        pygame.display.flip()

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
