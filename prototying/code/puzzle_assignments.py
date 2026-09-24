'''
code: puzzle_assignments.py 
by: Michael Roberts
last updated: 09/23/26

## code description:
+ build puzzle matrix
+ build shared sides list by checking each puzzle piece and adding LRTB neighbors (left,right,top,bottom) 
+ randomly assign puzzle pieces to students. pieces with the most neighbors first 
+ add responsibility for sides to student list
+ students should have the same number of sides to work on +-1 side
- students should not be neighbors to the same person more than twice 
+ run simulations until conditions are met
- show visual using turtle graphics with piece and side assignments

## datasets
puzzle_pieces = ['A0','A1','A2',
                 'B0','B1','B2',
                 'C0','C1','C2']

shared_sides = [A0B0, A0A1, A1A2, A1B1, A2B2, 
                B0C0, B0B1, B1C1, B1B2, B2C2, 
                C0C1, C1C2]

students = ['jim,A0,A2,C1,A0B0,A2A1,C1C0,C1C2',
            'bob,A1,B2,B1,B1B2,A1A0,B1A1,A2B2',
            'joe,C2,C0,B0,B0B1,C2B2,C1B1,B0C0']

Build python environment:
python3 -m venv myenv
source myenv/bin/activate
pip install  

## example script call:
python3 ./script.py \
    --var1 20

'''

import argparse, turtle, random

def build_puzzle(args):
    puzzle_pieces = []
    for i in range(args.width):
        for j in range (args.height):
            piece = f"{chr(i+65)}{j}"
            puzzle_pieces.append(piece)
    return puzzle_pieces

def build_shared_sides(args, puzzle_pieces):
    shared_sides = []
    for index, p in enumerate(puzzle_pieces):
        # check right
        if (str(args.width - 1) not in p):
            right_side = f"{p}{puzzle_pieces[index + 1]}"
            shared_sides.append(right_side)
        # check bottom
        if (chr(args.height + 65 - 1) not in p):
            bottom_side = f"{p}{puzzle_pieces[index + args.width]}"
            shared_sides.append(bottom_side)
    return shared_sides

def assign_pieces(args, puzzle_pieces):
    assigned_students = args.students.split(",")
    student_index = 0
    while puzzle_pieces:
        p = random.choice(puzzle_pieces)
        puzzle_pieces.remove(p)
        if student_index >= len(assigned_students):
            student_index -= len(assigned_students)
        assigned_students[student_index] = f"{assigned_students[student_index]},{p}"
        student_index += 1
    return assigned_students

def assign_sides(args, assigned_students, shared_sides):
    student_index = 0
    if not args.match_attempts:
        match_attempts = 50
    else: 
        match_attempts = args.match_attempts
    loop_iterations = 0
    while shared_sides:
        side_to_assign = random.choice(shared_sides)
        if student_index >= len(assigned_students):
            student_index -= len(assigned_students)
        student_puzzle_pieces = "" 
        student_data= assigned_students[student_index].split(",")[1:]
        for item in student_data:
            if len(item) == 2:
                student_puzzle_pieces =f"{student_puzzle_pieces}{item}"
        if (side_to_assign[:2] in student_puzzle_pieces or side_to_assign[-2:] in student_puzzle_pieces):
            #print(f"{side_to_assign[:2]} or {side_to_assign[-2:]} in {student_puzzle_pieces}")
            assigned_students[student_index] = f"{assigned_students[student_index]},{side_to_assign}"
            student_index += 1
            shared_sides.remove(side_to_assign)
        loop_iterations += 1
        if loop_iterations > match_attempts:
            student_index += 1
            loop_iterations = 0 
    return assigned_students

def match_distribution_criteria(args, assigned_students):
    match_distribution_criteria = False
    sides = []
    for s in assigned_students:
        count = 0
        for data in s.split(",")[1:]:
            if len(data) == 4:
                count += 1
        sides.append(count)
    if (max(sides)-min(sides) < args.dist):
        match_distribution_criteria = True
    return match_distribution_criteria

def match_neighbor_criteria(args, assigned_students):
    match_neighbor_criteria = True
    return match_neighbor_criteria

def draw_puzzle(args, assigned_students):
    return True

def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--width", type=int, required=True, help="width of puzzle")
    parser.add_argument("--height", type=int, required=True, help="height of puzzle")
    parser.add_argument("--students", type=str, required=True, help="list of students seperated by commas")
    parser.add_argument("--dist", type=int, required=True, help="side distribution +- error")
    parser.add_argument("--neighbor_count", type=int, required=True, help="number of repeat neighbors")
    parser.add_argument("--match_attempts", type=int, required=False, help="attempts to match a side to a student before going to next student.")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    solution = False
    while not solution:
        puzzle_pieces = build_puzzle(args)
        print(puzzle_pieces)
        shared_sides = build_shared_sides(args, puzzle_pieces)
        print(shared_sides)
        assigned_students = assign_pieces(args, puzzle_pieces)
        print(assigned_students)
        assigned_students = assign_sides(args, assigned_students, shared_sides)
        print(assigned_students)
        if (match_distribution_criteria(args, assigned_students) and match_neighbor_criteria(args, assigned_students)):
            solution = True
    draw_puzzle(args, assigned_students)
