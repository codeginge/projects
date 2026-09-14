'''
code: sort_students.py
by: Michael Roberts
last updated: 9/10/26

## code description: 
this code will sort students by name, block, and class depending on the settings you choose. 
First use case is for sorting by class then by lastname for student bin organization. 

inputs:
sort_order - which columns to sort by and their order ex:"0,2" will sort by last name and then by block
file - expected file type is a CSV file with the following header as the first line
    last, first, block, class
bin_info - this is the information you know about the bins 
    "<leters for cabinets>;<number of rows>;<number of columns>;[<bin_to_exclude>,<another_bin_to_exclude>,...]"
output - file name for csv file output ex:"test.csv"

## example script call:
python3 ./sort_student_bins.py \
    --sort_order "0,2" \
    --file "../docs/dm_rosters_405.csv" \
    --bin_info "JKL;5;5;['K-1-1','K-1-2','K-1-3','K-1-4','K-1-5']" \
    --output "../../../Desktop/student_bin_locations.csv"

'''

import argparse, csv

def create_bins(args):
    [letters, rows, columns, exclude_bins] = args.bin_info.split(';')
    bin_list = []
    for l in letters:
        for r in range(int(rows)):
            for c in range(int(columns)):
                bin_id = f"{l}-{r+1}-{c+1}"
                if bin_id not in exclude_bins:
                    bin_list.append(bin_id)
    return(bin_list)

def student_sort(args):
    with open(args.file, "r") as current_file:
        students = current_file.read().splitlines()
        headers = students[0]
        students = students[1:]
        for col in args.sort_order.split(','):
            students.sort(key = lambda x: x.split(',')[int(col)].strip())
        return(students) 

def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--sort_order", type=str, help="rows to sort and the priority order")
    parser.add_argument("--file", type=str, help="file with student roster")
    parser.add_argument("--bin_info", type=str, help="letters, rows, columns, bins to exclude ex: IJKL,5,5,['k-1-1','k-1-2','k-1-3','k-1-4','k-1-5']")
    parser.add_argument("--output", type=str, help="file to output to")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    students = student_sort(args)
    bins = create_bins(args)
    with open(args.output, "w", newline="", encoding="utf-8") as file_output:
        writer = csv.writer(file_output)
        header = ["FIRST","LAST","BLOCK","SUBJECT","BIN"]
        writer.writerow(header)
        for index, s in enumerate(students):
            [last, first, block, subject] = s.split(',')
            student_data = [last, first, block, subject, bins[index]]
            writer.writerow(student_data)
