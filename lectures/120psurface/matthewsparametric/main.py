#!/usr/bin/env python
"""Direct render of parametric surfaces in python and pygame
Geoffrey Matthews, 2011"""

#Import Modules
import os, pygame
from pygame.locals import *
from pygame.compat import geterror

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

import numpy as N

from light import Light
from parametricsurface import *
from recursivesurface import *
from camera import Camera
from scene import Scene
from transform import *

if __name__ == "__main__":
    main_dir = os.getcwd() 
else:
    main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

sz = 3
if sz == 0:
    SCREENSIZE = (80,60)
elif sz == 1:
    SCREENSIZE = (160,120)
elif sz == 2:
    SCREENSIZE = (320,240)
else:
    SCREENSIZE = (640,480)

SCREENSIZE = N.array(SCREENSIZE)

def standardLights():
    return [Light((100,100,100,1), (.7,0,0)),
            Light((100,0,100,1), (0,.7,0)),
            Light((0,100,100,1), (0,0,.7))]

def singleLight():
    return [Light((100,100,100,1), (1,1,1))]

def headLight():
    return [Light((0,0,100,1), (1,1,1))]

def selectLights(n):
    if n==0:
        return standardLights()
    elif n == 1:
        return headLight()
    else:
        return singleLight()

MySurfaces = [PCheckerBox(),
              PTajSurface(),
              PTajInset(),
             PSinCos(),
             PSinc(),
             PCosDist(),
             PConchoid(),
             PSphere(),
             PTorus(),
             PGroup([PSphere(transform=scale(3,3,5)),
                     PTorus(transform=scale(1.25,1.25,0.25))]),
             RSphere()]
    
def selectSurf(n):
    global MySurfaces
    if 0 <= n and n < len(MySurfaces):
        return MySurfaces[n]
    else:
        newsurfs = []
        for i in range(10):
            trans = scaleU(0.5)
            trans = N.dot(translation(N.random.uniform(-5.0,5.0),
                                      N.random.uniform(-5.0,5.0),
                                      0), trans)
            s = PSphere(transform=trans)
            for dummy in range(1):
                s.lessDetail()
            newsurfs.append(s)
        return PGroup(newsurfs)

def simpleScene():    
    myScene = Scene(selectSurf(1), selectLights(1), Camera())
    return myScene

def main():
    global myScene
#Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode(SCREENSIZE)
    center = 0.5*makeVector(SCREENSIZE)
    pygame.display.set_caption('Matthews Parametric Surfaces in Python')
    
#Create The Backgound
    myScene = simpleScene()
    rendering = pygame.Surface(SCREENSIZE)
    rendering.fill((64,128,255))
    myScene.render(rendering, screen)
    
#Display The Background
    screen.blit(rendering, (0,0))
    pygame.display.flip()

#Prepare Game Objects
    clock = pygame.time.Clock()

    #Main Loop
    going = True
    oldVec = newVec = None
    frames = 0
    oldTime = pygame.time.get_ticks()
    lightToggle = 0
    lineToggle = False
    while going:
        clock.tick(30)

        #Handle Input Events
                elif event.key == K_c:
                    myScene.camera = Camera()
                elif event.key == K_l:
                    myScene.lights = selectLights(lightToggle)
                    lightToggle = (lightToggle + 1) % 3
                elif event.key == K_k:
                    myScene.renderLines = lineToggle
                    lineToggle = not(lineToggle)
                elif event.key == K_j:
                    myScene.sortPolys = not(myScene.sortPolys)
                elif event.key == K_0:
                    myScene.psurf = selectSurf(0)
                elif event.key == K_1:
                    myScene.psurf = selectSurf(1)
                elif event.key == K_2:
                    myScene.psurf = selectSurf(2)
                elif event.key == K_3:
                    myScene.psurf = selectSurf(3)
                elif event.key == K_4:
                    myScene.psurf = selectSurf(4)
                elif event.key == K_5:
                    myScene.psurf = selectSurf(5)
                elif event.key == K_6:
                    myScene.psurf = selectSurf(6)
                elif event.key == K_7:
                    myScene.psurf = selectSurf(7)
                elif event.key == K_8:
                    myScene.psurf = selectSurf(8)
                elif event.key == K_9:
                    myScene.psurf = selectSurf(9)
                elif event.key == K_o:
                    myScene.psurf.moreDetail()
                elif event.key == K_p:
                    myScene.psurf.lessDetail()
                elif event.key == K_F1:
                    pygame.event.set_blocked(KEYDOWN|KEYUP)
                    fname = raw_input("File name?  ")
                    pygame.event.set_blocked(0)
                    pygame.image.save(rendering,fname)

        #Input polling:
        pressed = pygame.mouse.get_pressed()
        if not(pressed[0]):
            newVec = None
            newMouse = None
        else:
            w,h = SCREENSIZE
            oldVec = newVec
            oldMouse = newMouse
            newMouse = makeVector(pygame.mouse.get_pos())
            if oldMouse != None:
                pass
                # trackball code here

        pressed = pygame.key.get_pressed()
        # Dolly-Zoom
        if pressed[K_d]:
            myScene.camera.dollyZoom(0.25)
        if pressed[K_f]:
            myScene.camera.dollyZoom(-0.25)

        # Truck, Dolly, Pedestal
        if pressed[K_q]:
            myScene.camera.leftMultiply(translation(0.1,0,0))   
        if pressed[K_w]:
            myScene.camera.leftMultiply(translation(-0.1,0,0))   
        if pressed[K_a]:
            myScene.camera.leftMultiply(translation(0,0.1,0))   
        if pressed[K_s]:
            myScene.camera.leftMultiply(translation(0,-0.1,0))   
        if pressed[K_z]:
            myScene.camera.leftMultiply(translation(0,0,0.1))   
        if pressed[K_x]:
            myScene.camera.leftMultiply(translation(0,0,-0.1))         

        # Rotate object, pre-multiply
        if pressed[K_DOWN]:
            myScene.camera.rightMultiply(rotationX(0.01*N.pi))
        if pressed[K_UP]:
            myScene.camera.rightMultiply(rotationX(-0.01*N.pi))
        if pressed[K_COMMA]:
            myScene.camera.rightMultiply(rotationY(0.01*N.pi))
        if pressed[K_PERIOD]:
            myScene.camera.rightMultiply(rotationY(-0.01*N.pi))
        if pressed[K_RIGHT]:
            myScene.camera.rightMultiply(rotationZ(0.01*N.pi))
        if pressed[K_LEFT]:
            myScene.camera.rightMultiply(rotationZ(-0.01*N.pi))

        # Semi-random axis
        if pressed[K_m]:
            myScene.camera.rightMultiply(rotationAxis(0.01*N.pi, (1,1,1,0)))          
                
        #Draw Everything
        frames += 1
        quads = myScene.render(rendering, screen)
        seconds = 0.001*(pygame.time.get_ticks()-oldTime)
        if seconds > 5.0:
            print quads, " quads rendered ",
            print round(1000.0*frames/float(pygame.time.get_ticks()-oldTime), 2), "fps"
            frames = 0
            oldTime = pygame.time.get_ticks()
        screen.blit(rendering, (0,0))
        pygame.display.flip()

    pygame.quit()

#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
