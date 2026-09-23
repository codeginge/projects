'''
code: puzzle_assignments.py 
by: Michael Roberts
last updated: 09/23/26

## code description:
+ build puzzle matrix
- add LRTB neighbors for each piece (left-right-top-bottom) 
- randomly assign puzzle pieces to students. pieces with the most neighbors first 
- add responsibility for sides to student list
- students should have the same number of sides to work on +-1 side
- students should not be neighbors to the same person more than twice 
- show visual using turtle graphics with piece and side assignments
- run simulations until conditions are met

## datasets
puzzle = ['A0,0-A1-0-B0','A1,A0-A2-0-B1','A2,A1-0-0-B2',
          'B0,0-B1-A0-C1','B1,B0-B2-A1-C1','B2,B1-0-A2-C2',
          'C0,0-C1-B0-0','C1,C0-C2-B1-0','C2,C1-0-B2-0']

shared_sides=[A0B0, A0A1, A1A2, A1B1, A2B2, 
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

import argparse, turtle

def build_puzzle(args):
    puzzle_pieces = []
    for i in range(args.width):
        for j in range (args.height):
            piece = f"{chr(i+65)}{j}"
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
    print(build_puzzle(args))

