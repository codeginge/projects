#TODO pause after each drawing cycle
#TODO add #circle and #regions counter below drawing... table of values

# Find the number of regions for all circles from min to max
time_delay=1
min=2000
max=3000
r=[]
n_circles=list(range(min,max))
for c in n_circles:
    r.append(c*c-(c-1))

# Draw overlapping circles 
circle_size = 130
radius_from_origin = 100
draw_speed = 50

import turtle
import numpy as np
import math
import time

t=turtle.Turtle()
for n in n_circles:
    angle = 0
    angle_increment = 360/n
    t.speed(15)
    t.up()
    t.setx(0)
    t.sety(-150)    
    text='Circles = {}, Regions = {}'.format(n,(n*n-(n-1)))
    t.write(text,True, align="center",font=('Arial',30,'bold'))
    for c in list(range(1,n+1)):
        t.speed(draw_speed)
        t.up()
        t.setx(radius_from_origin*np.cos(math.radians(angle)))
        t.sety(radius_from_origin*np.sin(math.radians(angle)))
        t.down()
        t.circle(circle_size)
        angle += angle_increment
    time.sleep(time_delay)
    t.clear()
