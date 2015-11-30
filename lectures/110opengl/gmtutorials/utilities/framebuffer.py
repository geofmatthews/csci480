# Create a framebuffer with color buffer and depth buffer,
# for multipass rendering effects.
# Some of this could be reused in multiple framebuffers,
# e.g. the depth buffer,
# but for simplicity we make each one separate.

from OpenGL.GL import *
from ctypes import c_void_p

def getFramebuffer(resolution = 512):
    # create a frame buffer and bind to it
    theFramebuffer = glGenFramebuffers(1)
    glBindFramebuffer(GL_FRAMEBUFFER, theFramebuffer)
    # create a texture to render into and bind to it
    theRenderedTexture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, theRenderedTexture)
    # fill with empty pixels (the last "0")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB,
                 resolution, resolution, 0, GL_RGB,
                 GL_UNSIGNED_BYTE, c_void_p(0))
    # filtering, needed
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    # now create a depth buffer and bind to it
    theDepthBuffer = glGenRenderbuffers(1)
    glBindRenderbuffer(GL_RENDERBUFFER, theDepthBuffer)
    glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT,
                          resolution, resolution)
    glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT,
                              GL_RENDERBUFFER, theDepthBuffer)
    # finally, configure our framebuffer
    # GL_COLOR_ATTACHMENT0 means we get colors from the default
    # output of the fragment shader (no shader changes needed)
    # with other color attachment points, a single shader
    # could render to different framebuffers in a single pass
    # query GL_MAX_COLOR_ATTACHMENTS to see how many are
    # supported by your graphics card
    glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0,
                         theRenderedTexture, 0)
    theDrawBuffers = [GL_COLOR_ATTACHMENT0]
    glDrawBuffers(1, theDrawBuffers)
    # check errors, necessary with pyopengl?
    if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
        raise StandardError("Frame buffer status no good.")
    return theFramebuffer
    
    
    
