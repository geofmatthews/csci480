# Classes to make constructing and drawing many objects simpler

# We will assume that all vertex arrays have 18 components of 32 bit floats
# whether or not they are all used:
# 4 floats position
# 4 floats normal
# 4 floats tangent (positive s texture coordinate direction "right")
# 4 floats bitangent (positive t texture coordinate direction "up")
# 2 floats texture coordinates

# Also assuming we're using 16 bit unsigned ints for elements

sizeOfFloat = 4
sizeOfShort = 2
vertexSize = 18*sizeOfFloat

from OpenGL.GL import *
from ctypes import c_void_p
from frames import Frame

def getBuffer(arr, type):
    buff = glGenBuffers(1)
    glBindBuffer(type, buff)
    glBufferData(type, arr, GL_STATIC_DRAW)
    glBindBuffer(type, 0)
    return buff

def vertexPointer(attrib, size, components, offset):
    if attrib >= 0:
        sizeOfFloat = 4
        glEnableVertexAttribArray(attrib)
        glVertexAttribPointer(attrib,
                              components,
                              GL_FLOAT,
                              GL_FALSE,
                              size,
                              c_void_p(offset*sizeOfFloat))
    
def bindTextureUnit(unit, texture, samplerUnif):
    glActiveTexture(GL_TEXTURE0 + unit)
    glBindTexture(GL_TEXTURE_2D, texture)
    glUniform1i(samplerUnif, unit)

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
        self.arrayBuffer = getBuffer(vertices, GL_ARRAY_BUFFER)
        self.elementBuffer = getBuffer(elements, GL_ELEMENT_ARRAY_BUFFER)
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
        vertexPointer(self.positionAttrib, vertexSize, 4, 0)
        vertexPointer(self.normalAttrib, vertexSize, 4, 4)
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
        self.arrayBuffer = getBuffer(vertices, GL_ARRAY_BUFFER)
        self.elementBuffer = getBuffer(elements, GL_ELEMENT_ARRAY_BUFFER)
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
        vertexPointer(self.positionAttrib, vertexSize, 4, 0)
        vertexPointer(self.normalAttrib, vertexSize, 4, 4)
        vertexPointer(self.tangentAttrib,vertexSize, 4, 8)
        vertexPointer(self.bitangentAttrib,vertexSize, 4, 12)
        vertexPointer(self.uvAttrib,vertexSize, 2, 16)
        # bind our color texture unit
        bindTextureUnit(0, self.colorTexture, self.colorSamplerUnif)
        # draw
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
        self.arrayBuffer = getBuffer(vertices, GL_ARRAY_BUFFER)
        self.elementBuffer = getBuffer(elements, GL_ELEMENT_ARRAY_BUFFER)
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
        # attribs
        glBindBuffer(GL_ARRAY_BUFFER, self.arrayBuffer)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.elementBuffer)
        vertexPointer(self.positionAttrib, vertexSize, 4, 0)
        vertexPointer(self.normalAttrib, vertexSize, 4, 4)
        vertexPointer(self.tangentAttrib, vertexSize, 4, 8)
        vertexPointer(self.uvAttrib, vertexSize, 2, 16)
        # bind our texture units
        bindTextureUnit(0, self.colorTexture, self.colorSamplerUnif)
        bindTextureUnit(1, self.normalTexture, self.normalSamplerUnif)
        # draw
        glDrawElements(GL_TRIANGLES, self.elementSize,
                       GL_UNSIGNED_SHORT, c_void_p(0))
        glUseProgram(0)

class flatTexturedMesh(Frame):
    """Use flattextured.vert and flattextured.frag"""
    def __init__(self, texture, vertexArray, shader, scaleuv):
        Frame.__init__(self)
        self.texture = texture
        self.shader = shader
        self.scaleuv = scaleuv
        # send data to opengl context:
        vertices = vertexArray[0]
        elements = vertexArray[1]
        self.elementSize = len(elements)*sizeOfShort
        self.arrayBuffer = getBuffer(vertices, GL_ARRAY_BUFFER)
        self.elementBuffer = getBuffer(elements, GL_ELEMENT_ARRAY_BUFFER)
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
        vertexPointer(self.positionAttrib, vertexSize, 4, 0)
        vertexPointer(self.uvAttrib, vertexSize, 2, 16)
        # bind our color texture unit
        bindTextureUnit(0, self.texture, self.colorSamplerUnif)
        # draw
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
        self.arrayBuffer = getBuffer(vertices, GL_ARRAY_BUFFER)
        self.elementBuffer = getBuffer(elements, GL_ELEMENT_ARRAY_BUFFER)
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
        # attribs
        glBindBuffer(GL_ARRAY_BUFFER, self.arrayBuffer)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.elementBuffer)
        vertexPointer(self.positionAttrib, vertexSize, 4, 0)
        vertexPointer(self.normalAttrib, vertexSize, 4, 4)
        vertexPointer(self.tangentAttrib, vertexSize, 4, 8)
        vertexPointer(self.bitangentAttrib, vertexSize, 4, 12)
        vertexPointer(self.uvAttrib, vertexSize, 2, 16)
        
        glDrawElements(GL_TRIANGLES, self.elementSize,
                       GL_UNSIGNED_SHORT, c_void_p(0))
        glUseProgram(0)
        

