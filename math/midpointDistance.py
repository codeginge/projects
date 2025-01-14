import math
import matplotlib.pyplot as plt
import random

""" 
This code takes the problemSet as a given array of [x1,y1,x2,y2] values 
and computes the midpoint and distance between them and plots each problem. 
Max of 15 problems 
"""

randomize = False

problemSet = [[-2,8,7,4],[1,0,3,4],[-4,10,5,6],[6,9,-2,-2],[10,-1,10,10],
              [7,-4,6,-5],[11,3,4,-7],[12,-4,2,4],[-5,-7,4,6],[4,7,1,2],
              [11,17,26,4],[6,2,-10,6],[0,0,12,2],[-2,-4,10,6],[4,7,4,9]]

def midpointDistance(probNum,x1,y1,x2,y2):
    # Calculations
    mx = round((x1+x2)/2,2)
    my = round((y1+y2)/2,2)
    sqr = math.fabs((x2-x1)**2+(y2-y1)**2)
    dis = round(math.sqrt(sqr),2)
    print("Problem #{}: Point A = ({},{}), Point B = ({},{})\nMidpoint = ({},{}) | Distance = {} or sqrt({})".format(probNum,x1,y1,x2,y2,mx,my,dis,sqr))
    
    # Plotting
    x=[x1,mx,x2]
    y=[y1,my,y2]
    plt.subplot(5,3,probNum)
    plt.plot(x,y,marker="o", markersize=2, markeredgecolor="red", markerfacecolor="green")

    # Add labels
    plt.title(f'Problem {probNum}', fontsize=8)
    plt.xlabel('X-axis', fontsize=8)
    plt.ylabel('Y-axis', fontsize=8)
    plt.tick_params(axis='both', which='major', labelsize=6)

def generate_random_problem_set(num_problems, x_range, y_range):
    """
    Generate a problem set with random coordinates.
    
    Parameters:
    - num_problems: Number of problems to generate.
    - x_range: Tuple (min_x, max_x) specifying the range for x coordinates.
    - y_range: Tuple (min_y, max_y) specifying the range for y coordinates.
    
    Returns:
    - A list of problems, each represented by a list [x1, y1, x2, y2].
    """
    problem_set = []
    for _ in range(num_problems):
        x1 = random.randint(*x_range)
        y1 = random.randint(*y_range)
        x2 = random.randint(*x_range)
        y2 = random.randint(*y_range)
        problem_set.append([x1, y1, x2, y2])
    return problem_set

if randomize == True:
    problemSet = generate_random_problem_set(15,(-20,20),(-20,20))

for i in range(len(problemSet)):
    probNum = i + 1
    [x1,y1,x2,y2] = problemSet[i]
    midpointDistance(probNum,x1,y1,x2,y2)

plt.subplots_adjust(hspace=0.7)
plt.show()
