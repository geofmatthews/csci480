# Classes to make constructing and drawing many objects simpler

# We will assume that all vertex arrays have 18 components,
# whether or not they are all used:
# 4 floats position
# 4 floats normal
# 4 floats tangent (positive s texture coordinate direction "right")
# 4 floats bitangent (positive t texture coordinate direction "up")
# 2 floats texture coordinates

sizeOfFloat = 4
sizeOfShort = 2
vertexSize = 18*sizeOfFloat

from OpenGL.GL import *
from ctypes import c_void_p
from frames import Frame

class coloredMesh(Frame):
    """Use phong.vert and phong.frag"""
    def __init__(self, color, vertexArray, shader):
        Frame.__init__(self)
        self.color = color
        self.shader = shader
        # send data to opengl context:
        vertices = vertexArray[0]
        elements = vertexArray[1]
        self.elementSize = len(elements)*sizeOfShort
        self.arrayBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.arrayBuffer)
        glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        self.elementBuffer = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.elementBuffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, elements, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        # find attribute locations:
        self.positionAttrib = glGetAttribLocation(shader, "position")
        self.normalAttrib = glGetAttribLocation(shader, "normal")
        self.uvAttrib = glGetAttribLocation(shader, "uv")
        # find the uniform locations:
        self.colorUnif = glGetUniformLocation(shader, "color")
        self.modelUnif = glGetUniformLocation(shader, "model")
        self.viewUnif = glGetUniformLocation(shader, "view")
        self.projectionUnif = glGetUniformLocation(shader, "projection")
        self.lightUnif = glGetUniformLocation(shader, "light")

    def display(self, view, projection, light):
        glUseProgram(self.shader)
        glUniformMatrix4fv(self.viewUnif, 1, GL_TRUE, view)
        glUniformMatrix4fv(self.projectionUnif, 1, GL_TRUE, projection)
        glUniform4fv(self.lightUnif, 1, light)
        glUniform4fv(self.colorUnif, 1, self.color)
        glUniformMatrix4fv(self.modelUnif, 1, GL_TRUE, self.model())
        glBindBuffer(GL_ARRAY_BUFFER, self.arrayBuffer)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.elementBuffer)
        glEnableVertexAttribArray(self.positionAttrib)
        glVertexAttribPointer(self.positionAttrib,
                              4,
                              GL_FLOAT,
                              GL_FALSE,
                              vertexSize,
                              c_void_p(0))
        glEnableVertexAttribArray(self.normalAttrib)
        glVertexAttribPointer(self.normalAttrib,
                              4,
                              GL_FLOAT,
                              GL_FALSE,
                              vertexSize,
                              c_void_p(4*sizeOfFloat))
        glDrawElements(GL_TRIANGLES, self.elementSize,
                       GL_UNSIGNED_SHORT, c_void_p(0))
        glUseProgram(0)

