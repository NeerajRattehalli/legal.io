companies = []

with open('merged.tsv','r') as in_file:
    for line in in_file:
        companies.append(line.split("\t")[0])

newCompanies = []
with open('final_updated.tsv','r') as in_file:
    for line in in_file:
        if line.split("\t")[0] not in newCompanies:
            newCompanies.append(line.split("\t")[0])
        else:
            print(line.split("\t")[0])

print(len(companies), len(newCompanies))