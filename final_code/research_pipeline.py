from bs4 import BeautifulSoup
import re, csv, ast, collections


class Pipeline:
    abbreviations = ['AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FM', 'FL', 'GA', 'GU', 'HI', 'ID',
                     'IL',
                     'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MH', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV',
                     'NH',
                     'NJ', 'NM', 'NY', 'NC', 'ND', 'MP', 'OH', 'OK', 'OR', 'PW', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN',
                     'TX',
                     'UT', 'VT', 'VI', 'VA', 'WA', 'WV', 'WI', 'WY'];
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

    @staticmethod
    def company_type_success_correlation(path_to_formatted_csv):
        company_types = []

        class CompanyType:
            def __init__(self, type, links, occurences):
                self.type = type
                self.links = links
                self.occurences = occurences
                self.success_rating = -1

            def __str__(self):
                return "name: " + str(self.type) + " occurences: " + str(self.occurences) + " links " + str(
                    self.links) + " success rating " + str(self.success_rating)

            def update_success_rating(self):
                self.success_rating = self.links / self.occurences

        with open(path_to_formatted_csv, "r") as in_file:
            csv_reader = csv.reader(in_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in csv_reader:
            if (row == 0):
                continue
            if row[3] == "n/a" or "--" in row[3]:
                continue
            sep = '-'
            fixed_row = row[3].split(sep, 1)[0]
            fixed_row = fixed_row.strip()
            if fixed_row == "E":
                fixed_row = "E-Discovery"
            links = [row[8], row[9], row[10], row[11], row[12]]
            valid_links = len(links)
            for link in links:
                if link == "n/a":
                    valid_links = valid_links - 1
            print(valid_links)
            print(fixed_row)

            if (len(company_types) == 0):
                company_types.append(CompanyType(fixed_row, 1, valid_links))
                company_types[0].update_success_rating()
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

        return [company.type, company.occurences, company.links, company.success_rating]

    @staticmethod
    def most_common_company_type(path_to_tags_file):
        company_types = {}

        with open(path_to_tags_file, "r") as in_file:
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
        arr = []
        while len(company_types) > 0:
            max_value = 0
            max_key = ""
            for key in company_types:
                if company_types[key] > max_value:
                    max_value = company_types[key]
                    max_key = key
                    arr.append((max_key, max_value))
                    del company_types[max_key]
        return arr

    @staticmethod
    def success_location_correlation(path_to_formatted_csv):
        country_links = []

        class Country:
            def __init__(self, name, occurences, links):
                self.name = name
                self.occurences = occurences
                self.links = links
                self.success_rating = links / occurences

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
                elif trimmed_location in Pipeline.abbreviations or trimmed_location in Pipeline.states:
                    trimmed_location = "USA"
                elif trimmed_location in Pipeline.indian_states:
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

                links = [row[8], row[9], row[10], row[11], row[12]]
                print(links)
                valid_links = len(links)
                for link in links:
                    if link == "n/a":
                        valid_links = valid_links - 1
                print(trimmed_location + " " + str(valid_links))
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

                arr = []
                for country in country_links:
                    arr.append([country.name, country.occurences, country.links, country.success_rating])
                return arr

    @staticmethod
    def companies_founded_by_year(path_to_formatted_csv):
        year_data = {}
        with open(path_to_formatted_csv, "r") as in_file:
            csv_reader = csv.reader(in_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in csv_reader:
                if row == 0:
                    continue
                founding_year = row[1]
                location = row[2]
                trimmed_location = ""
                rev_location = ''.join(reversed(location))
                if (rev_location == "a/n" or founding_year == "n/a"):
                    continue
                if "," not in location:
                    trimmed_location = location.strip()
                    continue
                if not founding_year.isdigit() or int(founding_year) > 2020:
                    continue
                founding_year = int(founding_year)
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
                elif trimmed_location in Pipeline.abbreviations or trimmed_location in Pipeline.states:
                    trimmed_location = "USA"
                elif trimmed_location in Pipeline.indian_states:
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
                # if (founding_year in years_to_check):
                #     print(founding_year + " " + trimmed_location)

                if founding_year not in year_data:
                    year_data[founding_year] = {}
                    year_data[founding_year][trimmed_location] = 1
                    continue
                if trimmed_location not in year_data[founding_year]:
                    year_data[founding_year][trimmed_location] = 1
                    continue
                year_data[founding_year][trimmed_location] = year_data[founding_year][trimmed_location] + 1

            ordered_year_data = collections.OrderedDict(
                sorted(collections.OrderedDict(year_data).items(), key=lambda key_value: key_value[0]))

            arr = []
            for key in ordered_year_data:
                    arr.append(([(str(key) + "\t" + str(ordered_year_data[key]))]))
            return arr

