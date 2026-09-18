# ----------------------------------------------
# usage: awk -v notes=1 -f notebooks.awk notebooks_data.txt
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
        }
        else if ($1 !="") {
            mistake_count = gsub(/(UOP|TCU|TCF|OLF|missing|RLF|DLF)/, "&", $2)
            print $1 " - " 9 - mistake_count 
            if (notes == 1) {
                print "\n" $2 "\n"
            }
        }
    }
}
