import csv

seen = []
with open("8-14-20-final.csv", "r") as in_file:
    csv_reader = csv.reader(in_file,  delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in csv_reader:
        if row[0] in seen:
            print(row[0])
        seen.append(row[0])
print(seen)
