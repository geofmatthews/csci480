from visual import *
from visual.controls import *

scene.background = color.gray(0.5)
scene.ambient = color.gray(0.5)

stepsize = 0.25
limits = arange(0,1+stepsize,stepsize)
boxes = []
for red in limits:
    for green in limits:
        for blue in limits:
            color = vector(red,green,blue)
            b = box(pos=color-vector(0.5,0.5,0.5),
                    color=color,
                    length=stepsize*0.5,
                    width=stepsize*0.5,
                    height=stepsize*0.5)
            b.mins = (red < 0.01, green < 0.01, blue < 0.01)
            b.maxs = (red > 0.99, green > 0.99, blue > 0.99)
            boxes.append(b)

def toggleAxes():
    for b in boxes:
        min01 = b.mins[0] and b.mins[1]
        min02 = b.mins[0] and b.mins[2]
        min12 = b.mins[1] and b.mins[2]
        max01 = b.maxs[0] and b.maxs[1]
        max02 = b.maxs[0] and b.maxs[2]
        max12 = b.maxs[1] and b.maxs[2]
        if not(max01 or max02 or max12) and not(min01 or min02 or min12):
            b.visible = not b.visible
                

t1 = toggle(pos=(10,10), width=20, height=20,
            text0 = 'Cube',
            text1 = 'Axes',
            action = lambda: toggleAxes())
            
            
