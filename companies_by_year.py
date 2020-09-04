import csv
import collections

companiesByYear = {}
years = []

with open("final/ManualFinalV5/final.tsv", "r") as in_file:
    condition = False
    for line in in_file:
        if condition:
            row = line.split("\t")
            if row == 0:
                continue
            year = row[1]
            if year not in companiesByYear:
                companiesByYear[year] = 0
            if year not in years:
                years.append(year)
            companiesByYear[year] += 1
        condition = True

years.sort()

with open("output_files/new_research_questions/companies_by_year.tsv", "w") as out_file:
    out_file.write("year\tcount\n")
    for year in years:
        if year != "" and year!= "n/a":
            out_file.write(year + "\t" + str(companiesByYear[year]) + "\n")