import pygame
import os
from OpenGL.GL import *
from OpenGL.GLU import *

# This must be done after the opengl context is active

def loadTexture(filename):
    surf = pygame.image.load(os.path.join("textures", filename))
    data = pygame.image.tostring(surf, "RGBA", 1)
    textureID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textureID)
    # wrapmode            
    wrapMode = GL_REPEAT
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, wrapMode)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, wrapMode)
    # how to scale things
    minFilter = GL_LINEAR
    magFilter = GL_LINEAR
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, minFilter)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, magFilter)
    # send the data to the hardware
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
                 surf.get_width(),
                 surf.get_height(),
                 0, GL_RGBA, GL_UNSIGNED_BYTE, data)

    glBindTexture(GL_TEXTURE_2D, 0)
    return textureID
