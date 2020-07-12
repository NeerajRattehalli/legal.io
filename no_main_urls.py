import csv

with open("final/final.tsv") as in_file:
    csv_reader = csv.reader(in_file,  delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for row in csv_reader:
        if row[7] == "n/a":
            print(row[7] + row[0])
            with open("TXTFiles/neel/neel_no_mainUrl.csv", "a") as out_file:
                csv_writer = csv.writer(out_file,  delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow([row[0], "{'status': ''}"])

