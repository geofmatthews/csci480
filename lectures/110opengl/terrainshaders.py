SCREEN_SIZE = (640,480)

import numpy as N

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import pygame
from pygame.locals import *

import time
import array

from Image import *

cameraPos = N.array((0.0, 1.0, -2.0))
lookVec = N.array((0.0, -1.0, 2.0))
polygons = 512
polygonsize = 0.02

vShaderSource = """
float interp(float a, float b, float pct) {
  float ft = pct*3.14159;
  float f = (1.0-cos(ft))*0.5;
  return a*(1.0-f) + b*(f);
}
float mynoise(float x, float y) {
  float modfactor = 512.0;
  float result = mod(x*223.234 + y*744.12 + x*y*432.12 + 254.321, modfactor);
  return result/modfactor;
}
float interpNoise(float x, float y) {
  float ix = floor(x);
  float fx = fract(x);
  float iy = floor(y);
  float fy = fract(y);
  float v1 = mynoise(ix,iy);
  float v2 = mynoise(ix+1.,iy);
  float v3 = mynoise(ix,iy+1.);
  float v4 = mynoise(ix+1.,iy+1.);
  float i1 = interp(v1,v2,fx);
  float i2 = interp(v3,v4,fx);
  return interp(i1,i2,fy);
}
float fbm(float x, float y) {
  x *= 1.0;
  y *= 1.0;
  float total = 0.0;
  float pers = 0.5;
  int numOctaves = 6;
  float freq = 1.0;
  float amp = 0.5;
  for (int i = 0; i < numOctaves; i++) {
    freq *= 2.0;
    amp *= pers;
    total += amp*interpNoise(x*freq, y*freq);
  }
  return total;
}
uniform vec3 camerapos;
varying float cameradist;
varying vec4 pos;
uniform vec3 worldpos;
varying vec3 normal;
void main() {
    pos = gl_Vertex + vec4(floor(worldpos),0.0);
    pos.y = fbm(pos.x, pos.z);
    vec3 cameravec = camerapos - pos.xyz;
    cameradist = sqrt(dot(cameravec, cameravec));
    vec3 y1 = vec3(pos.x,fbm(pos.x, pos.z+0.1),pos.z+0.1);
    vec3 y2 = vec3(pos.x+0.1,fbm(pos.x+0.1, pos.z),pos.z);
    vec3 n = cross(y1-pos.xyz,y2-pos.xyz);
    normal = normalize(gl_NormalMatrix*n);
    gl_Position = gl_ModelViewProjectionMatrix * pos;
}
"""

fShaderSource = """
float interp(float a, float b, float pct) {
  float ft = pct*3.14159;
  float f = (1.0-cos(ft))*0.5;
  return a*(1.0-f) + b*(f);
}
float mynoise(float x, float y) {
  float modfactor = 512.0;
  float foldx = mod(x*424.8383 + 934.99, modfactor);
  float foldy = mod(y*833.222 + 693.1223, modfactor);
  float foldxy = mod(x*y*342.112 + 744.43, modfactor);
  float result = mod(foldx*223.234 + foldy*744.12 + foldxy*432.12, modfactor);
  return result/modfactor;
}
float interpNoise(float x, float y) {
  float ix = floor(x);
  float fx = fract(x);
  float iy = floor(y);
  float fy = fract(y);
  float v1 = mynoise(ix,iy);
  float v2 = mynoise(ix+1.,iy);
  float v3 = mynoise(ix,iy+1.);
  float v4 = mynoise(ix+1.,iy+1.);
  float i1 = interp(v1,v2,fx);
  float i2 = interp(v3,v4,fx);
  return interp(i1,i2,fy);
}
float fbm(float x, float y) {
  x *= 0.5;
  y *= 0.5;
  float total = 0.0;
  float pers = 0.5;
  int numOctaves = 6;
  float freq = 1.0;
  float amp = 0.5;
  for (int i = 0; i < numOctaves; i++) {
    freq *= 2.0;
    amp *= pers;
    total += amp*interpNoise(x*freq, y*freq);
  }
  return total*1.5;
}
varying vec4 pos;
varying vec3 normal;
varying float cameradist;
vec3 lightdirection = normalize(vec3(2.0,1.0,2.0));
vec4 fogcolor = vec4(0.8, 0.8, 0.8, 1.0);
vec4 mycolor;
uniform float waterheight;
uniform float fognear;
void main() {
    if (pos.y < waterheight) { discard; }
    vec3 n = normalize(normal);
    float x = pos.x*2.0;
    float z = pos.z*2.0;
    float n1 = fbm(x,z);
    float n2 = fbm(x+123.0, z+321.0)*0.25;    
    float i = max(0.0, dot(n, lightdirection));
    mycolor = vec4(i*n2*2.0,i*n1,i*n2,1.0);
    float lowsnow = 0.35;
    float highsnow = 0.4;
    if (pos.y > lowsnow) {
      mycolor = mix(mycolor, vec4(1,1,1,1),
                    (pos.y-lowsnow)/(highsnow-lowsnow));
    }
    float fogfar = fognear + 3.0;
    if (cameradist < fognear) {
      gl_FragColor = mycolor;
    } else if (cameradist > fogfar) {
      gl_FragColor = fogcolor;
    } else {
      float pct = (cameradist - fognear)/(fogfar-fognear);
      gl_FragColor = mix(mycolor, fogcolor, pct);
    }
}
"""

