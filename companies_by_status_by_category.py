import csv
status_dict_by_category = {}

with open("final/ManualFinalV4/final.tsv") as in_file:
    reader = csv.reader(in_file, delimiter = "\t", quotechar = '"', quoting = csv.QUOTE_MINIMAL)
    for row in reader:
        try:
            category = row[3]
            status = row[14]
        except IndexError:
            continue
        if status == "n/a":
            continue
        if category not in status_dict_by_category:
            status_dict_by_category[category] = {}
        if status not in status_dict_by_category[category]:
            status_dict_by_category[category][status] = 1
        else:
            status_dict_by_category[category][status] += 1
    print(status_dict_by_category)
