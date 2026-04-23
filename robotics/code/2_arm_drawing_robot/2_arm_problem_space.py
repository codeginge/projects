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


def forward_kinematics(theta_1, link_1, theta_2, link_2):
    theta_1_rads = math.radians(theta_1)
    theta_2_rads = math.radians(theta_2) 
    x_link_1 = link_1*math.cos(theta_1_rads)
    y_link_1 = link_1*math.sin(theta_1_rads)
    x_link_2 = link_2*math.cos(theta_1_rads - theta_2_rads)
    y_link_2 = link_2*math.sin(theta_1_rads - theta_2_rads)
    x_sum = x_link_1 + x_link_2
    y_sum = y_link_1 + y_link_2
    coordinates = (x_sum, y_sum)
    return coordinates


def inverse_kinematics(x, y, link_1, link_2):
    theta_2 = math.acos((x**2+y**2-link_1**2-link_1**2)/(-2*link_1*link_2))
    theta_1 = math.atan(y/x) - math.atan((link_2*math.sin(theta_2))/(link_1+link_2*math.cos(theta_2)))
    angles = (theta_1, theta_2)
    return angles 


def build_problem_space(servo_angle_min, servo_angle_max, step, link_1_length, link_2_length): 
    """
    this function will build the domain and range of the problem space based off of servo range and link length
    """
    input_domain = []
    output_range = []
    for i in np.arange(servo_angle_min, servo_angle_max, step): # loop through all theta_1 possibilities
        for j in np.arange(servo_angle_min, servo_angle_max, step): # go through all theta_2 possibilities
            input_domain.append((i,j))
            output_range.append((forward_kinematics(i, link_1_length, j, link_2_length)))
    return (input_domain, output_range)


def ik_fk_coordinate_error(x_desired, y_desired, link_1, link_2, step):
    (theta_1_ik, theta_2_ik) = inverse_kinematics(x_desired,y_desired,link_1,link_2)
    (theta_1_ik_nearest_step, theta_2_ik_nearest_step) = (round(theta_1_ik / step) * step, round(theta_2_ik / step) * step) # round thetas to nearest step
    (x_actual, y_actual) = forward_kinematics(theta_1_ik_nearest_step, link_1, theta_2_ik_nearest_step, link_2)
    error_coordinates = (x_desired-x_actual, y_desired-y_actual)
    return error_coordinates


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


def build_scatter_plot(data, check_data_points, filename, link_1, link_2, step):
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
        errors.append(ik_fk_coordinate_error(x_desired, y_desired, link_1, link_2, step))
    print(f"{errors}/n/n{check_data_points}")
    plt.figure(figsize=(8,8))

    # draw desired points to check and links and angles to create them from IK
    plt.scatter(check_data_points[0],check_data_points[1],s=10,c='green',alpha=0.5)
    for i in range(len(check_data_points[0])):
        (x_i, y_i) = (check_data_points[0][i], check_data_points[1][i])
        (theta_1, theta_2) = inverse_kinematics(x_i, y_i, link_1, link_2)
        print(f"x: {x_i}, y: {y_i}, theta 1: {math.degrees(theta_1)}, theta 2: {math.degrees(theta_2)}")
        (link_1_x, link_1_y) = (link_1*math.cos(theta_1), link_1*math.sin(theta_1)) 
        (link_2_x, link_2_y) = (link_2*math.cos(theta_2), link_2*math.sin(theta_2))
        plt.plot([0,link_1_x],[0,link_1_y],color='green',linestyle='--',linewidth=1)
        plt.plot([link_1_x,link_1_x+link_2_x],[link_1_y,link_1_y+link_2_y],color='green',linestyle='--',linewidth=1)

    # draw points of reachable space
    plt.scatter(x_coordinates, y_coordinates, s=1, c='blue', alpha=0.5) # s, c, and alpha relate to the dot size, color and transparency
    plt.plot([0,link_1],[0,0],color='black',linestyle='--',linewidth=2)
    plt.plot([link_1,(link_1 + link_2)],[0,0],color='red',linestyle='--',linewidth=2)
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
    return parser.parse_args()


if __name__ == "__main__":
    args = argument_parser()
    data = build_problem_space(args.min, args.max, args.step, args.link_1, args.link_2)
    check_data_points = generate_randomized_data_points(data, args.datapoints_desired) # generate points to check 
    build_scatter_plot(data, check_data_points, args.file, args.link_1, args.link_2, args.step)
    save_to_csv(data,args.file)


