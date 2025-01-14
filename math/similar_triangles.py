'''
similar_triangles.py is a random triangle generator to help aid teaching content
related to similar triangles by creating two similar triangles.
'''

import turtle, random, math, time

def draw_triangle_0(sf, t, side_1, side_2, side_3,angle_1, angle_2, angle_3, added_rotation, solved):
	scale_factor=sf*100
	t.setheading(angle_1+added_rotation)
	t.forward(side_1*scale_factor/side_1)
	t.setheading(angle_2+added_rotation)
	t.forward(side_2*scale_factor/side_1)
	t.setheading(angle_3+added_rotation)
	t.forward(side_3*scale_factor/side_1)
	dist= 100
	if added_rotation>180: dist= -100
	t.penup()
	t.setheading(270)
	t.forward(dist)
	t.pendown()
	if solved == 1:
		triangle_data = "angles = {}, {}, {}\n sides = {}, {}, {}".format(round(180-(360-angle_3),2),round(180-angle_2,2),round(180-(angle_3-angle_2),2),round(side_1*sf,2),round(side_2*sf,2),round(side_3*sf,2))
	if solved == 0:
		triangle_data = "angles = {}, {}, {}\n sides = {}, ____, ____".format(round(180-(360-angle_3),2),round(180-angle_2,2),round(180-(angle_3-angle_2),2),round(side_1*sf,2))
	t.write(triangle_data, align="center", font=("Arial", 20, "normal"))


def draw_triangle_1(sf, t, side_1, side_2, side_3,angle_1, angle_2, angle_3, added_rotation, solved):
	scale_factor=sf*100
	t.setheading(angle_1+added_rotation)
	t.forward(side_1*scale_factor/side_1)
	t.setheading(angle_2+added_rotation)
	t.forward(side_2*scale_factor/side_1)
	t.setheading(angle_3+added_rotation)
	t.forward(side_3*scale_factor/side_1)
	dist= 100
	if added_rotation>180: dist= -100
	t.penup()
	t.setheading(270)
	t.forward(dist)
	t.pendown()
	if solved == 1:
		triangle_data = "angles = {}, {}, ____\n sides = {}, {}, {}".format(round(180-(360-angle_3),2),round(180-angle_2,2),round(side_1*sf,2),round(side_2*sf,2),round(side_3*sf,2))
	if solved == 0:
		triangle_data = "angles = {}, ____, {}\n sides = {}, ____, ____".format(round(180-(360-angle_3),2),round(180-(angle_3-angle_2),2),round(side_1*sf,2))
	t.write(triangle_data, align="center", font=("Arial", 20, "normal"))


def draw_triangle_2(sf, t, side_1, side_2, side_3,angle_1, angle_2, angle_3, added_rotation, solved):
	scale_factor=sf*100
	t.setheading(angle_1+added_rotation)
	t.forward(side_1*scale_factor/side_1)
	t.setheading(angle_2+added_rotation)
	t.forward(side_2*scale_factor/side_1)
	t.setheading(angle_3+added_rotation)
	t.forward(side_3*scale_factor/side_1)
	dist= 100
	if added_rotation>180: dist= -100
	t.penup()
	t.setheading(270)
	t.forward(dist)
	t.pendown()
	if solved == 1:
		triangle_data = "angles = {}, {}, {}\n sides = {}, {}, {}".format(round(180-(360-angle_3),2),round(180-angle_2,2),round(180-(angle_3-angle_2),2),round(side_1*sf,2),round(side_2*sf,2),round(side_3*sf,2))
	if solved == 0:
		triangle_data = "angles = _____, _____, _____\n sides = {}, {}, {}".format(round(side_1*sf,2),round(side_2*sf,2),round(side_3*sf,2))
	t.write(triangle_data, align="center", font=("Arial", 20, "normal"))


def draw_triangle_3(sf, t, side_1, side_2, side_3,angle_1, angle_2, angle_3, added_rotation, solved):
	scale_factor=sf*100
	t.setheading(angle_1+added_rotation)
	t.forward(side_1*scale_factor/side_1)
	t.setheading(angle_2+added_rotation)
	t.forward(side_2*scale_factor/side_1)
	t.setheading(angle_3+added_rotation)
	t.forward(side_3*scale_factor/side_1)
	dist= 100
	if added_rotation>180: dist= -100
	t.penup()
	t.setheading(270)
	t.forward(dist)
	t.pendown()
	if solved == 1:
		triangle_data = "angles = {}, {}, {}\n sides = {}, {}, {}".format(round(180-(360-angle_3),2),round(180-angle_2,2),round(180-(angle_3-angle_2),2),round(side_1*sf,2),round(side_2*sf,2),round(side_3*sf,2))
	if solved == 0:
		triangle_data = "angles = _____, _____, _____\n sides = {}, {}, {}".format(round(side_1*sf,2),round(side_2*sf,2),round(side_3*sf,2))
	t.write(triangle_data, align="center", font=("Arial", 20, "normal"))


def move_start(t, x, y):
	t.penup()
	t.goto(x, y)
	t.pendown()


def gen_tri(t,tri):
	t.showturtle()
	triangle_type=random.randrange(0,5,1)
	#triangle_type=4
	#0 - equilateral triangle 		1-1-1
	#1 - isoceles right triangle 	1-1-sqrt(2)
	#2 - right triangle 			30-60-90
	#3 - right trianlge 			3-4-5
	#4 - right trianlge 			5-12-13



	if triangle_type == 0:
		[s1,s2,s3,a1,a2,a3]=[1,1,1,0,120,240]
	if triangle_type == 1:
		[s1,s2,s3,a1,a2,a3]=[1,math.sqrt(2),1,0,135,270]
	if triangle_type == 2:
		[s1,s2,s3,a1,a2,a3]=[3,2*math.sqrt(3),math.sqrt(3),0,150,270]
	if triangle_type == 3:
		[s1,s2,s3,a1,a2,a3]=[4,5,3,0,143.13,270]
	if triangle_type == 4:
		[s1,s2,s3,a1,a2,a3]=[12,13,5,0,157.38,270]

	t.clear()
	t1_rotation=random.randrange(0,360,1)
	t2_rotation=random.randrange(0,360,1)
	move_start(t,-200,0)
	if tri == 1:
		draw_triangle_0(1,t,s1,s2,s3,a1,a2,a3,t1_rotation,1)
		move_start(t,200,0)
		sf=random.randrange(2,4,1)
		draw_triangle_0(sf,t,s1,s2,s3,a1,a2,a3,t2_rotation,0)
	if tri == 2:
		draw_triangle_1(1,t,s1,s2,s3,a1,a2,a3,t1_rotation,1)
		move_start(t,200,0)
		sf=random.randrange(2,4,1)
		draw_triangle_1(sf,t,s1,s2,s3,a1,a2,a3,t2_rotation,0)
	if tri == 3:
		draw_triangle_2(1,t,s1,s2,s3,a1,a2,a3,t1_rotation,1)
		move_start(t,200,0)
		sf=random.randrange(2,4,1)
		draw_triangle_2(sf,t,s1,s2,s3,a1,a2,a3,t2_rotation,0)
	t.hideturtle()

# create a turtle object
t = turtle.Turtle()
num_problems=5
for x in range(0,num_problems):
	gen_tri(t,1)
	input("Press Enter to continue...")
	#time.sleep(3)
for x in range(0,num_problems):
	gen_tri(t,2)
	input("Press Enter to continue...")
	#time.sleep(3)
for x in range(0,num_problems):
	gen_tri(t,3)
	input("Press Enter to continue...")
	#time.sleep(3)

turtle.done()

