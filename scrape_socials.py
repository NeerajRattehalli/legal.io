from bs4 import BeautifulSoup
import requests
import csv
import sys
from urllib.parse import unquote

csv.field_size_limit(sys.maxsize)

everything = "everything"
twitter = "twitter"
facebook = "facebook"
crunchbase = "crunchbase"
angellist = "angellist"
main = ""
linkedin = "linkedin"

twitter_url = " twitter_url"
facebook_url = " facebook_url"
cruncbase_url = " crunchbase_url"
angellist_url = " angellist_url"
main_url = "main_url"
linkedin_url = " linkedin_url"

url_company_map = {twitter_url: twitter, facebook_url: facebook, cruncbase_url: crunchbase, angellist_url: angellist,
                   main_url: main, linkedin_url: linkedin}


def format_link(link):
    for i in range(0, len(link)):
        if link[i] == "&":
            return link[7:i]


def check_if_timeout(company_socials, to_scrape):
        if len(company_socials) == 0 and len(to_scrape) > 0:
            print("too many requests")
            print()
            sys.exit(0)


def scrape(company_name, to_scrape, line_num):
    # print(company_name)
    # print(to_scrape)
    # go through the array of socials
    company_socials = {}
    for i in to_scrape:
        search_url = "https://www.google.com/search?q=" + str(company_name) + "+" + url_company_map[i]
        webpage = requests.get(search_url)
        result_div = soup.find_all('div', attrs={'class': 'ZINbbc'})
        # find all a tags with an href
        for j in range(0, result_div.__len__()):
            a_tag = result_div[j].find('a', href=True)
            company_socials[i] = "0"
            try:
                href = a_tag['href']
                if (href.startswith("/url?q=")):
                    valid_link = unquote(format_link(href))
                    company_socials[i] = " " + str(valid_link)
                    break
            except TypeError:
                break
            # find first href tag that is a valid url
    check_if_timeout(company_socials, to_scrape)
    return company_socials


def write_to_csv(company_name, company_socials, line_number):
    with open("thingsToCheckManually.csv", "r") as to_read:
        reader = csv.reader(to_read, delimiter=",", quotechar='"')
        # for i in range(0, line_number - 1):
        #     next(reader)
        # row_to_write = next(reader)
        for row in reader:
            if company_name in row:
                row_to_write = row
                print(row_to_write)
                new_row = []
                for j in range(0, len(row_to_write)):
                    if "url" in row_to_write[j] or j == (len(row_to_write)-1):
                        for k in range(0, j):
                            new_row.append(row_to_write[k])
                        break
                new_row.append(company_socials)
        with open("companiesWithSocials.csv", "a") as to_write:
            csv_writer = csv.writer(to_write, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(new_row)
            print("wrote " + str(new_row))

    # with open(csv_name, "w") as file_to_write:
    #     file_writer = csv.writer(file_to_write, delimiter=",",  quotechar='"')
    #     for i in range(0, line_number-1):
    #         next(file_writer)
    #     row_to_write = next(file_writer)
    #     print(row_to_write)
    #     #write to line_number -1


with open("thingsToCheckManually.csv", "r") as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=",", quotechar='"')
    print(csv_reader)
    check = False
    for row in csv_reader:
        if row[0] == "Vertex Legal App" or check == True:
            print(row)
            company_name = row[0]
            check = True
            # print(company_name)
            to_scrape = []
            if twitter_url in row:
                to_scrape.append(twitter_url)
            if facebook_url in row:
                to_scrape.append(facebook_url)
            if cruncbase_url in row:
                to_scrape.append(cruncbase_url)
            if angellist_url in row:
                to_scrape.append(angellist_url)
            if (main_url) in row:
                to_scrape.append(main_url)
            if (linkedin_url) in row:
                to_scrape.append(linkedin_url)
            company_socials = scrape(company_name, to_scrape, csv_reader.line_num)
            write_to_csv(company_name, company_socials, csv_reader.line_num)
