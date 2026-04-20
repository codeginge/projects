"""
BUILD PROBLEM SPACE
By: Michael Roberts 
Last Updated: 4/20/2026

This code is designed for a two arm robotic drawing robot. This code creates a reference table for use in reverse kinematics. The code will loop through all avalible angle positions for both servos and output the (x,y) coordinate they corrispond to.
"""

import math
import csv
import matplotlib.pyplot as plt


def coordinate_calculation(theta_1, link_1, theta_2, link_2):
    theta_1_rads = math.radians(theta_1)
    theta_2_rads = math.radians(theta_2) 
    x_link_1 = link_1*math.cos(theta_1_rads)
    y_link_1 = link_1*math.sin(theta_1_rads)
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
    input_domain = []
    output_range = []
    for i in range(servo_angle_min, servo_angle_max, step): # loop through all theta_1 possibilities
        for j in range(servo_angle_min, servo_angle_max, step): # go through all theta_2 possibilities
            input_domain.append((i,j))
            output_range.append((coordinate_calculation(i, link_1_length, j, link_2_length)))
    return (input_domain, output_range)


def save_to_csv(data, filename):
    with open(filename,mode='w',newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['theta_1','theta_2','x_value','y_value'])
        angle_data = data[0]
        coordinate_data = data[1]
        for i in range(len(angle_data)):
            t1,t2 = angle_data[i]
            x,y = coordinate_data[i]
            writer.writerow([t1,t2,x,y])
    print(f"File written to {filename}")


def build_problem_space_plot(data, filename):
    theta_1_angles, theta_2_angles = data[0]
    x_coordinates, y_coordinates = data[1]
    plt.figure(figsize=(8,8))
    plt.scatter(x_coordinates, y_coordinates, s=1, c='blue', alpha=0.5) # s, c, and alpha relate to the dot size, color and transparency
    plt.title("2-Arm Linkage Problem Space")
    plt.xlabel("X Position (MM)")
    plt.ylabel("Y Position (MM)")
    plt.grid(True)
    plt.axis('equal')
    plt.show()
    plt.savefig(filename)
    print(f"Plot saved to file {filename}")


data=(build_problem_space(0, 181, 1, 3, 3))
filename="/Users/michael/Desktop/projects/robotics/code/2_arm_problem_space.csv"
build_problem_space_plot(data,filename)
save_to_csv(data,filename)

