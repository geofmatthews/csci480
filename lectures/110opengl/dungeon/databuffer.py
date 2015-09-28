import numpy as N
from ctypes import c_void_p

from OpenGL.GL import *

class DataBuffer():
    def __init__(self, data, components, location, offset=0, stride=4):
        bytesPerFloat = 4
        self.data = N.array(data, dtype=N.float32)
        self.components = components
        self.offset = c_void_p(offset*bytesPerFloat)
        self.stride = stride*bytesPerFloat
        self.location = location
        
        self.bufferObject = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.bufferObject)
        glBufferData(GL_ARRAY_BUFFER, self.data, GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def Start(self):
        glEnableVertexAttribArray(self.location)
        glBindBuffer(GL_ARRAY_BUFFER, self.bufferObject)
        glVertexAttribPointer(self.location, self.components,
                              GL_FLOAT, False, self.stride, self.offset)

    def Stop(self):
        glDisableVertexAttribArray(self.location)
