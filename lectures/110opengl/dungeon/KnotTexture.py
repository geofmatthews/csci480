
import os

from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import pygame
from pygame.locals import *

import numpy as N
from ctypes import c_void_p

def loadFile(filename):
    with open(os.path.join(os.getcwd(), filename)) as fp:
        return fp.read()

vertexShader = """
#version 330
uniform vec2 knotCrawl;
in vec4 position;
out vec4 fragmentPosition;
in vec4 normal;
out vec4 fragmentNormal;
in vec4 upVectorAttrib;
out vec4 fragmentUpVector;
in vec2 texcoord;
out vec2 fragmentTexcoord;
in vec2 knotcoord;
out vec2 fragmentKnotcoord;
uniform mat4 mvMatrix;
uniform mat4 pMatrix;
out vec4 eye;

void main()
{
    fragmentNormal = mvMatrix * normal;
    fragmentUpVector = mvMatrix * upVectorAttrib;
    fragmentTexcoord = texcoord;
    fragmentKnotcoord = knotcoord + knotCrawl;
    fragmentPosition = mvMatrix * position;
    eye = -vec4(fragmentPosition.xyz, 0.0);
    gl_Position = pMatrix * fragmentPosition;   
}
"""
fragmentShader = """
#version 330
uniform sampler2D firstTexture;
uniform sampler2D secondTexture;
uniform sampler2D randomArray;
uniform mat4 mvMatrix;
in vec4 fragmentNormal;
in vec4 fragmentUpVector;
in vec4 fragmentPosition;
in vec2 fragmentTexcoord;
in vec2 fragmentKnotcoord;
in vec4 eye;
uniform vec4 light;
out vec4 outputColor;
uniform int whichTexture;
vec4 upVector;


int LFSR_Rand_Gen(in int n)
{
  n = (n << 13) ^ n;
  return (n * (n*n*15731+789221) + 1376312589) & 0x7fffffff;
}

void hash(int x, int y, out float h1, out float h2)
{
  int result1 = LFSR_Rand_Gen(x);
  result1 = LFSR_Rand_Gen(result1+y);
  int result2 = LFSR_Rand_Gen(result1);
  h1 = float(result1 % 1024)/1024.0;
  h2 = float(result2 % 1024)/1024.0;
  }

vec4 normFromCircle(float x, float y, float radius, vec4 side, vec4 up, vec4 oldNorm) {
  vec4 newNorm = oldNorm;
  float halfroot2 = 0.70710678;
  float len = sqrt(x*x+y*y);
  float dist = len - halfroot2;
  if (abs(dist) < radius) {
    float hdist = dist/radius;
    float vdist = sqrt(1.0 - hdist*hdist);
    vec4 outVector = normalize(x*side + y*up);
    newNorm = normalize(hdist*outVector + vdist*oldNorm);
  }
  return newNorm;
}

vec4 normFromLine(float x, float y, float radius, vec4 side, vec4 up, vec4 trueNorm, vec4 defaultNorm){
      vec4 newNorm = defaultNorm;
      float cx = 0.5*(x-y+1);
      float cy = 0.5*(y-x+1);
      float dx = cx-x;
      float dy = cy-y;
      float dist = sqrt(dx*dx+dy*dy);
      if (x*x+y*y < cx*cx+cy*cy) {
        dist = -dist;
      }
      if (abs(dist) < radius) {
        vec4 outVector = normalize(side + up);
        float hdist = dist/radius;
        float vdist = sqrt(1.0 - hdist*hdist);
        newNorm = normalize(hdist*outVector + vdist*trueNorm);
      }
      return newNorm;
      }

     
vec4 newNormal(vec2 texcoord, vec4 oldNormal) {
  float lineRadius = 0.25;
  upVector = normalize(upVector);
  vec4 sideVector = vec4(normalize(cross(upVector.xyz, oldNormal.xyz)),0.0);
  int intX = int(texcoord.x);
  int intY = int(texcoord.y);
  float x = texcoord.x - intX;
  float y = texcoord.y - intY;
  x = 2.0*x - 1.0;
  y = 2.0*y - 1.0;
  bool A = (x > -y);
  bool B = (x > y);
  float left, up, right, down, dummy;
  hash(intX, intY, left, up);
  hash(intX+1, intY, right, dummy);
  hash(intX, intY+1, dummy, down);
  float threshold = 0.25;
  vec4 newNorm = oldNormal;
  if (A && B) {
    if (right < threshold) {
      newNorm = normFromCircle(x,y,lineRadius,sideVector,upVector,oldNormal);
    } else {
      newNorm = normFromLine(x,y,lineRadius,sideVector,upVector,oldNormal,newNorm);
      newNorm = normFromLine(x,-y,lineRadius,sideVector,-upVector,oldNormal,newNorm);
    }
  }
  else if (!A && B) {
    if (up < threshold) {
      newNorm = normFromCircle(x,y,lineRadius,sideVector,upVector,oldNormal);
    } else {
      newNorm = normFromLine(x,-y,lineRadius,sideVector,-upVector,oldNormal,newNorm);
      newNorm = normFromLine(-x,-y,lineRadius,-sideVector,-upVector,oldNormal,newNorm);
    }
  }
  else if (!A && !B) {
    if (left < threshold) {
      newNorm = normFromCircle(x,y,lineRadius,sideVector,upVector,oldNormal);
    } else {
      newNorm = normFromLine(-x,-y,lineRadius,-sideVector,-upVector,oldNormal,newNorm);
      newNorm = normFromLine(-x,y,lineRadius,-sideVector,upVector,oldNormal,newNorm);
    }
  }
  else if (A && !B) {
    if (down < threshold) {
      newNorm = normFromCircle(x,y,lineRadius,sideVector,upVector,oldNormal);
    } else {
      newNorm = normFromLine(-x,y,lineRadius,-sideVector,upVector,oldNormal,newNorm);
      newNorm = normFromLine(x,y,lineRadius,sideVector,upVector,oldNormal,newNorm);
    }
  }
  return newNorm;
}  
  
void main()
{
    vec4 lightVector;
    vec4 eyeVector, reflectVector;
    vec4 normalVector;
    float intensity, specular, lambert;
    
    lightVector = normalize(light - fragmentPosition);
    normalVector = normalize(fragmentNormal);
    upVector = normalize(fragmentUpVector);

    normalVector = newNormal(fragmentKnotcoord, normalVector);
    
    lambert = dot(normalVector, lightVector);
    intensity = max(0.0, lambert);    
    if (whichTexture == 0) {
        outputColor = intensity * texture2D(firstTexture, fragmentTexcoord);
    }
    else {
        outputColor = intensity * texture2D(randomArray, fragmentTexcoord);
    }
    eyeVector = normalize(eye);
    if (lambert > 0.0) {
        reflectVector = reflect(-lightVector, normalVector);
        specular = pow(max(dot(reflectVector, eyeVector), 0.0),
                       55);
        outputColor += vec4(specular,specular,specular,1.0);
    }
}
"""

