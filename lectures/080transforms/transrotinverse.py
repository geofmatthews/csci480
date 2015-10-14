# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 15:17:37 2014

@author: matthews
"""

import numpy,random,time

def xrotation(theta):
    c = numpy.cos(theta)
    s = numpy.sin(theta)
    m = numpy.identity(4)
    m[0,0] = c
    m[1,1] = c
    m[0,1] = -s
    m[1,0] = s
    return m
    
def yrotation(theta):
    c = numpy.cos(theta)
    s = numpy.sin(theta)
    m = numpy.identity(4)
    m[0,0] = c
    m[2,2] = c
    m[0,2] = -s
    m[2,0] = s
    return m
    
def zrotation(theta):
    c = numpy.cos(theta)
    s = numpy.sin(theta)
    m = numpy.identity(4)
    m[1,1] = c
    m[2,2] = c
    m[1,2] = -s
    m[2,1] = s
    return m
    
def randomRotation():
    m = numpy.identity(4)
    for i in range(10):
        angle = numpy.pi * random.random()
        m = numpy.dot(xrotation(angle), m)
        angle = numpy.pi * random.random()
        m = numpy.dot(yrotation(angle), m)
        angle = numpy.pi * random.random()
        m = numpy.dot(zrotation(angle), m)
    return m
    
def randomTranslation():
    m = numpy.identity(4)
    for i in range(3):
        m[i,3] = random.random()
    return m
    
def randomTransRot():
    return numpy.dot(randomTranslation(), randomRotation())
    
ident = numpy.identity(4)

def transRotInv(m):
    rot = numpy.copy(ident)
    rot[0:3,0:3] = numpy.transpose(m[0:3,0:3])
    trans = numpy.copy(ident)
    trans[0:3,3] = -m[0:3,3]
    return numpy.dot(rot, trans)    
           
rot = randomRotation()
trans = randomTranslation()
rottrans = numpy.dot(trans, rot)
inv = transRotInv(rottrans)

print rot
print trans
print rottrans
print inv

print numpy.round(numpy.dot(rottrans, inv), 2)
print numpy.round(numpy.dot(rottrans, numpy.linalg.inv(rottrans)),2)

now = time.clock()
for i in range(100000):
    x = numpy.linalg.inv(rottrans)
print time.clock() - now
now = time.clock()
for i in range(100000):
    x = transRotInv(rottrans)
print time.clock() - now

def rotInv(m):
    m[0:3,0:3] = numpy.transpose(m[0:3,0:3])
    
def transInv(m):
    m[0:3,3] = -m[0:3,3]
 
r = numpy.copy(rot)
t = numpy.copy(trans)
rotInv(r)
transInv(t)
print numpy.round(numpy.dot(numpy.dot(rot,trans), numpy.dot(t,r)),2)
   
now = time.clock()
for i in range(100000):
    r = numpy.copy(rot)
    t = numpy.copy(trans)
    x = numpy.linalg.inv(numpy.dot(r,t))
print time.clock() - now
now = time.clock()
for i in range(100000):
    r = numpy.copy(rot)
    t = numpy.copy(trans)
    rotInv(r)
    transInv(t)
    #rottrans = numpy.dot(r,t)
    x = numpy.dot(t,r)
print time.clock() - now

now = time.clock()
for i in range(100000):
    r = numpy.linalg.inv(rot)
    t = numpy.linalg.inv(trans)
    x = numpy.dot(t,r)
print time.clock() - now
now = time.clock()
for i in range(100000):
    r = numpy.copy(rot)
    t = numpy.copy(trans)
    rotInv(r)
    transInv(t)
    #rottrans = numpy.dot(r,t)
    x = numpy.dot(t,r)
print time.clock() - now
