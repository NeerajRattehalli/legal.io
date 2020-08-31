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


with open("output_files/new_research_questions/companies_by_status_by_location.tsv", "w") as out_file:
    out_file.write("category, acquired, active, inactive\n")
    for category in status_dict_by_location:
        try:
            acquired =  str(status_dict_by_location[category]["acquired"])
        except:
            acquired = str(0)

        try:
            active =  str(status_dict_by_location[category]["active"])
        except:
            active = str(0)

        try:
            inactive =  str(status_dict_by_location[category]["inactive"])
        except:
            inactive = str(0)

        out_file.write(category + "\t" + acquired + "\t" + active + "\t" + inactive + "\n")

