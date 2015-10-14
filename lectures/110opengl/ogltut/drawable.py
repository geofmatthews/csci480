import numpy as N
from OpenGL.GL import *
from ctypes import c_void_p
from transforms import *

class Drawable():
    def __init__(self,
                 control,
                 programID,
                 pmatrixID,
                 vmatrixID,
                 mmatrixID,
                 textureID,
                 texture,
                 vertNormUVBuffer,
                 vertNormUVIndexBuffer,
                 pID,
                 nID,
                 uvID,
                 lightID,
                 numberOfVertices):

         self.control = control
         self.programID = programID
         self.pmatrixID = pmatrixID
         self.vmatrixID = vmatrixID
         self.mmatrixID = mmatrixID
         self.textureID = textureID
         self.texture = texture
         self.vertNormUVBuffer = vertNormUVBuffer
         self.vertNormUVIndexBuffer = vertNormUVIndexBuffer
         self.pID = pID
         self.nID = nID
         self.uvID = uvID
         self.lightID = lightID
         self.numberOfVertices = numberOfVertices

    def Draw(self, mmatrix, vmatrix, pmatrix, time, lightDirection):                 
        # use our shader
        glUseProgram(self.programID)
        # send our transform to the shader
        glUniformMatrix4fv(self.pmatrixID, 1, GL_TRUE, pmatrix)
        glUniformMatrix4fv(self.mmatrixID, 1, GL_TRUE, mmatrix)
        glUniformMatrix4fv(self.vmatrixID, 1, GL_TRUE, vmatrix)
        # GL_TRUE: transpose the matrix for opengl column major order

        ld = N.dot(rotationYMatrix(time), lightDirection)
        glUniform4fv(self.lightID, 1, ld)
        
        # bind our texture to unit 0
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        # set our sampler
        glUniform1i(self.textureID, 0)

        # only one attribute buffer:
        glBindBuffer(GL_ARRAY_BUFFER, self.vertNormUVBuffer)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.vertNormUVIndexBuffer)
        # three different attribute pointers:
        bytesPerFloat = 4
        bytesPerShort = 2
        # points:
        if self.pID >= 0:
            glEnableVertexAttribArray(self.pID)
            glVertexAttribPointer(
                self.pID,             # attrib  
                4,                      # size
                GL_FLOAT,               # type
                GL_FALSE,               # normalized?
                10*bytesPerFloat,       # stride
                c_void_p(0)             # array buffer offset
                )
        # normals:
        if self.nID >= 0:
            glEnableVertexAttribArray(self.nID)
            glVertexAttribPointer(
                self.nID,
                4,
                GL_FLOAT,
                GL_FALSE,
                10*bytesPerFloat,
                c_void_p(4*bytesPerFloat))
        # uvs:
        if self.uvID >= 0:
            glEnableVertexAttribArray(self.uvID)
            glVertexAttribPointer(
                self.uvID,
                2,
                GL_FLOAT,
                GL_FALSE,
                10*bytesPerFloat,
                c_void_p(8*bytesPerFloat))
        
        # draw the triangle
        glDrawElements(GL_TRIANGLES, self.numberOfVertices*bytesPerShort,
                       GL_UNSIGNED_SHORT, c_void_p(0))

        if self.pID >= 0:
            glDisableVertexAttribArray(self.pID)
        if self.nID >= 0:
            glDisableVertexAttribArray(self.nID)
        if self.uvID >= 0:
            glDisableVertexAttribArray(self.uvID)

