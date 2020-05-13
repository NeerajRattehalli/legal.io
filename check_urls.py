import csv
import requests
import re
from bs4 import BeautifulSoup

base_url = "https://www.crunchbase.com/organization/"

def formatUrl(name):

    name = re.sub("[^A-Z, a-z,.,0-9]", "", name)
    name = name.lower()
    name = name.replace(".", "-")
    name = name.replace(" ", "-")
    if name.endswith("-"):
        name = name[:-1]
    if name.startswith("-"):
        name = name[1:]
    return base_url + name

def isValid(url):
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "DNT": "1",
               "Connection": "close", "Upgrade-Insecure-Requests": "1"}
    html = requests.get(url, headers=headers).text
    parser = BeautifulSoup(html , "html.parser")
    print(parser.title.string)
    if parser.title.string == 'Crunchbase':
        return False
    return True


def write_csv(file, company_name, url):
    print(file)
    with open(file, mode='a') as output_file:
        csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([company_name, url])
        print("Written: " + str(company_name))



with open('updatedDataCopy.tsv', 'r') as data:
    data_reader = csv.reader(data, delimiter="\t", quotechar='"')
    for row in data_reader:
        company_name = row[0]
        url = formatUrl(company_name)
        if(isValid(url)):
            write_csv("scrapable.csv", company_name, url)
        else:
            write_csv("not_scrapable.csv", company_name, url)










