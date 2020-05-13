import csv

last_line = None

with open('odm/organizations.csv', 'r') as odm:
            odm_reader = csv.reader(odm, delimiter = ",", quotechar='"')
            for row in reversed(list(odm_reader)):
                last_line = ','.join(row)
                break

def write_to_output(file_name, to_write):
    with open(file_name, mode='a') as output_file:
        csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(to_write)
        print("Written to " + str(file_name) + " " + str(company_name))
        output_file.close()



with open('updatedDataCopy.tsv', 'r') as data:
    data_reader = csv.reader(data, delimiter="\t", quotechar='"')
    for row in data_reader:
        company_name = row[0]
        with open('odm/organizations.csv', 'r') as odm:
            odm_reader = csv.reader(odm)
            for row_odm in odm_reader:
                if row_odm[1] == company_name:
                    write_to_output("in_odm.csv", row_odm)
                if row_odm == last_line:
                    print("written to not")
                    write_to_output("not_in_odm.csv", row_odm)








