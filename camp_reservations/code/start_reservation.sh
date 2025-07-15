#!/bin/bash

source camp_res/bin/activate

python3 ./camp_reservations.py \
  --sites F143,E119 \
  --start_date 2025-07-10 \
  --people 5 \
  --nights 14 \
  --site_type rv \
  --time "09:00:00.000" \
  --attempts 2