def checkError(status, msg):
    if not(status):
        print msg
        exit()
        
def renderBitmapString(x,y,string):
    return
    font = GLUT_BITMAP_9_BY_15
    glWindowPos2f(x, y);
    for c in string:
        glutBitmapCharacter(font, ord(c))
    

def randomTexture():
    w,h = 128,128
    tmpList = [N.random.randint(0,255) for i in range(3*w*h)]
    tmpArray = array.array('B', tmpList)
    img = tmpArray.tostring()
    texture = glGenTextures(1)
    
    glActiveTexture(GL_TEXTURE0)
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT )
    glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT )
    glTexImage2D(GL_TEXTURE_2D, 0, 3, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, img)
    glBindTexture(GL_TEXTURE_2D, texture)
    return texture
    
def resize(width, height):   
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(55.0, float(width)/height, .1, 1000.)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init():
    global cameraPos, lookVec
    glColor3f(0,1,0)
    glEnable(GL_TEXTURE_2D)
    
    glEnable(GL_DEPTH_TEST)
    
    glShadeModel(GL_SMOOTH)
    glClearColor(0.8,0.8,0.8,1.0)
    
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)        
    glLight(GL_LIGHT0, GL_POSITION,  (1, 1, 1, 0))

    vSource = vShaderSource
    fSource = fShaderSource

    vShader = glCreateShader(GL_VERTEX_SHADER)
    fShader = glCreateShader(GL_FRAGMENT_SHADER)
    program = glCreateProgram()
    glAttachShader(program, vShader)
    glAttachShader(program, fShader)
    glShaderSource(vShader,  vSource)
    glShaderSource(fShader,  fSource)
    glCompileShader(vShader)
    glCompileShader(fShader)

    status = glGetShaderiv( vShader, GL_COMPILE_STATUS)
    checkError(status, "Failed to compile vertex shader.")
    status = glGetShaderiv(fShader, GL_COMPILE_STATUS)
    checkError(status, "Failed to compile fragment shader.")
    
    texture = randomTexture()
    glLinkProgram(program)
    glUseProgram(program)

    locationParam = glGetUniformLocation(program, "worldpos")
    cameraParam = glGetUniformLocation(program, "camerapos")
    waterParam = glGetUniformLocation(program, "waterheight")
    fogParam = glGetUniformLocation(program, "fognear")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(55.0, 1.5, 0.1, 100.0)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    eyex,eyey,eyez = cameraPos
    atx,aty,atz = cameraPos + lookVec
    gluLookAt(eyex,eyey,eyez,   atx,aty,atz,    0,1,0)
    glUniform3f(cameraParam, eyex,eyey,eyez)
    glUniform3f(locationParam, atx, aty, atz)
    return (locationParam, cameraParam, waterParam, fogParam)

