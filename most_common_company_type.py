import csv
import ast

company_types = {}

with open("top_tags.tsv", "r") as in_file:
    csv_reader = csv.reader(in_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in csv_reader:
       arr = ast.literal_eval(row[1])

       counts = []
       for i in range(0, len(arr)):
            sub_arr = arr[i]
            count = sub_arr[1]
            counts.append(count)
            if(len(counts) > 0 and count < counts[0]):
                for j in range (0,i):
                    company_type = arr[j][0]
                    if company_type in company_types:
                        company_types[company_type] = company_types[company_type] + 1
                    else:
                        company_types[company_type] = 1
with open("most_common_company_types.tsv", "a") as out_file:
    csv_writer = csv.writer(out_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    while len(company_types) > 0:
        max_value = 0
        max_key = ""

        for key in company_types:
            if company_types[key] > max_value:
                max_value = company_types[key]
                max_key = key
        csv_writer.writerow([max_key, max_value])
        del company_types[max_key]







