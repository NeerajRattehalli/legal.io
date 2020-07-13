import csv

with open("neel_no_mainUrl.tsv") as in_file:
    csv_reader = csv.reader(in_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in csv_reader:
        first_element = row[0]
        string_list = list(row[1])
        code = string_list[-3]
        if (code == "1"):
            string_list[-3] = "0"
        elif (code == "0"):
           string_list[-3] = "1"

        with open("neel_no_mainUrl_final.tsv", "a") as out_file:
            csv_writer = csv.writer(out_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([first_element, ''.join(string_list)])
