import csv
status_dict_by_location = {}

with open("final/ManualFinalV4/final.tsv") as in_file:
    reader = csv.reader(in_file, delimiter = "\t", quotechar = '"', quoting = csv.QUOTE_MINIMAL)
    for row in reader:
        try:
            location = row[2]
            status = row[14]
        except IndexError:
            continue
        if status == "n/a":
            continue
        if location not in status_dict_by_location:
            status_dict_by_location[location] = {}
        if status not in status_dict_by_location[location]:
            status_dict_by_location[location][status] = 1
        else:
            status_dict_by_location[location][status] += 1
    print(status_dict_by_location)
