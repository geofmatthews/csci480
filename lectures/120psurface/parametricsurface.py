from visual import *
from visual.controls import *

scene.width = 500
scene.height = 500
grid = []
    
def reset():
    global grid, function
    n = shapemenu.value
    for g in grid:
        g.visible = False
    if n=="Saddle":
        init(saddle, saddleranges)
    elif n=="Torus":
        init(torus, torusranges)
    elif n=="Sphere":
        init(psphere, sphereranges)
    grid = []
    for s in srange:
        pos = [function(s,t) for t in trange]
        gridline = curve(color=color.yellow, pos=pos)
        grid.append(gridline)
    for t in trange:
        pos = [function(s,t) for s in srange]
        gridline = curve(color=color.yellow, pos=pos)
        grid.append(gridline)
    setBall()
        
def setBall():
    global srange, trange, function
    s = sslider.value
    mins = min(srange)
    maxs = max(srange)
    s = mins + 0.01*s*(maxs-mins)
    t = tslider.value
    mint = min(trange)
    maxt = max(trange)
    t = mint + 0.01*t*(maxt-mint)
    ball.pos = function(s,t)
    svec.pos = tvec.pos = nvec.pos = ball.pos
    if function == saddle:
        svec.axis = norm(vector(1,0,2*s))
        tvec.axis = norm(vector(0,1,-2*t))
        nvec.axis = norm(vector(-2*s, 2*t, 1))
    elif function == torus:
        svec.axis = norm(vector(-(1+.2*cos(t))*sin(s),
                                (1+.2*cos(t))*cos(s),
                                0.0))
        tvec.axis = norm(vector(-.2*sin(t)*cos(s),
                                -.2*sin(t)*sin(s),
                                .2*cos(t)))
        nvec.axis = norm(cross(svec.axis, tvec.axis))
    elif function == psphere:
        svec.axis = norm(vector(cos(s)*cos(t),
                                cos(s)*sin(t),
                                -sin(s)))
        tvec.axis = norm(vector(-sin(s)*sin(t),
                                sin(s)*cos(t),
                                0.0))
        nvec.axis = norm(cross(svec.axis, tvec.axis))
    else: # slower default method:
        svec.axis = norm(function(s+1.0e-10,
                                  t) - ball.pos)
        tvec.axis = norm(function(s,
                                  t+1.0e-10) - ball.pos)
        nvec.axis = norm(cross(svec.axis, tvec.axis))


def saddle(s,t):
    return vector(s, t, s*s - t*t)

saddleranges = [arange(-1,1,.1), arange(-1,1,.1)]

def torus(s,t):
    return vector((1 + .2*cos(t))*cos(s),
                  (1 + .2*cos(t))*sin(s),
                  .2*sin(t))

torusranges = [arange(0,2.01*pi,.1*pi),
               arange(0,2.01*pi,.2*pi)]

def psphere(s,t):
    return vector(sin(s)*cos(t),
                  sin(s)*sin(t),
                  cos(s))
sphereranges = [arange(0,1.01*pi, .1*pi),
                arange(0,2.01*pi, .1*pi)]


def init(func, ranges):
    global function, srange, trange
    function = func
    srange,trange = ranges

init(saddle, saddleranges)

ball = sphere(radius = 0.1, color=color.cyan, pos=(min(srange), min(trange)))
svec = arrow(color=color.red, pos=ball.pos, axis=(1,0,0))
tvec = arrow(color=color.green, pos=ball.pos, axis=(0,1,0))
nvec = arrow(color=color.blue, pos=ball.pos, axis=(0,0,1)) 

c = controls(x=512,y=0,width=500,height=500)
sslider = slider(pos = (-64,64),
                 action=lambda: setBall(),
                 color=color.red)
tslider = slider(pos = (-64,32),
                 action= lambda: setBall(),
                 color=color.green)

shapemenu = menu(width=64,height=12,text="Shape")
shapemenu.items.append(("Saddle", lambda: reset()))
shapemenu.items.append(("Sphere", lambda: reset()))
shapemenu.items.append(("Torus", lambda: reset()))

reset()


