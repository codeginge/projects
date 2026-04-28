"""
BUILD PROBLEM SPACE
By: Michael Roberts 
Last Updated: 4/20/2026

This code is designed for a two arm robotic drawing robot. This code creates a reference table for use in reverse kinematics. The code will loop through all avalible angle positions for both servos and output the (x,y) coordinate they corrispond to.

Build python env using the following:
python3 -m venv myenv 
source myenv/bin/activate
pip install matplotlib

Run Example:
python3 ./2_arm_problem_space.py --max 120 --min 0 --step 5 --link_1 3.25 --link_2 7 --file "/Users/michael/Desktop/projects/robotics/code/2_arm_drawing_robot/2_arm_problem_space"
"""

import math
import csv
import matplotlib.pyplot as plt
import argparse
import numpy as np
import random


def forward_kinematics(theta_1, link_1, theta_2, link_2, output_type, offset):
    # angle input = radians
    x_link_1 = link_1*math.cos(theta_1)
    y_link_1 = link_1*math.sin(theta_1)
    x_link_2 = link_2*math.cos(theta_1 + theta_2 + offset)
    y_link_2 = link_2*math.sin(theta_1 + theta_2 + offset)
    coordinate_parts = (x_link_1, y_link_1, x_link_2, y_link_2)
    x_sum = x_link_1 + x_link_2
    y_sum = y_link_1 + y_link_2
    coordinate_sum = (x_sum, y_sum)
    if output_type == "sum": 
        return coordinate_sum
    if output_type == "parts":
        return coordinate_parts


def inverse_kinematics(x, y, link_1, link_2, arm_type, offset):
    # angle input = radians
    if arm_type == "elbow_up":
        elbow_coefficient = -1
    if arm_type == "elbow_down":
        elbow_coefficient = 1
    if math.sqrt(x*x + y*y) < link_1 + link_2:
        # angle output is in radians
        theta_2 = (math.acos((x*x+y*y-link_1*link_1-link_2*link_2)/(2*link_1*link_2)) - offset)*elbow_coefficient
        theta_1 = math.atan2(y, x) - math.atan2((link_2*math.sin(theta_2)),(link_1+link_2*math.cos(theta_2)))
        angles = (theta_1, theta_2)
        return angles
    else:
        print(f"point ({x},{y}) is outside reachable area") 


def build_problem_space(servo_angle_min, servo_angle_max, step, link_1_length, link_2_length, arm_type, offset_degrees): 
    """
    this function will build the domain and range of the problem space based off of servo range and link length
    input domain is degrees
    output range is coordinates
    """
    offset = math.radians(offset_degrees)
    input_domain = []
    output_range = []
    for i in np.arange(servo_angle_min, servo_angle_max, step): # loop through all theta_1 possibilities
        for j in np.arange(servo_angle_min, servo_angle_max, step): # go through all theta_2 possibilities
            i_rads = math.radians(i)
            if arm_type == "elbow_up":
                j_rads = -math.radians(j)
            else: 
                j_rads = math.radians(j)
            input_domain.append((i,j))
            FK = forward_kinematics(i_rads, link_1_length, j_rads, link_2_length, "sum", offset) # theta_2 put it as a negative
            output_range.append(FK)
    return (input_domain, output_range)


def ik_fk_coordinate_error(x_desired, y_desired, link_1, link_2, step, arm_type, offset):
    IK = inverse_kinematics(x_desired, y_desired, link_1, link_2, arm_type, offset)
    if IK is not None:
        (theta_1_ik_rads, theta_2_ik_rads) = IK
        (theta_1_ik, theta_2_ik) = (math.degrees(theta_1_ik_rads), math.degrees(theta_2_ik_rads)) # convert to degrees
        (theta_1_ik_nearest_step, theta_2_ik_nearest_step) = (round(theta_1_ik / step) * step, round(theta_2_ik / step) * step) # round degrees down to nearest step
        (x_actual, y_actual) = forward_kinematics(math.radians(theta_1_ik_nearest_step), link_1, math.radians(theta_2_ik_nearest_step), link_2, "sum", offset) # calculate new FK
        error_coordinates = (x_desired-x_actual, y_desired-y_actual) # get error between FK rounded step and actual 
        return error_coordinates
    else:
        return ("NA","NA")

def save_to_csv(data, filename):
    with open(f"{filename}.csv",mode='w',newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['theta_1','theta_2','x_value','y_value'])
        angle_data = data[0]
        coordinate_data = data[1]
        for i in range(len(angle_data)):
            t1,t2 = angle_data[i]
            x,y = coordinate_data[i]
            writer.writerow([t1,t2,x,y])
    print(f"File written to {filename}.csv")


