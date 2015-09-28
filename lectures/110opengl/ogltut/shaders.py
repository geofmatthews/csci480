import os,sys,exceptions
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram

def loadFile(filename):
    with open(os.path.join(os.getcwd(), filename)) as fp:
        return fp.read()

def loadProgram(vertexfile, fragmentfile):
    vert = loadFile(vertexfile)
    frag = loadFile(fragmentfile)
    try:
        vertprog = compileShader(vert, GL_VERTEX_SHADER)
    except exceptions.RuntimeError as err:
        print "VERTEX SHADER ERROR:\n", err[0]
    try:
        fragprog = compileShader(frag, GL_FRAGMENT_SHADER)
    except exceptions.RuntimeError as err:
        print "FRAGMENT SHADER ERROR:\n", err[0]
    try:
        myProgram = compileProgram(vertprog, fragprog)
    except exceptions.RuntimeError as err:
        print "SHADER LINKER ERROR:\n", err[0]
    return myProgram
        
    
