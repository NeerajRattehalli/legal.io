import csv
import requests
from bs4 import BeautifulSoup
import socket





headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "DNT": "1",
                   "Connection": "close", "Upgrade-Insecure-Requests": "1"}


incorrect = []

with open("final/final.tsv", "r") as in_file:
    csv_reader = csv.reader(in_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    met = False
    for row in csv_reader:
        main_url = row[7]
        name = row[0]
        if not met and name != "RechtEasy.at":
            print(name)
            continue
        if name == "RechtEasy.at":
            met = True
            print("MET")
        response_code = 0
        # changed = False
        if main_url == "main_url" or main_url == "n/a":
            continue
        if main_url[0:4] != "http":
            main_url = "https://" + str(main_url)
            print(main_url)
        print(main_url)
        try:
            response = requests.head(main_url)
            response_code_first_digit = int(str(response.status_code)[0])
            if(response_code_first_digit >=4):
                with open("output_files/400_codes.csv", "a") as out_file:
                    csv_writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    csv_writer.writerow([name, main_url, response.status_code])
            elif (response_code_first_digit >= 3):
                with open("output_files/300_codes.csv", "a") as out_file:
                    csv_writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    csv_writer.writerow([name, main_url, response.status_code])
            elif (response_code_first_digit >= 2):
                with open("output_files/200_codes.csv", "a") as out_file:
                    csv_writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    csv_writer.writerow([name, main_url, response.status_code])
        except requests.exceptions.ConnectionError:
            print(main_url + " didnt work")
            incorrect.append((name, main_url))
            with open("output_files/400_codes.csv", "a") as out_file:
                csv_writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow([name, main_url, "Connection Error"])


    #     except requests.exceptions.SSLError:s
    #         incorrect.append((name, main_url, response_code))
    #         print("error")
    #         continue
    #     if str(response.status_code)[0] == "3":
    #         incorrect.append((name, main_url, response.status_code))
    #         continue
    #     #bad status code
    #     elif int(str(response.status_code)[0]) > 3:
    #         incorrect.append((name, main_url, response.status_code))
    # print(incorrect)




        #     parser = BeautifulSoup(html, "html.parser")
        # except requests.exceptions.SSLError:
        #     # main_url = main_url[:4] + main_url[5:]
            # try:
            #     html = requests.get(main_url, headers=headers).text
            #     parser = BeautifulSoup(html, "html.parser")
            # except Exception:
            #     print("broken url "  + str(main_url))
            #     broken.append((name, main_url))

