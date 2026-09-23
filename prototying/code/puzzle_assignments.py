'''
code: puzzle_assignments.py 
by: Michael Roberts
last updated: 09/23/26

## code description:
- build puzzle matrix
- assign students to puzzle peices
- find all shared sides of puzzle peices
- evenly distrubute shared sides of puzzles to students
- students should have the same number of sides to work on +-1 side
- students should not be neighbors to the same person more than twice 
- show visual using turtle graphics with peice and side assignments
- run simulations until conditions are met

Build python environment:
python3 -m venv myenv
source myenv/bin/activate
pip install ... 

## example script call:
python3 ./script.py \
    --var1 20

'''

import argparse, turtle

def build_puzzle(args):
    puzzle_pieces = []
    for j in range(args.width):
        for i in range (args.height):
            piece = f"{i},{j}"
            puzzle_pieces.append(piece)
    return puzzle_pieces

def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--width", type=int, required=True, help="width of puzzle")
    parser.add_argument("--height", type=int, required=True, help="height of puzzle")
    parser.add_argument("--students", type=str, required=True, help="list of students seperated by commas")
    parser.add_argument("--dist", type=int, required=True, help="side distribution +- error")
    parser.add_argument("--neighbor_count", type=int, required=True, help="number of repeat neighbors")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    build_puzzle(args)

