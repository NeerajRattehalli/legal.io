import csv
import ast

class CompanyType:
    def __init__(self, links, occurences):
        self.links = links
        self.occurences = occurences




company_types = {}



with open("top_tags.tsv", "r") as in_file:
    csv_reader = csv.reader(in_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in csv_reader:
       arr = ast.literal_eval(row[1])
       company_url = row[0]
       counts = []
       for i in range(0, len(arr)):
            sub_arr = arr[i]
            count = sub_arr[1]
            counts.append(count)
            if(len(counts) > 0 and count < counts[0]):
                for j in range (0,i):
                    company_type = arr[j][0]
                    if company_type in company_types:
                        company_types[company_type].occuerences = company_types[company_type].occurences + 1
                    else:
                        company_types[company_type].occurences = 1
                with open("final.tsv", "r") as final:
                    final_reader = csv.reader(final, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    for row in final_reader:
                        if row[]

