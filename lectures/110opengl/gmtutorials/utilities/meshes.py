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
    """Use phongshader.vert and phongshader.frag"""
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
