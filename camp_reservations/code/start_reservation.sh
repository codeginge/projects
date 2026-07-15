#!/bin/bash

source myenv/bin/activate

python3 ./assateague_2027.py \
  --sites 1138 \
  --start_date 07/16/2027 \
  --nights 14 \
  --time "09:42:00.000" \
  --attempts 4

