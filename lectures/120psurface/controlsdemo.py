from visual.controls import *
 
def change(): # Called by controls when button clicked
    if b.text == 'Click me':
        b.text = 'Try again'
    else:
        b.text = 'Click me'
 
c = controls() # Create controls window
# Create a button in the controls window:
b = button( pos=(0,0), width=60, height=60, 
              text='Click me', action=lambda: change() )
