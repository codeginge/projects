"""
BUILD PROBLEM SPACE
By: Michael Roberts 
Last Updated: 4/20/2026

This code is designed for a two arm robotic drawing robot. This code creates a reference table for use in reverse kinematics. The code will loop through all avalible angle positions for both servos and output the (x,y) coordinate they corrispond to.
"""

import math


def coordinate_calculation(theta_1, link_1, theta_2, link_2):
    theta_1_rads = math.radians(theta_1)
    theat_2_rads = math.radians(theta_2) 
    x_link_1 = link_1*math.cos(theta_1_rads)
    y_link_1 = link_1*math.sin(theat_1_rads)
    x_link_2 = link_2*math.cos(theta_2_rads)
    y_link_2 = link_2*math.sin(theta_2_rads)
    x_sum = x_link_1 + x_link_2
    y_sum = y_link_1 + y_link_2
    coordinates = (x_sum, y_sum)
    return coordinates


def build_problem_space(servo_angle_min, servo_angle_max, step, link_1_length, link_2_length): 
    """
    this function will build the domain and range of the problem space based off of servo range and link length
    """
    domain = []
    range = []
    for i in range(servo_angle_min, servo_angle_max, step): // loop through all theta_1 possibilities
        for j in range(servo_angle_min, servo_angle_max, step): // go through all theta_2 possibilities
            domain.append(i,j)
            range.append(coordinate_calculation(i, link_1_length, j, link_2_length))
    return (domain, range)


print(build_problem_space(0, 181, 1, 3, 3))