class Landscape(object):
        
    def __init__(self, polygons, polygonsize):
        self.generateList = True
        self.callList = glGenLists(1)
        self.polygonsize = polygonsize
        self.polygons = polygons
        self.width = polygonsize * polygons
        self.height = self.width
        self.vertices = {}
        self.normals = {}
        self.texcoords = {}

    def GenerateVertices(self, x,y):
        startx = x - self.width*0.5
        starty = y - self.height*0.5
        for row in range(self.polygons+2):
            for col in range(self.polygons+2):
                x = startx + row*self.polygonsize
                y = starty + col*self.polygonsize
                z = 0.0
                self.vertices[(row,col)] = N.array((x,z,y))

    def Point(self, row,col):
        glVertex3fv(self.vertices[(row,col)])

    def Render(self):
        global cameraPos
        if self.generateList:
            self.generateList = False
            glNewList(self.callList, GL_COMPILE)
            glBegin(GL_QUADS)
            for row in range(self.polygons):
                for col in range(self.polygons):
                    self.Point(row,col)
                    self.Point(row+1,col)
                    self.Point(row+1,col+1)
                    self.Point(row,col+1)
            glEnd()
            glEndList()
        else:
            glCallList(self.callList)
            
def main():
    global lookVec, cameraPos, polygons, polygonsize
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, OPENGL|DOUBLEBUF)    
    resize(*SCREEN_SIZE)
    locationParam, cameraParam, waterParam, fogParam = init()
    waterHeight = 0.2
    fogNear = 3.0
    
    clock = pygame.time.Clock()
    
    landscape = Landscape(polygons, polygonsize)
    atx, aty, atz = lookVec + cameraPos
    landscape.GenerateVertices(0,0)

    theta = 0.025
    sintheta = N.sin(theta)
    costheta = N.cos(theta)
    leftRotate = N.array([[costheta, 0, -sintheta],
                          [0,        1,     0],
                          [sintheta, 0, costheta]])
    rightRotate = N.array([[costheta, 0, sintheta],
                          [0,        1,     0],
                          [-sintheta, 0,costheta]])

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            if event.type == KEYUP and event.key == K_ESCAPE:
                pygame.quit()
                return
            
        # Clear the screen, and z-buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
                        
        time_passed = clock.tick(30)
        time_passed_seconds = time_passed / 1000.
        
        pressed = pygame.key.get_pressed()

        delta = 0.025
        changed = False
        # Modify direction vectors for key presses
        if pressed[K_UP]:
            cameraPos[2] += lookVec[2]*delta
            cameraPos[0] += lookVec[0]*delta
            changed = True
        elif pressed[K_DOWN]:
            cameraPos[2] -= lookVec[2]*delta
            cameraPos[0] -= lookVec[0]*delta
            changed = True
            
        if pressed[K_LEFT]:
            lookVec = N.dot(lookVec, leftRotate )
            changed = True
        elif pressed[K_RIGHT]:
            lookVec = N.dot(lookVec, rightRotate )
            changed = True

        if pressed[K_u]:
            cameraPos[1] += delta*0.5
            lookVec[1] -= delta*0.5
        elif pressed[K_d]:
            cameraPos[1] -= delta*0.5
            lookVec[1] += delta*0.5

        if pressed[K_w]:
            waterHeight += 0.001
        if pressed[K_s]:
            waterHeight -= 0.001

        if pressed[K_f]:
            fogNear += 0.1
        if pressed[K_v]:
            fogNear -= 0.1

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        eyex,eyey,eyez = cameraPos
        atx,aty,atz = cameraPos + lookVec
        gluLookAt(eyex,eyey,eyez,   atx,aty,atz,    0,1,0)
        glUniform3f(locationParam, atx, aty, atz)
        glUniform3f(cameraParam, eyex,eyey,eyez)
        glUniform1f(waterParam, waterHeight)
        glUniform1f(fogParam, fogNear)

        landscape.Render()
        renderBitmapString(5,5, repr((atx, atz)))
        # Show the screen
        pygame.display.flip()
        

if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.quit()