class coloredTextureMesh(Frame):
    """Use textured.vert and textured.frag"""
    def __init__(self, colortexture, vertexArray, shader):
        Frame.__init__(self)
        self.useNormals = 1
        self.colorTexture = colortexture
        self.shader = shader
        # send data to opengl context:
        vertices = vertexArray[0]
        elements = vertexArray[1]
        self.elementSize = len(elements)*sizeOfShort
        self.arrayBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.arrayBuffer)
        glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        self.elementBuffer = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.elementBuffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, elements, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        # find attribute locations:
        self.positionAttrib = glGetAttribLocation(shader, "position")
        self.normalAttrib = glGetAttribLocation(shader, "normal")
        self.tangentAttrib = glGetAttribLocation(shader, "tangent")
        self.bitangentAttrib = glGetAttribLocation(shader, "bitangent")
        self.uvAttrib = glGetAttribLocation(shader, "uv")
        # find the uniform locations:
        self.colorSamplerUnif = glGetUniformLocation(shader, "colorsampler")
        self.normalSamplerUnif = glGetUniformLocation(shader, "normalsampler")
        self.modelUnif = glGetUniformLocation(shader, "model")
        self.viewUnif = glGetUniformLocation(shader, "view")
        self.projectionUnif = glGetUniformLocation(shader, "projection")
        self.lightUnif = glGetUniformLocation(shader, "light")
        self.useNormalsUnif = glGetUniformLocation(shader, "usenormals")

    def display(self, view, projection, light):
        glUseProgram(self.shader)
        # uniforms
        glUniformMatrix4fv(self.viewUnif, 1, GL_TRUE, view)
        glUniformMatrix4fv(self.projectionUnif, 1, GL_TRUE, projection)
        glUniform4fv(self.lightUnif, 1, light)
        glUniformMatrix4fv(self.modelUnif, 1, GL_TRUE, self.model())
        glUniform1i(self.useNormalsUnif, self.useNormals)
        glBindBuffer(GL_ARRAY_BUFFER, self.arrayBuffer)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.elementBuffer)
        glEnableVertexAttribArray(self.positionAttrib)
        glVertexAttribPointer(self.positionAttrib,
                              4,
                              GL_FLOAT,
                              GL_FALSE,
                              vertexSize,
                              c_void_p(0))
        glEnableVertexAttribArray(self.normalAttrib)
        glVertexAttribPointer(self.normalAttrib,
                              4,
                              GL_FLOAT,
                              GL_FALSE,
                              vertexSize,
                              c_void_p(4*sizeOfFloat))
        if self.tangentAttrib >= 0:
            glEnableVertexAttribArray(self.tangentAttrib)
            glVertexAttribPointer(self.tangentAttrib,
                                  4,
                                  GL_FLOAT,
                                  GL_FALSE,
                                  vertexSize,
                                  c_void_p(8*sizeOfFloat))
        if self.bitangentAttrib >= 0:
            glEnableVertexAttribArray(self.bitangentAttrib)
            glVertexAttribPointer(self.bitangentAttrib,
                                  4,
                                  GL_FLOAT,
                                  GL_FALSE,
                                  vertexSize,
                                  c_void_p(12*sizeOfFloat))
        if self.uvAttrib >= 0:
            glEnableVertexAttribArray(self.uvAttrib)
            glVertexAttribPointer(self.uvAttrib,
                                  2,
                                  GL_FLOAT,
                                  GL_FALSE,
                                  vertexSize,
                                  c_void_p(16*sizeOfFloat))
        # bind our color texture units
        colorUnit = 0
        glActiveTexture(GL_TEXTURE0 + colorUnit)
        glBindTexture(GL_TEXTURE_2D, self.colorTexture)
        glUniform1i(self.colorSamplerUnif, colorUnit)
        
        glDrawElements(GL_TRIANGLES, self.elementSize,
                       GL_UNSIGNED_SHORT, c_void_p(0))
        glUseProgram(0)

