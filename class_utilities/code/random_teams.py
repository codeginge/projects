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
    --team_members 4 \
    --roster "./class.txt"

'''

import argparse, random, math

def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--team_members", type=int, required=True, help="variable description")
    parser.add_argument("--roster", type=str, required=True, help="text file with a student's name per line")
    return parser.parse_args()

def parse_names(roster):
    with open(roster, "r") as file:
        names = file.read().splitlines()
        return(names)

if __name__ == "__main__":
    args = parse_args()
    team_members = args.team_members
    roster = args.roster

    students = parse_names(roster)
    num_teams = math.ceil(len(students)/team_members)
    teams = [[] for _ in range(num_teams)]
    while len(students) != 0:
        for t in range(num_teams):
            if len(students) != 0:
                rand_student = random.choice(students)
                teams[t].append(rand_student)
                students.remove(rand_student)
    for t in range(num_teams):
        print(f"team {t}:")
        for member in teams[t]:
            print(member)