def generate_randomized_data_points(data, datapoints_desired):
    xy_list = data[1]
    x_coordinates, y_coordinates = [], []
    selected_data = random.sample(range(len(xy_list)), datapoints_desired) # random_entries
    for i in range(len(xy_list)):
        if i in selected_data:
            x_coordinates.append(round((xy_list[i][0]),1))
            y_coordinates.append(round((xy_list[i][1]),1))
    randomized_data = (x_coordinates, y_coordinates)
    return randomized_data


def build_scatter_plot(data, check_data_points, filename, link_1, link_2, step, arm_type, offset_degrees):
    offset = math.radians(offset_degrees)
    theta_list = data[0]
    xy_list = data[1]
    theta_1_angles, theta_2_angles, x_coordinates, y_coordinates = [], [], [], []
    for i in range(len(theta_list)):
        theta_1_angles.append(theta_list[i][0])
        theta_2_angles.append(theta_list[i][1])
        x_coordinates.append(xy_list[i][0]) 
        y_coordinates.append(xy_list[i][1])
    errors = []
    for i in range(len(check_data_points[0])):
        # for each coordinate calculate error
        x_desired = check_data_points[0][i]
        y_desired = check_data_points[1][i]
        errors.append(ik_fk_coordinate_error(x_desired, y_desired, link_1, link_2, step, arm_type, offset))
    plt.figure(figsize=(8,8))

    # draw desired points to check and links and angles to create them from IK
    plt.scatter(check_data_points[0],check_data_points[1],s=30,c='green',alpha=0.5)
    for i in range(len(check_data_points[0])):
        (x_i, y_i) = (check_data_points[0][i], check_data_points[1][i])
        IK = inverse_kinematics(x_i, y_i, link_1, link_2, arm_type, offset)
        if IK is None: continue
        (theta_1, theta_2) = IK
        info = f"x: {x_i}, y: {y_i} \nt_1: {round(math.degrees(theta_1), 2)}, t_2: {round(math.degrees(theta_2), 2)}"
        (link_1_x_i, link_1_y_i, link_2_x_i, link_2_y_i) = forward_kinematics(theta_1, link_1, theta_2, link_2, "parts", offset) 
        plt.plot([0,link_1_x_i],[0,link_1_y_i],color='black',linestyle='--',linewidth=2)
        plt.plot([link_1_x_i,link_1_x_i+link_2_x_i],[link_1_y_i,link_1_y_i+link_2_y_i],color='red',linestyle='--',linewidth=2)
        plt.text(x_i-1,y_i+.2,info,fontsize=8,color='black')

    # draw points of reachable space
    plt.scatter(x_coordinates, y_coordinates, s=1, c='blue', alpha=0.5) # s, c, and alpha relate to the dot size, color and transparency
    plt.title("2-Arm Linkage Problem Space")
    plt.xlabel("X Position (IN)")
    plt.ylabel("Y Position (IN)")
    plt.grid(True)
    plt.axis('equal')
    plt.autoscale(enable=True, axis='both', tight=None)
    plt.savefig(f"{filename}.png")
    print(f"Plot saved to file {filename}.png")


def argument_parser():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--min", type=float, required=True, help="minimum servo angle")
    parser.add_argument("--max", type=float, required=True, help="maximum servo angle")
    parser.add_argument("--step", type=float, required=True, help="servo angle step size")
    parser.add_argument("--link_1", type=float, required=True, help="link 1 length (inches)")
    parser.add_argument("--link_2", type=float, required=True, help="link 2 length (inches)")
    parser.add_argument("--file", type=str, required=True, help="file location (/DIR/filename) for output .csv and .png files")
    parser.add_argument("--datapoints_desired", type=int, required=True, help="number of points to check if forward and reverse kinematic equations are working as expected")
    parser.add_argument("--arm_type", type=str, required=True, help="avaliable arm types are elbow_up and elbow_down")
    parser.add_argument("--offset_degrees", type=float, required=True, help="starting degree offset for theta_2")
    return parser.parse_args()


if __name__ == "__main__":
    args = argument_parser()
    data = build_problem_space(args.min, args.max, args.step, args.link_1, args.link_2, args.arm_type, args.offset_degrees)
    check_data_points = generate_randomized_data_points(data, args.datapoints_desired) # generate points to check 
    build_scatter_plot(data, check_data_points, args.file, args.link_1, args.link_2, args.step, args.arm_type, args.offset_degrees)
    save_to_csv(data,args.file)


