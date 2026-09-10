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
python3 ./script.py \
    --var1 20

'''

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--var1", type=int, required=True, help="variable description")
    return parser.parse_args()

if __name__ = "__main__":
    args = parse_args()
    var1 = args.var1

