'''
code: sort_students.py
by: Michael Roberts
last updated: 9/10/26

## code description: 
this code will sort students by name, block, and class depending on the settings you choose. 
First use case is for sorting by class then by lastname for student bin organization. 

inputs:
file - expected file type is a CSV file with the following header as the first line
    last, first, block, class

Build python environment:
python3 -m venv myenv
source myenv/bin/activate
pip install ... 

## example script call:
python3 ./sort_students.py --sort_order "0,2" --file "/directory/file.csv"

'''

import argparse

def student_sort(sort_order, file):
    with open(file, "r") as current_file:
        students = current_file.read().splitlines()
        headers = students[0]
        students = students[1:]
        print(headers)
        for col in sort_order.split(','):
            students.sort(key = lambda x: x.split(',')[int(col)].strip())
        return(students) 

def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--sort_order", type=str, help="rows to sort and the priority order")
    parser.add_argument("--file", type=str, help="file with student roster")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    students = student_sort(args.sort_order, args.file)
    for s in students:
        print(s)