def projectionMatrix(n,f,w,h):
    return N.array(((2.0*n/w, 0, 0, 0),
                    (0, 2.0*n/h, 0, 0),
                    (0, 0, -(f+n)/(f-n), -2.0*f*n/(f-n)),
                    (0, 0, -1, 0)), dtype = N.float32)

def translationMatrix(x,y,z):
    return N.array(((1, 0, 0, x),
                    (0, 1, 0, y),
                    (0, 0, 1, z),
                    (0, 0, 0, 1)), dtype = N.float32)

def rotationXMatrix(angle):
    s = N.sin(angle)
    c = N.cos(angle)
    return N.array(((1.0, 0.0, 0.0, 0.0),
                    (0.0,   c,  -s, 0.0),
                    (0.0,   s,   c, 0.0),
                    (0.0, 0.0, 0.0, 1.0)), dtype = N.float32)
def rotationYMatrix(angle):
    s = N.sin(angle)
    c = N.cos(angle)
    return N.array(((  c, 0.0,  -s, 0.0),
                    (0.0, 1.0, 0.0, 0.0),
                    (  s, 0.0,   c, 0.0),
                    (0.0, 0.0, 0.0, 1.0)), dtype = N.float32)

def initialize_program():
    """
    Instead of calling OpenGL's shader compilation functions directly
    (glShaderSource, glCompileShader, etc), we use PyOpenGL's wrapper
    functions, which are much simpler to use.
    """
    global cubeProgram
    cubeProgram = compileProgram(
        compileShader(vertexShader, GL_VERTEX_SHADER),
        compileShader(fragmentShader, GL_FRAGMENT_SHADER)
    )

