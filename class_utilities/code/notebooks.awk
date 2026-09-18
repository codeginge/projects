# ----------------------------------------------
# usage: awk -v n=1 -v d="MM/DD" -v p="person_name" -f notebooks.awk data.txt
# ----------------------------------------------

BEGIN {
    FS = ","
    started = 0
}

$0 ~ /NOTEBOOK_DATA_BELOW/ {
    started = 1
    next
}

{
    if (started == 1) {
        if ($1 ~ /^[0-1][0-9]\/[0-3][0-9]/) {
            print "notebook check " $1
            date = $1
        }
        else if ($1 !="") {
            mistake_count = gsub(/(UOP|TCU|TCF|OLF|missing|RLF|DLF)/, "&", $2)
            print $1 " - " 9 - mistake_count 
            if (n == 1) { 
                print $2 "\n"
            }
        }
    }
}
