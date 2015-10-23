import os
import numpy as N
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
from databuffer import DataBuffer

class Cylinder():
    def __init__(self,
                 height = 16.0,
                 radius = 1.5,
                 vertShader = 'knotvertex.vs',
                 fragShader = 'knotfragment.fs',
                 shaderPositionName = 'position',
                 shaderNormalName = 'normal',
                 shaderTexcoordName = 'texcoord'):
        self.height = height
        self.radius = radius
        with open(os.path.join(os.getcwd(), vertShader)) as fp:
            vert = fp.read()
        with open(os.path.join(os.getcwd(), fragShader)) as fp:
            frag = fp.read()
        try:
            self.program = compileProgram(
                compileShader(vert, GL_VERTEX_SHADER),
                compileShader(frag, GL_FRAGMENT_SHADER))
        except RuntimeError as rte:
            print rte[0]
            raise
        self.positionLocation = glGetAttribLocation(self.program,
                                                    shaderPositionName)
        self.normalLocation = glGetAttribLocation(self.program,
                                                  shaderNormalName)
        self.texcoordLocation = glGetAttribLocation(self.program,
                                                    shaderTexcoordName)
        self.makeDataBuffers()

    def makeDataBuffers(self):
        positions = []
        normals = []
        texcoords = []
        for angle in N.arange(0.0, 2.01*N.pi, 0.1*N.pi):
            s = N.sin(angle)
            c = N.cos(angle)
            r = self.radius
            h = self.height
            positions.extend((0.5*r*s,   h+1.0, 0.5*r*c, 1.0))
            positions.extend((r*s, -1.0, r*c, 1.0))
            normals.extend((s, 0.0, c, 0.0))
            normals.extend((s, 0.0, c, 0.0))
            texcoords.extend((4*angle/N.pi,   h))
            texcoords.extend((4*angle/N.pi, 0.0))
        self.n = len(positions)/4
        self.positions = DataBuffer(positions, 4, self.positionLocation, 0, 4)
        self.normals = DataBuffer(normals, 4, self.normalLocation, 0, 4)
        self.texcoords = DataBuffer(texcoords, 2, self.texcoordLocation, 0, 2)

    def draw(self, uniforms1f, uniforms4fv, uniformMatrices):
        glUseProgram(self.program)
        for a in uniforms1f:
            loc = glGetUniformLocation(self.program, a)
            glUniform1f(loc, uniforms1f[a])
        for a in uniforms4fv:
            loc = glGetUniformLocation(self.program, a)
            glUniform4fv(loc, 1, uniforms4fv[a])
        for a in uniformMatrices:
            loc = glGetUniformLocation(self.program, a)
            glUniformMatrix4fv(loc, 1, True, uniformMatrices[a])
        bufs = (self.positions, self.normals, self.texcoords)
        for buf in bufs: buf.Start()
        glDrawArrays(GL_TRIANGLE_STRIP, 0, self.n)
        for buf in bufs: buf.Stop()
        glUseProgram(0)
        
        
            
        

        
            
            
        
        
                 
