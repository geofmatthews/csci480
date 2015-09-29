# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 09:07:41 2014

@author: matthews
"""

import os, pygame
from pygame.locals import *
import random
import numpy as np

if __name__ == "__main__":
    main_dir = os.getcwd() 
else:
    main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

def handleInput(screen):
    #Handle Input Events
    for event in pygame.event.get():
        if event.type == QUIT:
            return True
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return True
            elif event.key == K_s:
                pygame.event.set_blocked(KEYDOWN|KEYUP)
                fname = raw_input("File name?  ")
                pygame.event.set_blocked(0)
                pygame.image.save(screen,fname)
    return False

def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
#Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('Colors!')

#Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((64, 128, 255))

#Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

#Prepare Game Objects
    clock = pygame.time.Clock()

    going = True
    pixelsize = 256 # power of 2
    width, height = screen.get_size()
    # main loop
    while going:
        going = not(handleInput(screen))
        # start drawing loop
        while pixelsize > 0:
            print(pixelsize)
            clock.tick(1)
            for x in range(0,width,pixelsize):
                xx = x/float(width)
                for y in range(0,height,pixelsize):
                    #clock.tick(2)
                    yy = y/float(height)
                    # draw into background surface
                    r = random.randint(0,255)
                    color = (r,r,r)
                    color = [int(255*n) for n in (xx,yy,1-xx)]
                    color = 255*np.array((xx,yy,1-xx))
                    background.fill(color, ((x,y),(pixelsize,pixelsize)))
                    
                    #draw background into screen
                    screen.blit(background, (0,0))
                    pygame.display.flip()
                    if handleInput(screen):
                        return
                            
            pixelsize /= 2



#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
