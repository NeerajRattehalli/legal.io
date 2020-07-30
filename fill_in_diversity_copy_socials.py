import csv

from pipeline_copy import Company

with open('diversity_copy.tsv', "r") as in_file:
    csv_reader = csv.reader(in_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for row in csv_reader:
        status = row[0]
        if(len(status) <= 0):
            continue
        if status[0] != "O":
            continue
        company_name = row[1]
        to_scrape = ['main_url', " twitter_url", " angellist_url", " crunchbase_url", " linkedin_url", " facebook_url"]
        line_num = csv_reader.line_num
        socials = Company.scrape(company_name, to_scrape)
        with open("diversity_data_blanks.tsv", "a") as out_file:
            csv_writer = csv.writer(out_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([company_name, socials["main_url"],socials[" twitter_url"], socials[" angellist_url"], socials[" crunchbase_url"], socials[" linkedin_url"], socials[" facebook_url"]])


        #print(socials)
        # with open("diversity_copy_final.tsv", "a") as out_file:
        #     csv_writer =  csv.writer(out_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #     csv_reader_out_file = csv.reader(in_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #     for line in csv_reader:
        #         if line_num == csv_reader.line_num:
        #             csv_writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], socials["main_url"],socials[" twitter_url"], socials[" angellist_url"], socials[" crunchbase_url"], socials[" linkedin_url"], socials[" facebook_url"]])
        #
        #




