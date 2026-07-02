'''
code: random_teams.py 
by: Michael Roberts
last updated: 07/02/2026

## code description:
this code will access a csv file of names and then randomly create teams based on the number of people in the list and how many people per team set by the user

Build python environment:
python3 -m venv myenv
source myenv/bin/activate 

## example script call:
python3 ./random_teams.py \
    --people 4 \
    --roster "./class.txt"

'''

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--people", type=int, required=True, help="variable description")
    parser.add_argument("--roster", type=str, required=True, help="text file with a student's name per line")
    return parser.parse_args()

def parse_names(roster):
    with open(roster, "r") as file:
        names = file.read().splitlines()
        return(names)

if __name__ == "__main__":
    args = parse_args()
    people = args.people
    roster = args.roster

    students = parse_names(roster)
    for student in students:
        print(student)

