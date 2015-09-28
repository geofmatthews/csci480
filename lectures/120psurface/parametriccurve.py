from visual import *
from visual.controls import *

scene.width = 500
scene.height = 500

def f(t):
    return vector(10*cos(t), 10*sin(t), t)
def tf(t):
    return vector(-10*sin(t), 10*cos(t), 1)/2
def nf(t):
    return vector(-10*cos(t), -10*sin(t), 0)/2
def bf(t):
    #return vector(1*sin(t), 1*cos(t), 10*sin(t)*sin(t)+10*cos(t)*cos(t))/2
    return vector(1*sin(t), 1*cos(t), 10)/2

trange = arange(0,4*pi,0.1)

pos = [f(t) for t in trange]

helix = curve(color=color.yellow,pos=pos)

ball = sphere(color=color.red,pos=f(0.0))
tvec = arrow(color=color.red, pos=ball.pos, axis=(1,0,0))
nvec = arrow(color=color.green, pos=ball.pos, axis=(0,1,0))
bvec = arrow(color=color.blue, pos=ball.pos, axis=(0,0,1)) 

def setBall():
    ball.pos = f(tslider.value)
    tvec.pos = nvec.pos = bvec.pos = ball.pos
    tvec.axis = tf(tslider.value)
    nvec.axis = nf(tslider.value)
    bvec.axis = bf(tslider.value)

c = controls(x=0,y=500,width=500,height=128)

tslider = slider(
    pos=(-64,0),
    length=128,
    min=0.0, max=4*pi,
    action=setBall)
