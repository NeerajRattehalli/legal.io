from pipeline_copy import Company
import csv

with open("diversity_data_blanks.tsv", "r") as in_file:
    csv_reader = csv.reader(in_file, delimiter="\t", quotechar="'", quoting=csv.QUOTE_MINIMAL)
    for row in csv_reader:
        company_name = row[0]
        url = row[1]
        print(url)
        tags = Company.find_tags(url)
        row_dict = {"main_url":row[1], "twitter_url":row[2], "angellist_url":row[3], "crunchbase_url":row[4], "linkedin_url":row[5], "facebook_url":row[6]}
        with open("diversity_data_blanks_final.tsv", "a") as out_file:
            csv_writer = csv.writer(out_file, delimiter="\t", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            row = [company_name, row_dict, tags]
            csv_writer.writerow(row)
            print("wrote row + " + str(row))
