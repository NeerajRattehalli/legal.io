import csv, requests, re
from bs4 import BeautifulSoup


with open("final/ManualFinalV2/8-14-20-final.csv", "r") as in_file:
    csv_reader = csv.reader(in_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in csv_reader:
        if row[1] == "n/a":
            search_url = "https://www.google.com/search?q=" + str(row[0].replace(' ', '')) + "+" "founding+date"
            webpage = requests.get(search_url).text
            arr = (re.findall('(?<![0-9])(?:(?:19[0-9]{2}|20[0-2][0-9]))(?![0-9])', webpage))
            print(arr)
            dictionary = {}
            for element in arr:
                if element != '1967' and element != '2020':
                    if element in dictionary:
                        dictionary[element] = dictionary[element] + 1
                    else:
                        dictionary[element] = 1
            with(open("company_founding_date.csv", 'a')) as out_file:
                csv_writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow([[row[0]], dictionary])
                print("wrote",[row[0]], dictionary)





