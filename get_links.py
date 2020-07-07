import csv

with open("final/final.csv", "r") as in_file:
    csv_reader = csv.reader(in_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in csv_reader:
        main_url = row[7]
        print(main_url)