class reflectorMesh(Frame):
    """Use reflector.vert and reflector.frag"""
    def __init__(self,
                 posxTexture,
                 negxTexture,
                 posyTexture,
                 negyTexture,
                 poszTexture,
                 negzTexture,
                 vertexArray,
                 shader):
        Frame.__init__(self)
        self.posxTexture = posxTexture
        self.negxTexture = negxTexture
        self.posyTexture = posyTexture
        self.negyTexture = negyTexture
        self.poszTexture = poszTexture
        self.negzTexture = negzTexture
        self.shader = shader
        # send data to opengl context:
        vertices = vertexArray[0]
        elements = vertexArray[1]
        self.elementSize = len(elements)*sizeOfShort
        self.arrayBuffer = getBuffer(vertices, GL_ARRAY_BUFFER)
        self.elementBuffer = getBuffer(elements, GL_ELEMENT_ARRAY_BUFFER)
        # find attribute locations:
        self.positionAttrib = glGetAttribLocation(shader, "position")
        self.normalAttrib = glGetAttribLocation(shader, "normal")
        self.tangentAttrib = glGetAttribLocation(shader, "tangent")
        self.bitangentAttrib = glGetAttribLocation(shader, "bitangent")

        # find the uniform locations:
        self.posxUnif = glGetUniformLocation(shader, "posxsampler")
        self.negxUnif = glGetUniformLocation(shader, "negxsampler")
        self.posyUnif = glGetUniformLocation(shader, "posysampler")
        self.negyUnif = glGetUniformLocation(shader, "negysampler")
        self.poszUnif = glGetUniformLocation(shader, "poszsampler")
        self.negzUnif = glGetUniformLocation(shader, "negzsampler")

        self.modelUnif = glGetUniformLocation(shader, "model")
        self.viewUnif = glGetUniformLocation(shader, "view")
        self.projectionUnif = glGetUniformLocation(shader, "projection")
        self.lightUnif = glGetUniformLocation(shader, "light")
        self.colorUnif = glGetUniformLocation(shader, "color")

    def display(self, view, projection, light):
        glUseProgram(self.shader)
        # uniforms
        glUniformMatrix4fv(self.viewUnif, 1, GL_TRUE, view)
        glUniformMatrix4fv(self.projectionUnif, 1, GL_TRUE, projection)
        glUniform4fv(self.lightUnif, 1, light)
        glUniformMatrix4fv(self.modelUnif, 1, GL_TRUE, self.model())
        # attribs
        glBindBuffer(GL_ARRAY_BUFFER, self.arrayBuffer)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.elementBuffer)
        vertexPointer(self.positionAttrib, vertexSize, 4, 0)
        vertexPointer(self.normalAttrib, vertexSize, 4, 4)
        vertexPointer(self.tangentAttrib, vertexSize, 4, 8)
        vertexPointer(self.bitangentAttrib, vertexSize, 4, 12)
        # bind all those texture units
        bindTextureUnit(0, self.posxTexture, self.posxUnif)
        bindTextureUnit(1, self.negxTexture, self.negxUnif)
        bindTextureUnit(2, self.posyTexture, self.posyUnif)
        bindTextureUnit(3, self.negyTexture, self.negyUnif)
        bindTextureUnit(4, self.poszTexture, self.poszUnif)
        bindTextureUnit(5, self.negzTexture, self.negzUnif)
        
        glDrawElements(GL_TRIANGLES, self.elementSize,
                       GL_UNSIGNED_SHORT, c_void_p(0))
        glUseProgram(0)
        
