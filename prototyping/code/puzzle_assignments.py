'''
code: puzzle_assignments.py 
by: Michael Roberts
last updated: 09/23/26

## code description:
this code creates up to a 26x10 puzzle, assigns students to each puzzle piece, and assigns 
ownership of the sides to students. once ownership is established a visual is created.

TODO
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
python3 ./puzzle_assignments.py --width 7 --height 7 --students "jim,bob,joe,jeff,rich,christian,luke,brian" --dist 1 --neighbor_count 5 --match_attempts 300

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
        ###### HERE - why does this break on non square runs like 4x7 or 7x4?
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
            assigned_students[student_index] = f"{assigned_students[student_index]},{side_to_assign}"
            student_index += 1
            shared_sides.remove(side_to_assign)
        loop_iterations += 1
        if loop_iterations > match_attempts:
            student_index += 1
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
    match_neighbor_criteria = False
    neighbor_counts = []
    for s in assigned_students:
        distinct_neighbors, pieces_data, sides_data = [], [], []
        student = s.split(",")[0]
        for data in s.split(",")[1:]:
            if len(data) == 2:
                pieces_data.append(data)
            if len(data) == 4:
                sides_data.append(data)
        for side in sides_data:
            for piece in pieces_data:
                if piece in side:
                    side_to_check = side.replace(piece, "")
                    for possible_neighbor in assigned_students:
                        current_possible_neighbor = possible_neighbor.split(",")[0]
                        for neighbor_data in possible_neighbor.split(",")[1:]:
                            if (len(neighbor_data) == 4 and side_to_check in neighbor_data):
                                if current_possible_neighbor not in distinct_neighbors:
                                    distinct_neighbors.append(current_possible_neighbor) 
        neighbor_counts.append(len(distinct_neighbors))
        if args.debug: print(f"student: {student} | neighbors: {distinct_neighbors} | neighbor counts: {neighbor_counts}")
    if min(neighbor_counts) >= args.neighbor_count:
        match_neighbor_criteria = True
    return match_neighbor_criteria

def draw_puzzle(args, assigned_students, puzzle_pieces):
    if args.debug: print("start")
    # turtle pen setup
    piece_width, piece_height, font_size, line_weight, line_color, scale_border_up = 110, 110, 12, 1, "#000000", 1.05
    piece_info = piece_width, piece_height, font_size, line_weight, line_color, scale_border_up
    pen = turtle.Turtle()
    pen.up
    pen.speed(10)
    pen.pensize(line_weight)
    pen.pencolor(line_color)
    puzzle_length = len(puzzle_pieces)
    screen = turtle.Screen()
    screen.setup(width=piece_width*args.width*scale_border_up, height=piece_height*args.height*scale_border_up)
    screen.setworldcoordinates(0,-piece_height*args.height*scale_border_up,piece_width*args.width*scale_border_up,0)
    # draw boxes
    for index, p in enumerate(puzzle_pieces):
        owner, right_owner, bottom_owner, draw_top, draw_left = None, None, None, None, None
        if "A" in p: draw_top = True
        if "0" in p: draw_left = True
        for s in assigned_students:
            for data in s.split(","):
                if (len(data) == 2 and p in data):
                    owner = s.split(",")[0]
                if index + 1 < puzzle_length:
                    right_piece = f"{p}{puzzle_pieces[index + 1]}"
                    if (right_piece in data): 
                        right_owner = s.split(",")[0]
                if index + args.width < puzzle_length:
                    bottom_piece = f"{p}{puzzle_pieces[index + args.width]}"
                    if (bottom_piece in data): 
                        bottom_owner = s.split(",")[0]
        grid_coordinates = p
        draw_puzzle_piece(args, grid_coordinates, owner, right_owner, bottom_owner, draw_top, draw_left, pen, piece_info)
    turtle.done()
    return True

def draw_puzzle_piece(args, grid_coordinates, owner, right_owner, bottom_owner, draw_top, draw_left, pen, piece_info):
    piece_width, piece_height, font_size, line_weight, line_color, scale_border_up = piece_info
    if args.debug: print(f"piece: {grid_coordinates} | owner: {owner} | R: {right_owner} | B: {bottom_owner} | T: {draw_top} | L: {draw_left}")
    x = int(grid_coordinates[1])
    y = int(ord(grid_coordinates[0]) - 65)
    # draw box
    x_box, y_box = x * piece_width, -y * piece_height
    pen.goto(x_box,y_box)
    if draw_top:pen.down()
    pen.goto(x_box + piece_width, y_box)
    pen.up()
    pen.down()
    pen.goto(x_box + piece_width, y_box - piece_height)
    pen.goto(x_box, y_box - piece_height)
    pen.up()
    if draw_left:pen.down()
    pen.goto(x_box, y_box)
    pen.up()
    pen.goto(x_box + piece_width/2, y_box - piece_height/2)
    pen.down()
    pen.write(f"{grid_coordinates} \n{owner}")
    pen.up()
    if right_owner:
        pen.up()
        pen.goto(x_box + piece_width, y_box - piece_height/2)
        pen.down()
        pen.write(right_owner)
        pen.up()
    if bottom_owner:
        pen.up()
        pen.goto(x_box + piece_width/2, y_box - piece_height)
        pen.down()
        pen.write(bottom_owner)
        pen.up()
    return True

def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--width", type=int, required=True, help="width of puzzle")
    parser.add_argument("--height", type=int, required=True, help="height of puzzle")
    parser.add_argument("--students", type=str, required=True, help="list of students seperated by commas")
    parser.add_argument("--dist", type=int, required=True, help="side distribution +- error")
    parser.add_argument("--neighbor_count", type=int, required=True, help="number of repeat neighbors")
    parser.add_argument("--match_attempts", type=int, required=False, help="attempts to match a side to a student before going to next student.")
    parser.add_argument("--debug", type=bool, required=False, help="prints debug statements")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    solution = False
    while not solution:
        puzzle_pieces = build_puzzle(args)
        if args.debug: print(puzzle_pieces)
        shared_sides = build_shared_sides(args, puzzle_pieces)
        if args.debug: print(shared_sides)
        assigned_students = assign_pieces(args, puzzle_pieces)
        if args.debug: print(assigned_students)
        assigned_students = assign_sides(args, assigned_students, shared_sides)
        if args.debug: print(assigned_students)
        distribution_criteria = match_distribution_criteria(args, assigned_students)
        neighbor_criteria = match_neighbor_criteria(args, assigned_students)
        if (distribution_criteria and neighbor_criteria):
            solution = True
    print(assigned_students)
    draw_puzzle(args, assigned_students, build_puzzle(args))
