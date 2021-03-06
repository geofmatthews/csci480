import os
import numpy as N
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
from databuffer import DataBuffer

class Floor():
    def __init__(self,
                 height = -0.5,
                 width = 100.0,
                 vertShader = 'knotvertex.vs',
                 fragShader = 'knotfragment.fs',
                 shaderPositionName = 'position',
                 shaderNormalName = 'normal',
                 shaderTexcoordName = 'texcoord'):
        self.height = height
        self.width = width
        
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

    def domeHeight(self,x,z):
        return self.height
    
    def quad(self,x,z,step):
        x1 = x+step
        z1 = z+step
        a = N.array((x,self.domeHeight(x,z),z),dtype=N.float32)
        b = N.array((x,self.domeHeight(x,z1),z1),dtype=N.float32)
        c = N.array((x1,self.domeHeight(x1,z1),z1),dtype=N.float32)
        d = N.array((x1,self.domeHeight(x1,z),z),dtype=N.float32)
        norm = N.cross(b-a,d-a)
        norm = norm/N.sqrt(N.dot(norm,norm))
        self.texcoords.extend((x,z,x1,z1,x1,z,x,z,x,z1,x1,z1))
        for pt in (a,c,d,a,b,c):
            self.positions.extend(pt)
            self.positions.append(1.0)
            self.normals.extend(norm)
            self.normals.append(0.0)

    def makeDataBuffers(self):
        self.positions = []
        self.normals = []
        self.texcoords = []
        step = self.width
        for x in N.arange(-self.width, self.width, step):
            for z in N.arange(-self.width, self.width, step):
                self.quad(x,z,step)
        self.n = len(self.positions)/4
        print self.n
        self.positions = DataBuffer(self.positions, 4, self.positionLocation, 0, 4)
        self.normals = DataBuffer(self.normals, 4, self.normalLocation, 0, 4)
        self.texcoords = DataBuffer(self.texcoords, 2, self.texcoordLocation, 0, 2)

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
        glDrawArrays(GL_TRIANGLES, 0, self.n)
        for buf in bufs: buf.Stop()
        glUseProgram(0)
                


        
                
        
        