class DataBuffer():
    def __init__(self, data, components, location, offset=0, stride=4):
        bytesPerFloat = 4
        self.data = N.array(data, dtype=N.float32)
        self.components = components
        self.offset = c_void_p(offset*bytesPerFloat)
        self.stride = stride*bytesPerFloat
        self.location = location
        
        # Find a buffer object:
        self.bufferObject = glGenBuffers(1)
        # Bind to that buffer object:
        glBindBuffer(GL_ARRAY_BUFFER, self.bufferObject)
        # Copy data into that buffer object:
        glBufferData(GL_ARRAY_BUFFER, self.data, GL_STATIC_DRAW)
        # Bind to null buffer object:
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def Start(self):
        # Bind to vertex shader attribute location:
        glEnableVertexAttribArray(self.location)
        # Bind to buffer object:
        glBindBuffer(GL_ARRAY_BUFFER, self.bufferObject)
        # Specify how to map data to vertex shader attribute:
        glVertexAttribPointer(self.location, self.components,
                              GL_FLOAT, False, self.stride, self.offset)

    def Stop(self):
        # Unbind to shader variable location:
        glDisableVertexAttribArray(self.location)

def lerp(x, a, b):
    return (1-x)*a + x*b
        
def initializeDataBuffers():
    global cubeProgram
    #front of cube:
    a = [-1,-1, 1, 1]
    b = [ 1,-1, 1, 1]
    c = [ 1, 1, 1, 1]
    d = [-1, 1, 1, 1]
    #back of cube:
    e = [-1,-1,-1, 1]
    f = [ 1,-1,-1, 1]
    g = [ 1, 1,-1, 1]
    h = [-1, 1,-1, 1]
    positions =  a+b+c + c+d+a # front
    positions += d+c+g + g+h+d # top
    positions += h+g+f + f+e+h # back
    positions += e+f+b + b+a+e # bottom
    positions += e+a+d + d+h+e # left
    positions += b+f+g + g+c+b # right
    
    top = [0,1,0,0]
    right = [1,0,0,0]
    back = [0,0,-1,0]
    left = [-1,0,0,0]
    front = [0,0,1,0]
    bottom = [0,-1,0,0]
    normals  = 6*front + 6*top + 6*back + 6*bottom + 6*left + 6*right
    upvectors = 6*top + 6*back + 6*bottom + 6*front + 6*top + 6*top
    
    texs = 6*[0,0,  1,0,  1,1,     1,1,  0,1,  0,0]
    texcoords = [1*i for i in texs]
    knotcoords = [10*i for i in texs]
    
    posLocation = glGetAttribLocation(cubeProgram, "position")
    posBuffer = DataBuffer(positions, 4, posLocation, 0, 4)
    normLocation = glGetAttribLocation(cubeProgram, "normal")
    normBuffer = DataBuffer(normals, 4, normLocation, 0, 4)
    upLocation = glGetAttribLocation(cubeProgram, "upVectorAttrib")
    upBuffer = DataBuffer(upvectors, 4, upLocation, 0, 4)
    texcoordLocation = glGetAttribLocation(cubeProgram, "texcoord")
    texcoordBuffer = DataBuffer(texcoords, 2, texcoordLocation, 0, 2)
    knotcoordLocation = glGetAttribLocation(cubeProgram, "knotcoord")
    knotcoordBuffer = DataBuffer(knotcoords, 2, knotcoordLocation, 0, 2)
    
    return [posBuffer, normBuffer, upBuffer, texcoordBuffer, knotcoordBuffer]

class TextureBuffer():
    def __init__(self, filename, location, program, unit):
        if filename == 'randomArray':
            # Make a random array of bytes:
            size = 256
            arr = range(size*size)
            for i in range(size*size):
                arr[i] = N.random.randint(0,255)
            width,height = size,size
            textureData = N.array(arr, dtype=N.ubyte)
            # that didn't work--why?
            # this does:
            textureSurface = pygame.Surface((size,size))
            for i in range(size):
                for j in range(size):
                    r = N.random.randint(0,255)
                    g = N.random.randint(0,255)
                    b = N.random.randint(0,255)
                    a = N.random.randint(0,255)
                    pygame.draw.rect(textureSurface,(r,g,b,a),pygame.Rect(i,j,1,1),1)
            width,height= size,size
            textureData = pygame.image.tostring(textureSurface,"RGBA", 1)
        else:    
            # Load the file
            textureSurface = pygame.image.load(filename)
            width,height = textureSurface.get_size()
            # Convert to bytes
            textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
        # Find a handle for a texture
        texture = glGenTextures(1)
        # Bind to it
        glBindTexture(GL_TEXTURE_2D, texture)
        # Set some texture parameters
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
        # Upload the data to the graphics card
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA,
                     GL_UNSIGNED_BYTE, textureData)
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)

        # Match a location to a texture unit
        glUseProgram(program)
        glUniform1i(location, unit)
        glUseProgram(0)

        # Save for later (don't need to save image on CPU side anymore)
        self.texture = texture
        self.unit = unit

    def Start(self):
        # Activate texture unit and bind texture
        glActiveTexture(GL_TEXTURE0 + self.unit)
        glBindTexture(GL_TEXTURE_2D, self.texture)

    def Stop(self):
        glBindTexture(GL_TEXTURE_2D, 0)
 
