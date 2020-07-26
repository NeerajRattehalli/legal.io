#Authors: Neel Kandlikar and Neeraj Rattehalli

import csv, ast, collections


class ResearchPipeline:
    abbreviations = ['AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FM', 'FL', 'GA', 'GU', 'HI', 'ID',
                     'IL',
                     'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MH', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV',
                     'NH',
                     'NJ', 'NM', 'NY', 'NC', 'ND', 'MP', 'OH', 'OK', 'OR', 'PW', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN',
                     'TX',
                     'UT', 'VT', 'VI', 'VA', 'WA', 'WV', 'WI', 'WY']
    states = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut",
              "District of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho",
              "Illinois",
              "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan",
              "Minnesota",
              "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire",
              "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
              "Puerto Rico",
              "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia",
              "Virgin Islands",
              "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]
    indian_states = ["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat",
                     "Haryana",
                     "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh",
                     "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan",
                     "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttarakhand", "Uttar Pradesh", "West Bengal",
                     "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli", "Daman and Diu",
                     "Delhi",
                     "Lakshadweep", "Puducherry"]

    """determines the average success rating (measured by social media presence) of companies by company category/sector
       :param path_to_formatted_csv: the path to the csv with all of the compiled data and the headers 
       "name,date,hq,category,audience,model,description,main_url,twitter_url,angellist_url,crunchbase_url,linkedin_url,
       facebook_url,tags,status" all in order
       
       :returns an array of CompanyType objects, each containing the name of the CompanyType, the total numbber of links for the
                company type and the determined success rating for the company type
       """

    @staticmethod
    def company_type_success_correlation(path_to_formatted_csv):
        # initialize empty array of company types
        company_types = []

        # define inner class "CompanyType" with the name of the company type, the total number of links for the company type, and the total number of times that company type occured
        class CompanyType:
            def __init__(self, type, links, occurences):
                self.type = type
                self.links = links
                self.occurences = occurences
                self.success_rating = -1

            def __str__(self):
                return "name: " + str(self.type) + " occurences: " + str(self.occurences) + " links " + str(
                    self.links) + " success rating " + str(self.success_rating)

            # update the success rating, determined by the number of social media links
            def update_success_rating(self):
                self.success_rating = self.links / self.occurences

        with open(path_to_formatted_csv, "r") as in_file:
            csv_reader = csv.reader(in_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in csv_reader:
                # skip missing data
                if (row == 0):
                    continue
                if row[3] == "n/a" or "--" in row[3]:
                    continue
                # format row
                sep = '-'
                fixed_row = row[3].split(sep, 1)[0]
                fixed_row = fixed_row.strip()
                if fixed_row == "E":
                    fixed_row = "E-Discovery"
                # obtain links
                links = [row[8], row[9], row[10], row[11], row[12]]
                valid_links = len(links)
                # count how many valid links per company
                for link in links:
                    if link == "n/a":
                        valid_links = valid_links - 1
                # if the array is empty initialize a new CompanyType object and append it to the array
                if (len(company_types) == 0):
                    company_types.append(CompanyType(fixed_row, 1, valid_links))
                    # update success rating
                    company_types[0].update_success_rating()
                # iterate through and update the company types array as more links and occurences of a particular company type are found
                for i in range(0, len(company_types)):
                    company = company_types[i]
                    if (company.type == fixed_row):
                        company.occurences = company.occurences + 1
                        company.links = company.links + valid_links
                        company.update_success_rating()
                        break
                    if (i == len(company_types) - 1):
                        company_types.append(CompanyType(fixed_row, valid_links, 1))
                        company.update_success_rating()

        return company_types

    """finds the most commmon company types according to pre-determined tags
       :param path_to_formatted_csv: the path to the csv with all of the compiled data and the headers 
       "name,date,hq,category,audience,model,description,main_url,twitter_url,angellist_url,crunchbase_url,linkedin_url,
       facebook_url,tags,status" all in order
       
       :returns: a dictionary with the various company types as the keys and the number of occurrences as values
       """

    @staticmethod
    def most_common_company_types(path_to_final_csv):

        # initialize compDict
        compDict = {}
        with open(path_to_final_csv) as in_file:
            for line in in_file:
                # store the tags for each company in a dictionary
                company = line.split(",")[0]
                tagDict = eval(line.split("\"")[13])
                compDict[company] = tagDict

        def getMax(tags):
            # get tag with the maximum occurrences
            tagCopy = tags.copy()
            bestTag, maxVal = tagCopy.popitem()
            for tag in tagCopy:
                if tagCopy[tag] > maxVal:
                    maxVal = tagCopy[tag]
                    bestTag = tag
            return (bestTag, maxVal)

        def getTop3Tag(tags):
            # get top 3 tags with the maximum occurrences
            tagCopy = tags.copy()
            bestList = []
            for i in range(3):
                bestTag, val = getMax(tagCopy)
                bestList.append([bestTag, val])
                print(tagCopy)
                del tagCopy[bestTag]
                print("here", bestList)
            return bestList

        top3TagDict = {}
        for company in compDict:
            top3TagDict[company] = getTop3Tag(compDict[company])

        # populate dictionary
        for company in top3TagDict:
            tags = top3TagDict[company][:]
            for tagPair in top3TagDict[company]:
                # remove tags that do not occur at all
                if tagPair[1] == 0:
                    tags.remove(tagPair)
                top3TagDict[company] = tags

        with open("top_tags.tsv", "w") as out_file:
            for company in top3TagDict:
                out_file.write(company + "\t" + str(top3TagDict[company]) + "\n")

        company_types = {}

        # read from csv and return the dictionary of top tags
        with open("top_tags.tsv", "r") as in_file:
            csv_reader = csv.reader(in_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in csv_reader:
                arr = ast.literal_eval(row[1])
                counts = []
                for i in range(0, len(arr)):
                    sub_arr = arr[i]
                    count = sub_arr[1]
                    counts.append(count)
                    if (len(counts) > 0 and count < counts[0]):
                        for j in range(0, i):
                            company_type = arr[j][0]
                            if company_type in company_types:
                                company_types[company_type] = company_types[company_type] + 1
                            else:
                                company_types[company_type] = 1
        return company_types

    """finds the location distribution of companies
           :param path_to_formatted_csv: the path to the csv with all of the compiled data and the headers 
           "name,date,hq,category,audience,model,description,main_url,twitter_url,angellist_url,crunchbase_url,linkedin_url,
           facebook_url,tags,status" all in order
           
           :returns: an array with the number companies in each country
           """

    @staticmethod
    def success_location_correlation(path_to_formatted_csv):

        #initialize array of links
        country_links = []

        #create inner helper class that stores the name, occurrences and number of links for a particular country
        class Country:
            def __init__(self, name, occurrences, links):
                self.name = name
                self.occurences = occurrences
                self.links = links
                self.success_rating = links / occurrences

            def __str__(self):
                return "name: " + str(self.name) + " occurences: " + str(self.occurences) + " links " + str(
                    self.links) + " success rating " + str(self.success_rating)

            def update_success_rating(self):
                self.success_rating = self.links / self.occurences

        with open(path_to_formatted_csv, "r") as in_file:
            csv_reader = csv.reader(in_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in csv_reader:
                if row == 0:
                    continue
                location = row[2]

                #format the country name
                trimmed_location = ""
                rev_location = ''.join(reversed(location))
                if "," not in location:
                    trimmed_location = location.strip()
                    continue
                if (rev_location == "a/n"):
                    continue
                for i in range(0, len(rev_location)):
                    if (rev_location[i] == ","):
                        trimmed_location = ''.join(reversed(rev_location[0:i])).strip()
                        break
                trimmed_location = ''.join([i for i in trimmed_location if not i.isdigit()]).strip()
                trimmed_location = trimmed_location[0].upper() + trimmed_location[1:]
                trimmed_location = trimmed_location.replace(".", "")

                # check for variations in spelling bewteen location names
                if (trimmed_location == "United States"):
                    trimmed_location = "USA"
                elif trimmed_location in ResearchPipeline.abbreviations or trimmed_location in ResearchPipeline.states:
                    trimmed_location = "USA"
                elif trimmed_location in ResearchPipeline.indian_states:
                    trimmed_location = "India"
                elif (trimmed_location == "FR"):
                    trimmed_location = "France"
                elif (trimmed_location == "United Kingdom"):
                    trimmed_location = "UK"
                elif (trimmed_location == "Cundinamarca"):
                    trimmed_location = "Colombia"
                elif (trimmed_location == "S/n  Santiago de Compostela"):
                    trimmed_location = "Spain"
                elif (trimmed_location == "ON"):
                    trimmed_location = "Canada"
                elif (trimmed_location == "Ontario"):
                    trimmed_location = "Canada"
                elif (trimmed_location == "Ontario Canada"):
                    trimmed_location = "Canada"
                elif (trimmed_location == "Melbourne VIC"):
                    trimmed_location = "Australia"
                elif (trimmed_location == "Sydney"):
                    trimmed_location = "Australia"
                elif (trimmed_location == "CA and the world"):
                    trimmed_location = "USA"

                #store links for a particular company in an array
                links = [row[8], row[9], row[10], row[11], row[12]]

                #check if links are broken
                valid_links = len(links)
                for link in links:
                    if link == "n/a":
                        valid_links = valid_links - 1
                print(trimmed_location + " " + str(valid_links))
                #update aray with new data
                if (len(country_links) == 0):
                    country_links.append(Country(trimmed_location, 1, valid_links))
                    country_links[0].update_success_rating()
                for i in range(0, len(country_links)):
                    country = country_links[i]
                    if (country.name == trimmed_location):
                        country.occurences = country.occurences + 1
                        country.links = country.links + valid_links
                        country.update_success_rating()
                        break
                    if (i == len(country_links) - 1):
                        country_links.append(Country(trimmed_location, 1, valid_links))
                        country.update_success_rating()
                #return the data
                arr = []
                for country in country_links:
                    arr.append([country.name, country.occurences, country.links, country.success_rating])
                return arr

    """finds the number of companies founded per year and per country, essentially creating a timeline of when companies were founded 
               :param path_to_formatted_csv: the path to the csv with all of the compiled data and the headers 
               "name,date,hq,category,audience,model,description,main_url,twitter_url,angellist_url,crunchbase_url,linkedin_url,
               facebook_url,tags,status" all in order
               
               :param current_year: the current year

               :returns: an array with the number of companies founded each year and in each country
               """

    @staticmethod
    def companies_founded_by_year(path_to_formatted_csv, current_year):
        #initialize an empty dictionary
        year_data = {}
        with open(path_to_formatted_csv, "r") as in_file:
            csv_reader = csv.reader(in_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in csv_reader:
                if row == 0:
                    continue
                founding_year = row[1]
                location = row[2]
                #correct location name and check for errors in data
                trimmed_location = ""
                rev_location = ''.join(reversed(location))
                if (rev_location == "a/n" or founding_year == "n/a"):
                    continue
                if "," not in location:
                    trimmed_location = location.strip()
                    continue
                if not founding_year.isdigit() or int(founding_year) > current_year:
                    continue
                founding_year = int(founding_year)
                for i in range(0, len(rev_location)):
                    if (rev_location[i] == ","):
                        trimmed_location = ''.join(reversed(rev_location[0:i])).strip()
                        break
                trimmed_location = ''.join([i for i in trimmed_location if not i.isdigit()]).strip()
                trimmed_location = trimmed_location[0].upper() + trimmed_location[1:]
                trimmed_location = trimmed_location.replace(".", "")

                # check for variations in spelling between location names
                if (trimmed_location == "United States"):
                    trimmed_location = "USA"
                elif trimmed_location in ResearchPipeline.abbreviations or trimmed_location in ResearchPipeline.states:
                    trimmed_location = "USA"
                elif trimmed_location in ResearchPipeline.indian_states:
                    trimmed_location = "India"
                elif (trimmed_location == "FR"):
                    trimmed_location = "France"
                elif (trimmed_location == "United Kingdom"):
                    trimmed_location = "UK"
                elif (trimmed_location == "Cundinamarca"):
                    trimmed_location = "Colombia"
                elif (trimmed_location == "S/n  Santiago de Compostela"):
                    trimmed_location = "Spain"
                elif (trimmed_location == "ON"):
                    trimmed_location = "Canada"
                elif (trimmed_location == "Ontario"):
                    trimmed_location = "Canada"
                elif (trimmed_location == "Ontario Canada"):
                    trimmed_location = "Canada"
                elif (trimmed_location == "Melbourne VIC"):
                    trimmed_location = "Australia"
                elif (trimmed_location == "Sydney"):
                    trimmed_location = "Australia"

                #check to see if values are in dictionary, if so update values, else create new key with value 1
                if founding_year not in year_data:
                    year_data[founding_year] = {}
                    year_data[founding_year][trimmed_location] = 1
                    continue
                if trimmed_location not in year_data[founding_year]:
                    year_data[founding_year][trimmed_location] = 1
                    continue
                year_data[founding_year][trimmed_location] = year_data[founding_year][trimmed_location] + 1

            #convert to ordered dict to sort dictionary chronologically
            ordered_year_data = collections.OrderedDict(
                sorted(collections.OrderedDict(year_data).items(), key=lambda key_value: key_value[0]))

            #return the data
            arr = []
            for key in ordered_year_data:
                arr.append(([(str(key) + "\t" + str(ordered_year_data[key]))]))
            return arr
