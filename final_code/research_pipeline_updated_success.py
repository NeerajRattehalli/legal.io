# Authors: Neel Kandlikar and Neeraj Rattehalli

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
    def company_type_success_correlation(path_to_formatted_csv, delimiter):
        # initialize empty array of company types
        company_types = {}

        # define inner class "CompanyType" with the name of the company type, the total number of links for the company type, and the total number of times that company type occured
        class CompanyType:
            def __init__(self, type):
                self.type = type
                self.occurrences = 0
                self.success_rating = -1
                self.score_sum = 0

            def __str__(self):
                # return "name: " + str(self.type) + " occurences: " + str(self.occurrences) + " score " + str(
                #     self.score_sum) + " success rating " + str(self.success_rating)
                return (str(self.type) + "," +   str(self.occurrences) + ","  +  str(self.score_sum) + "," +  str(self.success_rating))

            @staticmethod
            def success(foundingYear, status):
                if status.lower() == "inactive":
                    return 0
                elif status.lower() == "active":
                    return 2020 - int(foundingYear[0:4])
                elif status.lower() == "acquired":
                    return (2020 - int(foundingYear[0:4])) * 0.75
                else:
                    return 0

            # update the success rating, determined by the number of social media links
            def update_success_rating(self):
                self.success_rating = self.score_sum / self.occurrences

        with open(path_to_formatted_csv, "r") as in_file:
            csv_reader = csv.reader(in_file, delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL)
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
                status = row[14].lower()
                founding_date = row[1]
                if status == "n/a" or founding_date == "n/a":
                    continue
                company_type = row[3].strip().lower()

                if company_type not in company_types:
                    company_types[company_type] = CompanyType(company_type)
                company_types[company_type].score_sum = company_types[company_type].score_sum + CompanyType.success(founding_date, status)
                company_types[company_type].occurrences = company_types[company_type].occurrences + 1
                company_types[company_type].update_success_rating()

            return company_types

                # count how many valid links per company



    """finds the most commmon company types according to pre-determined tags
       :param path_to_formatted_csv: the path to the csv with all of the compiled data and the headers 
       "name,date,hq,category,audience,model,description,main_url,twitter_url,angellist_url,crunchbase_url,linkedin_url,
       facebook_url,tags,status" all in order

       :returns: a dictionary with the various company types as the keys and the number of occurrences as values
       """

    @staticmethod
    def most_common_company_types(path_to_final_csv, delimiter):
        type_count_dict = {}
        with open(path_to_final_csv, "r") as in_file:
            csv_reader = csv.reader(in_file,  delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in csv_reader:
                    continue
                comp_type = row[3].strip().lower()
                if comp_type == "n/a":
                    continue
                if comp_type not in type_count_dict:
                    type_count_dict[comp_type] = 0
                type_count_dict[comp_type] = type_count_dict[comp_type] + 1
            return type_count_dict

    """finds the location distribution of companies
           :param path_to_formatted_csv: the path to the csv with all of the compiled data and the headers 
           "name,date,hq,category,audience,model,description,main_url,twitter_url,angellist_url,crunchbase_url,linkedin_url,
           facebook_url,tags,status" all in order

           :returns: an array with the number companies in each country
           """

    @staticmethod
    def success_location_correlation(path_to_formatted_csv, delimiter):

        countries = {}

        # create inner helper class that stores the name, occurrences and number of links for a particular country
        class Country:
            def __init__(self, name):
                self.name = name
                self.occurrences = 0
                self.score_sum = 0
                self.success_rating = 0

            def __str__(self):
                return  str(self.name) + "," + str(self.occurrences) + "," + str(
                    self.score_sum) + "," + str(self.success_rating)

            @staticmethod
            def success(foundingYear, status):
                if status.lower() == "inactive":
                    return 0
                elif status.lower() == "active":
                    return 2020 - int(foundingYear[0:4])
                elif status.lower() == "acquired":
                    return (2020 - int(foundingYear[0:4])) * 0.75
                else:
                    return 0

            def update_success_rating(self):
                self.success_rating = self.score_sum / self.occurrences

        with open(path_to_formatted_csv, "r") as in_file:
            csv_reader = csv.reader(in_file, delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in csv_reader:
                if row == 0:
                    continue
                location = row[2]
                status = row[14].lower()
                founding_date = row[1]
                if status == "n/a" or founding_date == "n/a":
                    continue

                # format the country name
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

                if trimmed_location not in countries:
                    countries[trimmed_location] =  Country(trimmed_location)
                countries[trimmed_location].occurrences =  countries[trimmed_location].occurrences + 1
                countries[trimmed_location].score_sum = countries[trimmed_location].score_sum + Country.success(founding_date, status)
                countries[trimmed_location].update_success_rating()

            print(countries)
            return countries




    """finds the number of companies founded per year and per country, essentially creating a timeline of when companies were founded 
               :param path_to_formatted_csv: the path to the csv with all of the compiled data and the headers 
               "name,date,hq,category,audience,model,description,main_url,twitter_url,angellist_url,crunchbase_url,linkedin_url,
               facebook_url,tags,status" all in order

               :param current_year: the current year

               :returns: an array with the number of companies founded each year and in each country
               """

    @staticmethod
    def companies_founded_by_year(path_to_formatted_csv, current_year, delimiter):
        # initialize an empty dictionary
        year_data = {}
        with open(path_to_formatted_csv, "r") as in_file:
            csv_reader = csv.reader(in_file, delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in csv_reader:
                if row == 0:
                    continue
                founding_year = row[1]
                location = row[2]
                # correct location name and check for errors in data
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

                # check to see if values are in dictionary, if so update values, else create new key with value 1
                if founding_year not in year_data:
                    year_data[founding_year] = {}
                    year_data[founding_year][trimmed_location] = 1
                    continue
                if trimmed_location not in year_data[founding_year]:
                    year_data[founding_year][trimmed_location] = 1
                    continue
                year_data[founding_year][trimmed_location] = year_data[founding_year][trimmed_location] + 1

            # convert to ordered dict to sort dictionary chronologically
            ordered_year_data = collections.OrderedDict(
                sorted(collections.OrderedDict(year_data).items(), key=lambda key_value: key_value[0]))

            # return the data
            arr = []
            for key in ordered_year_data:
                arr.append(([(str(key) + " " + str(ordered_year_data[key]))]))
            return arr


