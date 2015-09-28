import numpy as N
from transforms import *
from psurfacetangent import *

def simpleVertShader():
    return """
#version 330 core
in vec4 positionBuffer;
in vec4 normalBuffer;
in vec2 uvBuffer;
uniform mat4 M;
uniform mat4 V;
uniform mat4 P;
uniform vec4 lightDirection;
out vec4 normal;
out vec4 tangent;
out vec4 light;
out vec4 eye;
out vec2 uv;
void main () {
  uv = uvBuffer;
  light = V * lightDirection;
  normal = V * M * normalBuffer;
  tangent = V * M * tangentBuffer;
  eye = -(V * M * positionBuffer);
  gl_Position = P * V * M * positionBuffer;
}
"""
def simpleFragShader(color):
    colorstr = ",".join([str(x) for x in color])
    return """
#version 330 core
in vec4 normal;
in vec4 tangent;
in vec4 light;
in vec4 eye;
in vec2 uv;
out vec4 color;
void main () {
  vec4 basecolor = vec4(""" + colorstr + """);
  float ambient

class Arrow():
    def __init__(self,
                 position = vec((0,0,0,1)),
                 vector = vec((1,0,0,0)),
                 color = vec((1,0,0,1))):
        self.position = position
        self.vector = vector
        self.color = color
        mag = N.sqrt(N.dot(vector, vector))
        self.vertices,self.indices = arrow(mag)
        self.numberOfVertices = len(self.indices)
        self.norm = N.normalize(vector)
        
                 
