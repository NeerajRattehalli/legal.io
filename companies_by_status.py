import csv

with open("final/ManualFinalV4/final.tsv") as in_file:
    reader = csv.reader(in_file, delimiter = "\t", quotechar = '"', quoting = csv.QUOTE_MINIMAL)
    status_dict = {}
    for row in reader:
        try:
            status = row[14]
        except IndexError:
            continue
        if status == "n/a":
            continue
        if status not in status_dict:
            status_dict[status] = 1
        else:
            status_dict[status] += 1
    print(status_dict)