def initializeTextureBuffers():
    global Locations, cubeProgram
    #texture = TextureBuffer('marblelabel.jpg', Locations['firstTexture'], cubeProgram, 0)
    #texture2 = TextureBuffer('crate.tga', Locations['secondTexture'], cubeProgram, 1)
    randomArray = TextureBuffer('randomArray', Locations['randomArray'], cubeProgram, 2)
    #return [texture, texture2, randomArray]
    return[randomArray]

def display():
    global cubeBuffers, textureBuffers ,time,  light, Locations, whichTex, rotX,rotY,knotCrawl
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    pMatrix = projectionMatrix(1.0, 100.0, 1.0, 0.75)
    
    trans = translationMatrix(0.0, -0.25, -5.0)
    rot = rotationXMatrix(rotX)
    rot = N.dot(rot, rotationYMatrix(rotY))
    
    mvMatrix =  N.dot(trans, rot)

    light = N.array((2*N.cos(time), 2*N.cos(time), 2*N.sin(time), 1), dtype=N.float32)
    light = N.dot(trans, light)
    
    glUseProgram(cubeProgram)
    glUniform1f(Locations['time'], time)
    glUniform4fv(Locations['light'], 1, light)
    glUniform1i(Locations['whichTexture'], whichTex)
    glUniform2fv(Locations['knotCrawl'],1,knotCrawl)
    
    # Remember to transpose:
    glUniformMatrix4fv(Locations['mvMatrix'], 1, True, mvMatrix)
    glUniformMatrix4fv(Locations['pMatrix'], 1, True, pMatrix)

    # activate buffers:
    for buf in cubeBuffers: buf.Start()
    for tex in textureBuffers: tex.Start()

    n = len(cubeBuffers[0].data)/cubeBuffers[0].components
    glDrawArrays(GL_TRIANGLES, 0, n)
    for buf in cubeBuffers: buf.Stop()
    for tex in textureBuffers: tex.Stop()
    
    glBindTexture(GL_TEXTURE_2D, 0)      
    glUseProgram(0)
    
def initializeVertexArray():
    # Must have a vertex array object to use vertex buffer objects.
    # Just one will do:
    global vao_array
    vao_array = N.zeros(1, dtype=N.uint)
    vao_array = glGenVertexArrays(1)
    glBindVertexArray(vao_array)


# Must be called after we have an OpenGL context, i.e. after the pygame
# window is created
def init():
    global cubeProgram, cubeBuffers,textureBuffers, Locations
    initialize_program()
    cubeBuffers = initializeDataBuffers()
    initializeVertexArray()
    Locations = {}
    for name in ('time','light','mvMatrix','pMatrix',
                 'firstTexture','secondTexture','whichTexture',
                 'randomArray', 'knotCrawl', 'upVectorAttrib'):
        Locations[name] = glGetUniformLocation(cubeProgram, name)

    textureBuffers = initializeTextureBuffers()
    
    glClearColor(0.1, 0.2, 0.3, 0.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)

       
def main():
    global window, time, light, inc, whichTex, rotX, rotY, knotCrawl
    pygame.init()
    screen = pygame.display.set_mode((800,600), OPENGL|DOUBLEBUF)
    clock = pygame.time.Clock()
    time = 0.0
    light = N.array((10,10,10,0), dtype = N.float32)
    timeInc = 0.01
    time = 0.0
    whichTex = 0
    init()
    rotX = rotY = 0.0
    knotCrawl = N.array((0.0, 0.0), dtype = N.float32)
    while True:     
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYUP and event.key == K_ESCAPE:
                return
            if event.type == KEYDOWN:
                if event.key == K_t:
                    if whichTex == 0:
                        whichTex = 1
                    else:
                        whichTex = 0
        pressed = pygame.key.get_pressed()
        if pressed[K_k]:
            knotCrawl[0] += 0.01
            knotCrawl[1] += 0.05
        if pressed[K_d]:
            time += 0.05
        if pressed[K_s]:
            time -= 0.05
        if pressed[K_UP]:
            rotX += 0.05
        if pressed[K_DOWN]:
            rotX -= 0.05
        if pressed[K_LEFT]:
            rotY += 0.05
        if pressed[K_RIGHT]:
            rotY -= 0.05
            
        clock.tick(30)
        #time += timeInc
        display()
        pygame.display.flip()

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
