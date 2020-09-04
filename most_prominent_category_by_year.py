import csv
import collections

companiesByCategoryByYear = {}
years = []
categories = []

with open("final/ManualFinalV5/final.tsv", "r") as in_file:
    condition = False
    for line in in_file:
        if condition:
            row = line.split("\t")
            if row == 0:
                continue
            year = row[1]
            category = row[3]
            if category == "n/a":
                continue

            if category not in categories:
                categories.append(category)
            if year not in years:
                years.append(year)
            if year not in companiesByCategoryByYear:
                companiesByCategoryByYear[year] = {}
            if category not in companiesByCategoryByYear[year]:
                companiesByCategoryByYear[year][category] = 0
            companiesByCategoryByYear[year][category] += 1
        condition = True

years.sort()

for year in companiesByCategoryByYear:
    for category in categories:
        if category not in companiesByCategoryByYear[year]:
            companiesByCategoryByYear[year][category] = 0

with open("output_files/new_research_questions/companies_by_category_by_year.tsv", "w") as out_file:
    out_file.write("year\t" + ("\t").join(categories) + "\n")
    for year in years:
        if year != "" and year!= "n/a":
            line = str(year)
            amounts = []
            for category in categories:
                amount = companiesByCategoryByYear[year][category]
                amounts.append(str(amount))

            out_file.write(year + "\t" + ("\t").join(amounts) + "\n")