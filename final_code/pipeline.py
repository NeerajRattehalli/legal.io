# create company object
# validate all the info - validate links (main) - validate links -> verify links function -> static
# look at all links -> if not there scrape -> static
# find the tags -> find whatever tags there are on the main url -> static
# correlate tags to stanford -> matrix -> static

# to_string -> return line to string
# Put quotes if csv
from bs4 import BeautifulSoup
from urllib.parse import unquote
import csv, requests, re, sys

class Company:
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

    url_company_map = {twitter_url: twitter, facebook_url: facebook, cruncbase_url: crunchbase,
                       angellist_url: angellist,
                       main_url: main, linkedin_url: linkedin}


    """verifies company main urls and company social media links
    :param urlString: the type of url being verified (main, twitter, facebook, angellist etc.)
    :param compName: company name
    :param: url
    :returns: true if the url is correct, false if it is incorrect
    """
    @staticmethod
    def verify_url(self, urlString, compName, url):
        # checks if the required string is in the url link itself
        if urlString == "main":
            if (len(url.split("/")) >= 3):
                url = url.split("/")[2]
        elif urlString not in url:
            return False
        # lowercase url
        url = url.lower()
        # Case 1: Company Name has no spaces
        if " " not in compName:
            if "." in compName:
                # Splits companies names
                compNameWord = compName.split(".")
                # prelim parsing
                for word in compNameWord:
                    # lowers each element
                    lowerWord = word.lower()
                    # checks that it's not a useless word
                    if "inc" in lowerWord or "llc" in lowerWord or "p.c." in lowerWord:
                        continue
                    else:
                        # checks that each word is part of url
                        if lowerWord not in url:
                            return False
                # all conditions work for len > 1
                return True
            # splits at uppercase letters
            splitName = re.findall('[A-Z][^A-Z]*', compName)
            # edge cases that need direct checking
            if len(splitName) == 1:
                compName = compName.lower()
                return compName in url
            if len(splitName) == len(compName):
                return False
            else:
                # index system that checks for increasing pattern in text
                prevIndex = -1
                # verification for each part of the name
                for item in splitName:
                    # lowers so easy compare
                    modified = item.lower()
                    # direct check
                    if modified not in url:
                        return False
                    # does the increase index checking
                    index = url.find(modified)
                    if prevIndex > index:
                        return False
                    prevIndex = index
                    # passed all the tests for len = 1
            return True
        else:
            # Splits companies names
            compNameWord = compName.split(" ")
            # prelim parsing
            for word in compNameWord:
                # lowers each element
                lowerWord = word.lower()

                # checks that it's not a useless word
                if "inc" in lowerWord or "llc" in lowerWord or "p.c." in lowerWord or "ltd" in lowerWord:
                    continue
                else:
                    # checks that each word is part of url
                    if lowerWord not in url:
                        return False
            # all conditions work for len > 1
            return True

    """formats scraped links
      :param link: the link that was scraped
      """
    @staticmethod
    def format_link(self, link):
        for i in range(0, len(link)):
            if link[i] == "&":
                return link[7:i]

    """checks if the request timed out due to too many requests
          :param company_socials: the dictionary of company socials
          :param to_scrape: the array of socials to scrape
          """
    @staticmethod
    def check_if_timeout(self, company_socials, to_scrape):
        if len(company_socials) == 0 and len(to_scrape) > 0:
            print("too many requests")
            print()
            sys.exit(0)

    """scrapes the socials and main url of comapnies using the first google search result
              :param company_name: company name
              :param to_scrape: the array of socials to scrape
              """
    @staticmethod
    def scrape(self, company_name, to_scrape):
       #initialize blank dictionary of company socials
        company_socials = {}
        # iterate through to_scrape array
        for i in to_scrape:
            #query google with the search quaery as the company named followed by the name of social
            search_url = "https://www.google.com/search?q=" + str(company_name) + "+" + url_company_map[i]
            #get the html of the webpage using requests library
            webpage = requests.get(search_url).text
            #pass the html of the website to BeautifulSoup constructor
            soup = BeautifulSoup(webpage, "html.parser")
            #find a specific div within the html that contains the url to the first result
            result_div = soup.find_all('div', attrs={'class': 'ZINbbc'})
            # find all a tags with an href
            for j in range(0, result_div.__len__()):
                #find a tag within div
                a_tag = result_div[j].find('a', href=True)
                #set default value to 0, will be replaced later  if url is found
                company_socials[i] = "0"
                try:
                    #try to find an a tag within the href
                    href = a_tag['href']
                    #check to see if url is found
                    if (href.startswith("/url?q=")):
                        #format link and add to dictionary
                        valid_link = unquote(format_link(href))
                        company_socials[i] = " " + str(valid_link)
                        break
                except TypeError:
                    break
        #check if there was a timeout due to too many requests within a given period of time
        Company.check_if_timeout(company_socials, to_scrape)
        return company_socials



    """finds and records the number of occurences of a specific list of keywords within a webpage
              :param path_to_tags_file: path to the file containing the keywords to look for
              :param path_to_output_file: path to the file where the number of occurences should be recorded
              """
    @staticmethod
    def find_tags(self, path_to_tags_file, path_to_output_file):

        tags_file = open(path_to_tags_file, 'r')
        tags = tags_file.readlines()
        for i in range(0, len(tags)):
            #make all tags lowercase
            tags[i] = tags[i].strip().lower()

        with open('output_files/final.tsv', 'r') as in_file:
            file_reader = csv.reader(in_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in file_reader:
                main_url = row[7]
                #check if current main url is working within the final.tsv file
                if main_url == "main_url" or main_url == "n/a":
                    continue
                if main_url[0:4] != "http":
                    main_url = "https://" + str(main_url)
                print(main_url)
                #attempt to get the webpage using requests
                webpage = ""
                try:
                    webpage = requests.get(main_url)
                #skip the current url if there is an exception
                except Exception as e:
                    # broken url
                    print("url " + str(main_url) + " is broken")
                    print(webpage)
                    continue
                #move on to next url if the status code is not a success (200)
                if webpage.status_code != 200 or len(webpage.history) > 1:
                    print(str(main_url) + " bad status code")
                    continue
                #move on if there is a redirect
                if len(webpage.history) > 0 and "302" in webpage.history[0]:
                    print("redirect")
                    continue
                print("webpage url " + str(webpage.url))
                print("main url " + str(main_url))
                print(webpage.status_code)
                print(webpage.history)

                #pass webpage html to Beautiful Soup constructor
                soup = BeautifulSoup(webpage.text, 'html.parser')

                #move on if the webpage has no title
                if soup is None or soup.title is None or soup.title.string is None:
                    continue
                #Check if webpage title has any signs of being a 404 or error landing page
                if soup.title is None or "404" in soup.title.string or "error" in soup.title.string or "Error" in soup.title.string or "Forbidden" in soup.title.string or "forbidden" in soup.title.string or "403" in soup.title.string:
                    # 404 page
                    print("url " + str(main_url) + " was bad title")
                    continue

                print(soup.title.string)
                #go through the webapage and keep a count of how often  a particulr
                occurrences = {}
                for tag in tags:
                    occurrences[tag] = 0
                for tag in tags:
                    occurrences[tag] = len((soup.find_all(string=re.compile(tag), recursive=True)))
                print(occurrences)
                with open(path_to_output_file, 'a') as out_file:
                    #write to output file
                    writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    row[0] = main_url
                    row[1] = str(occurrences)
                    writer.writerow(row)

    def __init__(self, row_as_string, delimiter):
        row = row_as_string.split(delimiter)
        self.name = row[0]
        self.date = row[1]
        self.hq = row[2]
        self.category = row[3]
        self.audience = row[4]
        self.model = row[5]
        self.description = row[6]
        self.main_url = row[7]
        self.twitter_url = row[8]
        self.angellist_url = row[9]
        self.crunchbase_url = row[10]
        self.linkedin_url = row[11]
        self.facebook_url = row[12]
        self.tags = row[13]
        self.status = row[14]
        socials = ["main", "twitter", "angellist", "crunchbase", "linkedin", "facebook"]
        to_scrape = []
        for i in range(0,7):
            if not Company.verify_url(row[i+7]):
                to_scrape.append(socials[i])
        Company.scrape(self.name, to_scrape)