class texturedMesh(Frame):
    """Use textured.vert and textured.frag"""
    def __init__(self, colortexture, normaltexture, vertexArray, shader):
        Frame.__init__(self)
        self.useNormals = 1
        self.colorTexture = colortexture
        self.normalTexture = normaltexture
        self.shader = shader
        # send data to opengl context:
        vertices = vertexArray[0]
        elements = vertexArray[1]
        self.elementSize = len(elements)*sizeOfShort
        self.arrayBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.arrayBuffer)
        glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        self.elementBuffer = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.elementBuffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, elements, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        # find attribute locations:
        self.positionAttrib = glGetAttribLocation(shader, "position")
        self.normalAttrib = glGetAttribLocation(shader, "normal")
        self.tangentAttrib = glGetAttribLocation(shader, "tangent")
        self.bitangentAttrib = glGetAttribLocation(shader, "bitangent")
        self.uvAttrib = glGetAttribLocation(shader, "uv")
        # find the uniform locations:
        self.colorSamplerUnif = glGetUniformLocation(shader, "colorsampler")
        self.normalSamplerUnif = glGetUniformLocation(shader, "normalsampler")
        self.modelUnif = glGetUniformLocation(shader, "model")
        self.viewUnif = glGetUniformLocation(shader, "view")
        self.projectionUnif = glGetUniformLocation(shader, "projection")
        self.lightUnif = glGetUniformLocation(shader, "light")
        self.useNormalsUnif = glGetUniformLocation(shader, "usenormals")

    def display(self, view, projection, light):
        glUseProgram(self.shader)
        # uniforms
        glUniformMatrix4fv(self.viewUnif, 1, GL_TRUE, view)
        glUniformMatrix4fv(self.projectionUnif, 1, GL_TRUE, projection)
        glUniform4fv(self.lightUnif, 1, light)
        glUniformMatrix4fv(self.modelUnif, 1, GL_TRUE, self.model())
        glUniform1i(self.useNormalsUnif, self.useNormals)
        glBindBuffer(GL_ARRAY_BUFFER, self.arrayBuffer)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.elementBuffer)
        glEnableVertexAttribArray(self.positionAttrib)
        glVertexAttribPointer(self.positionAttrib,
                              4,
                              GL_FLOAT,
                              GL_FALSE,
                              vertexSize,
                              c_void_p(0))
        glEnableVertexAttribArray(self.normalAttrib)
        glVertexAttribPointer(self.normalAttrib,
                              4,
                              GL_FLOAT,
                              GL_FALSE,
                              vertexSize,
                              c_void_p(4*sizeOfFloat))
        glEnableVertexAttribArray(self.tangentAttrib)
        glVertexAttribPointer(self.tangentAttrib,
                              4,
                              GL_FLOAT,
                              GL_FALSE,
                              vertexSize,
                              c_void_p(8*sizeOfFloat))
        glEnableVertexAttribArray(self.bitangentAttrib)
        glVertexAttribPointer(self.bitangentAttrib,
                              4,
                              GL_FLOAT,
                              GL_FALSE,
                              vertexSize,
                              c_void_p(12*sizeOfFloat))
        glEnableVertexAttribArray(self.uvAttrib)
        glVertexAttribPointer(self.uvAttrib,
                              2,
                              GL_FLOAT,
                              GL_FALSE,
                              vertexSize,
                              c_void_p(16*sizeOfFloat))
        # bind our color texture units
        colorUnit = 0
        glActiveTexture(GL_TEXTURE0 + colorUnit)
        glBindTexture(GL_TEXTURE_2D, self.colorTexture)
        glUniform1i(self.colorSamplerUnif, colorUnit)
        
        # bind our normal texture units
        normalUnit = 1
        glActiveTexture(GL_TEXTURE0 + normalUnit)
        glBindTexture(GL_TEXTURE_2D, self.normalTexture)
        glUniform1i(self.normalSamplerUnif, normalUnit)
        
        glDrawElements(GL_TRIANGLES, self.elementSize,
                       GL_UNSIGNED_SHORT, c_void_p(0))
        glUseProgram(0)

class flatTexturedMesh(Frame):
    """Use flattextured.vert and flattextured.frag"""
    def __init__(self, colortexture, vertexArray, shader, scaleuv):
        Frame.__init__(self)
        self.colorTexture = colortexture
        self.shader = shader
        self.scaleuv = scaleuv
        # send data to opengl context:
        vertices = vertexArray[0]
        elements = vertexArray[1]
        self.elementSize = len(elements)*sizeOfShort
        self.arrayBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.arrayBuffer)
        glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        self.elementBuffer = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.elementBuffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, elements, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        # find attribute locations:
        self.positionAttrib = glGetAttribLocation(shader, "position")
        self.uvAttrib = glGetAttribLocation(shader, "uv")
        # find the uniform locations:
        self.colorSamplerUnif = glGetUniformLocation(shader, "colorsampler")
        self.scaleuvUnif = glGetUniformLocation(shader, "scaleuv")
        self.modelUnif = glGetUniformLocation(shader, "model")
        self.viewUnif = glGetUniformLocation(shader, "view")
        self.projectionUnif = glGetUniformLocation(shader, "projection")

    def display(self, view, projection, light):
        glUseProgram(self.shader)
        # uniforms
        glUniform2fv(self.scaleuvUnif, 1, self.scaleuv)
        glUniformMatrix4fv(self.viewUnif, 1, GL_TRUE, view)
        glUniformMatrix4fv(self.projectionUnif, 1, GL_TRUE, projection)
        glUniformMatrix4fv(self.modelUnif, 1, GL_TRUE, self.model())
        glBindBuffer(GL_ARRAY_BUFFER, self.arrayBuffer)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.elementBuffer)
        glEnableVertexAttribArray(self.positionAttrib)
        glVertexAttribPointer(self.positionAttrib,
                              4,
                              GL_FLOAT,
                              GL_FALSE,
                              vertexSize,
                              c_void_p(0))
        glEnableVertexAttribArray(self.uvAttrib)
        glVertexAttribPointer(self.uvAttrib,
                              2,
                              GL_FLOAT,
                              GL_FALSE,
                              vertexSize,
                              c_void_p(16*sizeOfFloat))
        # bind our color texture unit
        colorUnit = 0
        glActiveTexture(GL_TEXTURE0 + colorUnit)
        glBindTexture(GL_TEXTURE_2D, self.colorTexture)
        glUniform1i(self.colorSamplerUnif, colorUnit)
        
        glDrawElements(GL_TRIANGLES, self.elementSize,
                       GL_UNSIGNED_SHORT, c_void_p(0))
        glUseProgram(0)


