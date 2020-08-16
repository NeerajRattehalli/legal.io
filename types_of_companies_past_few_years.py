import csv
import collections

# year : [type, count]
# {2014: [type, count] }

year_data = {}


with open("final/8-14-20-final.csv", "r") as in_file:
    csv_reader = csv.reader(in_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in csv_reader:
        if (row == 0):
            continue
        if row[3] == "n/a" or "--" in row[3]:
            continue
        sep = '-'
        fixed_row = row[3].split(sep, 1)[0]
        fixed_row = fixed_row.strip()
        if fixed_row == "E":
            fixed_row = "E-Discovery"
        year_founded = row[1]

        if year_founded in year_data:
            if fixed_row in year_data[year_founded]:
                year_data[year_founded][fixed_row] =  year_data[year_founded][fixed_row] + 1
            else:
                year_data[year_founded][fixed_row] = 1
        if year_founded not in year_data:
            year_data[year_founded] = {}
            year_data[year_founded][fixed_row] = 1


    ordered_year_data = collections.OrderedDict(sorted(collections.OrderedDict(year_data).items(), key=lambda key_value: key_value[0]))
    with open("output_files/company_types_by_year.tsv", "w") as out_file:
        csv_writer = csv.writer(out_file, delimiter="\t", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for year in ordered_year_data:
            csv_writer.writerow([year, year_data[year]])




