#!/bin/bash

source camp_res/bin/activate

python3 ./camp_reservations.py \
  --sites G182 \
  --start_date 2026-09-14 \
  --people 5 \
  --nights 14 \
  --site_type rv \
  --time "09:00:00.000" \
  --attempts 4

