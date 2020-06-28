import sys
import csv
import requests
from bs4 import BeautifulSoup
import re
import urllib3
import datetime

tags_file = open('stanford_tags.txt', 'r')

tags = tags_file.readlines()

for i in range(0, len(tags)):
    tags[i] = tags[i].strip().lower()

with open('output_files/final.tsv', 'r') as in_file:
    file_reader = csv.reader(in_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for row in file_reader:
        main_url = row[7]
        if main_url == "main_url" or main_url == "n/a":
            continue
        if main_url[0:4] != "http":
            main_url = "https://" + str(main_url)
        print(main_url)
        webpage = ""

        try:
            webpage = requests.get(main_url)
        except Exception as e:
            #broken url
            print("url " + str(main_url) + " is broken")
            print(webpage)
            continue

        print(webpage)


        if webpage.status_code != 200 or len(webpage.history) > 1:
            print(str(main_url) + " bad status code")
            continue
        if len(webpage.history) > 0 and "302" in webpage.history[0]:
            print("redirect")
            continue

        print("webpage url " + str(webpage.url))
        print("main url " + str(main_url))
        print(webpage.status_code)
        print(webpage.history)


        soup = BeautifulSoup(webpage.text, 'html.parser')

        if soup is None or soup.title is None or soup.title.string is None:
            continue

        if soup.title is None or "404" in soup.title.string or "error" in soup.title.string or "Error" in soup.title.string or "Forbidden" in soup.title.string or "forbidden" in soup.title.string or "403" in soup.title.string :
            #404 page
            print("url " + str(main_url) + " was bad title")
            continue

        print(soup.title.string)

        occurrences = {}
        for tag in tags:
            occurrences[tag] = 0
        for tag in tags:
            occurrences[tag] = len((soup.find_all(string= re.compile(tag), recursive=True)))

        print(occurrences)
        with open('output_files/found_stanford_tags.csv', 'a') as out_file:
            writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            row[0] = main_url
            row[1] = str(occurrences)
            writer.writerow(row)








