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

with open("output_files/new_research_questions/companies_by_status_by_category.csv", "w") as out_file:
    out_file.write("category, acquired, active, inactive\n")
    for category in status_dict_by_category:
        try:
            acquired =  str(status_dict_by_category[category]["acquired"])
        except:
            acquired = str(0)

        try:
            active =  str(status_dict_by_category[category]["active"])
        except:
            active = str(0)

        try:
            inactive =  str(status_dict_by_category[category]["inactive"])
        except:
            inactive = str(0)

        out_file.write(category + ", " + acquired + "," + active + "," + inactive + "\n")