class proceduralMesh(Frame):
    """Use bumpmap.vert and knot.frag, e.g."""
    def __init__(self, color, scaleCoords, vertexArray, shader):
        Frame.__init__(self)
        self.color = color
        self.scaleCoords = scaleCoords
        self.shader = shader
        # send data to opengl context:
        vertices = vertexArray[0]
        elements = vertexArray[1]
        self.elementSize = len(elements)*sizeOfShort
        self.arrayBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.arrayBuffer)
        glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        self.elementBuffer = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.elementBuffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, elements, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        # find attribute locations:
        self.positionAttrib = glGetAttribLocation(shader, "position")
        self.normalAttrib = glGetAttribLocation(shader, "normal")
        self.tangentAttrib = glGetAttribLocation(shader, "tangent")
        self.bitangentAttrib = glGetAttribLocation(shader, "bitangent")
        self.uvAttrib = glGetAttribLocation(shader, "uv")
        # find the uniform locations:
        self.modelUnif = glGetUniformLocation(shader, "model")
        self.viewUnif = glGetUniformLocation(shader, "view")
        self.projectionUnif = glGetUniformLocation(shader, "projection")
        self.lightUnif = glGetUniformLocation(shader, "light")
        self.scaleCoordsUnif = glGetUniformLocation(shader, "scalecoords")
        self.colorUnif = glGetUniformLocation(shader, "color")

    def display(self, view, projection, light):
        glUseProgram(self.shader)
        # uniforms
        glUniformMatrix4fv(self.viewUnif, 1, GL_TRUE, view)
        glUniformMatrix4fv(self.projectionUnif, 1, GL_TRUE, projection)
        glUniform4fv(self.lightUnif, 1, light)
        glUniform4fv(self.colorUnif, 1, self.color)
        glUniformMatrix4fv(self.modelUnif, 1, GL_TRUE, self.model())
        glUniform1f(self.scaleCoordsUnif, self.scaleCoords)
        glBindBuffer(GL_ARRAY_BUFFER, self.arrayBuffer)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.elementBuffer)
        glEnableVertexAttribArray(self.positionAttrib)
        glVertexAttribPointer(self.positionAttrib,
                              4,
                              GL_FLOAT,
                              GL_FALSE,
                              vertexSize,
                              c_void_p(0))
        glEnableVertexAttribArray(self.normalAttrib)
        glVertexAttribPointer(self.normalAttrib,
                              4,
                              GL_FLOAT,
                              GL_FALSE,
                              vertexSize,
                              c_void_p(4*sizeOfFloat))
        glEnableVertexAttribArray(self.tangentAttrib)
        glVertexAttribPointer(self.tangentAttrib,
                              4,
                              GL_FLOAT,
                              GL_FALSE,
                              vertexSize,
                              c_void_p(8*sizeOfFloat))
        glEnableVertexAttribArray(self.bitangentAttrib)
        glVertexAttribPointer(self.bitangentAttrib,
                              4,
                              GL_FLOAT,
                              GL_FALSE,
                              vertexSize,
                              c_void_p(12*sizeOfFloat))
        glEnableVertexAttribArray(self.uvAttrib)
        glVertexAttribPointer(self.uvAttrib,
                              2,
                              GL_FLOAT,
                              GL_FALSE,
                              vertexSize,
                              c_void_p(16*sizeOfFloat))
        
        glDrawElements(GL_TRIANGLES, self.elementSize,
                       GL_UNSIGNED_SHORT, c_void_p(0))
        glUseProgram(0)
        
