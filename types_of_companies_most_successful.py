import csv
import ast



company_types = []


class CompanyType:
    def __init__(self, type, links, occurences):
        self.type = type
        self.links = links
        self.occurences = occurences
    def __str__(self):
        return "name: " + str(self.type) + " occurences: " + str(self.occurences) + " links " + str(
            self.links) + " success rating " + str(self.success_rating)
    def update_success_rating(self):
        self.success_rating = self.links / self.occurences



with open("final/8-14-20-final.csv", "r") as in_file:
    csv_reader = csv.reader(in_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in csv_reader:
        # arr = ast.literal_eval(row[1])
        if (row == 0):
            continue
        if row[3] == "n/a" or "--" in row[3]:
            continue
        sep = '-'
        fixed_row = row[3].split(sep, 1)[0]
        fixed_row = fixed_row.strip()
        if fixed_row == "E":
            fixed_row = "E-Discovery"
        links = [row[8], row[9], row[10], row[11], row[12]]
        valid_links = len(links)
        for link in links:
            if link == "n/a":
                valid_links = valid_links - 1
        print(valid_links)
        print(fixed_row)


        if (len(company_types) == 0):
            company_types.append(CompanyType(fixed_row, 1, valid_links))
            company_types[0].update_success_rating()
        for i in range(0, len(company_types)):
            company = company_types[i]
            if(company.type == fixed_row):
                company.occurences = company.occurences + 1
                company.links = company.links + valid_links
                company.update_success_rating()
                break
            if(i == len(company_types)-1):
                company_types.append(CompanyType(fixed_row, valid_links, 1))
                company.update_success_rating()

    with open("output_files/success_by_company_type.tsv", "a") as out_file:
        csv_writer = csv.writer(out_file, delimiter="\t", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for company in company_types:
            csv_writer.writerow([company.type, company.occurences, company.links, company.success_rating])




