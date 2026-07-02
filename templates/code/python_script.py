'''
code: 
by: Michael Roberts
last updated: //

## code description:

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

