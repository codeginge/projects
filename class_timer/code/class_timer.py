'''
This code reads a text file and creates a timer to track all activities

Format:
INPUT - text file
<minutes for the task> - <name of task>
<minutes for another task> - <name of other task>
...

OUTPUT - terminal out
:: start - 0900 
0900 - 0903
0905 - 

'''

# Create variables
class_timeline_file = "../docs/02192026.txt"
start = ""
tasks = []

# Grab all information from txt file and sort into variables
with open(class_timeline) as textfile:
	for line in textfile:
		[time, task] = line.split(" - ")
		times.append(time)
		tasks.append(task)

# Display progress through timer






