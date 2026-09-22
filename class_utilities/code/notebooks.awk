# ----------------------------------------------
# usage: awk -v n=1 -v d="MM/DD" -v s=student_name -f notebooks.awk data.txt
# ----------------------------------------------
# 
# variables:
# n=1 - shows comments on student
# d="MM/DD" - shows only data from the date
# s=joe cutter - shows only joe cutter's informtion
# 
# *** notebook check document format ***
# POINTS, <assignment_points>
# <acroynm>, <acronym detail>, <"marking_variable" if points off>
# NOTEBOOK_DATA_BELOW
# <date>
# <student name>, <notes> <-- all in one line, only shorthand in CAPS
# *** end notebook check document format *** 
#
# *** example document ***
# POINTS, 10
# TCU, table of contents needs updating, marking_variable
# MIS, missing, marking_variable
# NOTEBOOK_DATA_BELOW
# 04/01
# joe cutter, TCU. MIS notes on lectures
# *** end example document ***
#
# *** example output ***
# Notebook Check 04/01
# joe cutter - 8
# *** end example output ***
# ----------------------------------------------

BEGIN {
    FS = ","
    started = 0
    first_in_series = 1
    points = 9
}

$0 ~ /NOTEBOOK_DATA_BELOW/ {
    started = 1
    next
}

{
    if (started == 0) {
        if (points == 9 && $1 == "POINTS") {
            points = $2
        }
        if ($3 != "" && $3 ~ "marking_variable") {
            if (first_in_series == 1) {
                mistake_pattern = $1
                first_in_series = 0
            } else {
            mistake_pattern = mistake_pattern "|" $1 
            }
        }
    }
    if (started == 1) {
        if ($1 ~ /^[0-1][0-9]\/[0-3][0-9]/) {
            data_date = $1
        }
        else if ($1 !="") {
            show_data = 1

            if (d != "" && data_date !~ d){
                show_data = 0
            }

            if (s != "" && $1 !~ s){
                show_data = 0
            }

            if (show_data == 1) {
                mistake_count = gsub(mistake_pattern, "&", $2)
                print data_date " - " $1 " - " points - mistake_count 
                if (n == 1) { 
                    print $2 "\n"
                }
            }
        }
    }
}
