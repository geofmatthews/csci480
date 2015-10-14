# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 13:36:17 2014

@author: matthews
"""

import pygame
from pygame.locals import *

from transforms import *

class Control():
    def __init__(self,
                 pos = vec((5,4,5)),
                 fwd = vec((-5,-4,-5)), 
                 up = vec((0,1,0)),
                 fov = 45.0,
                 speed=0.1,
                 mouseSpeed = 0.001):
        self.pos = pos
        self.fwd = normalize(vec(fwd))
        self.up = normalize(vec(up) - N.dot(vec(up),fwd)*fwd)
        self.rt = N.cross(fwd,up)
        self.fov = fov
        self.speed = speed
        self.mouseSpeed = mouseSpeed
        self.computeRotation()
        self.modelPosition = vec((0,0,0))
        self.modelTranslation = N.identity(4,dtype=N.float32)
        self.modelRotation = 0.0
        self.modelPitch = 0.0

    def handleMouseButton(self, button):
        if button == 4:
            self.fov *= 1.1
        elif button == 5:
            self.fov *= 0.9

    def handleMouseMotion(self):
        pressed = pygame.mouse.get_pressed()
        if pressed[0]:
            self.computeRotation()
        elif pressed[2]:
            self.computeModelRotation()

    def computeModelRotation(self):
        speed = 0.01
        r,u = pygame.mouse.get_rel()
        r = min(r,20)
        r = max(r,-20)
        self.modelRotation -= r*0.005
        u = min(u,20)
        u = max(u,-20)
        self.modelPitch += u*0.005
        
    def computeRotation(self):       
        fwd = self.fwd
        rt = self.rt
        up = self.up
        r,u = pygame.mouse.get_rel()
        r = min(r,20)
        r = max(r,-20)
        u = min(u,20)
        u = max(u,-20)
        fwd += r*rt*self.mouseSpeed
        fwd += -u*up*self.mouseSpeed
        fwd = normalize(fwd)
        if fwd[0] != 0 or fwd[1] != 1 or fwd[2] != 0:
            up = vec((0,1,0))
        up = normalize(up - N.dot(up,fwd)*fwd)
        rt = N.cross(fwd,up)
        self.fwd = fwd
        self.rt = rt
        self.up = up

    def handleKeyboard(self):
        pressed = pygame.key.get_pressed()
        if pressed[K_w]:
            self.pos += self.speed*self.fwd
        elif pressed[K_s]:
            self.pos -= self.speed*self.fwd
        elif pressed[K_a]:
            self.pos -= self.speed*self.rt
        elif pressed[K_d]:
            self.pos += self.speed*self.rt
        elif pressed[K_t]:
            self.modelPosition[0] += self.speed
        elif pressed[K_y]:
            self.modelPosition[0] -= self.speed
        elif pressed[K_u]:
            self.modelPosition[1] += self.speed
        elif pressed[K_i]:
            self.modelPosition[1] -= self.speed
        elif pressed[K_o]:
            self.modelPosition[2] += self.speed
        elif pressed[K_p]:
            self.modelPosition[2] -= self.speed
            
    def getProjectionMatrix(self):
        self.fov = min(self.fov, 170)
        self.fov = max(self.fov, 5)
        return perspective(self.fov, 4.0/3.0, .1, 100.0)
        
    def getViewMatrix(self):
        return viewFromFrame(self.pos, self.fwd, self.rt, self.up)

    def getModelMatrix(self):
        p = self.modelPosition
        self.modelTranslation[0:3,3] = self.modelPosition
        rot = rotationYMatrix(self.modelRotation)
        pitch = rotationXMatrix(self.modelPitch)
        rotpitch = N.dot(pitch, rot)
        trans = self.modelTranslation
        return N.dot(trans,rotpitch)
    
    
    
                  
