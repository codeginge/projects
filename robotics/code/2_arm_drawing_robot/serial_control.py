'''
code: serial_control.py
by: Michael Roberts
last updated: 10/06/26

## code description:
turn lines into drawing coordinates and send over serial to an arduino nano using the 
move_to_cords.ino code to draw lines defined.

Build python environment:
python3 -m venv myenv
source myenv/bin/activate
pip install pyserial 

## example script call:
python3 ./serial_control.py 

'''

import argparse, serial

def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--var1", type=int, required=True, help="variable description")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

