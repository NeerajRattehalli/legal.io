import csv
from pprint import pprint
import collections

abbreviations = ['AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FM', 'FL', 'GA', 'GU', 'HI', 'ID', 'IL',
                 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MH', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH',
                 'NJ', 'NM', 'NY', 'NC', 'ND', 'MP', 'OH', 'OK', 'OR', 'PW', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX',
                 'UT', 'VT', 'VI', 'VA', 'WA', 'WV', 'WI', 'WY'];
states = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut",
          "District of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois",
          "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota",
          "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire",
          "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico",
          "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands",
          "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]
indian_states = ["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana",
                 "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh",
                 "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan",
                 "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttarakhand", "Uttar Pradesh", "West Bengal",
                 "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli", "Daman and Diu", "Delhi",
                 "Lakshadweep", "Puducherry"]

country_links = []

class Country:
  def __init__(self, name, occurences, links):
    self.name = name
    self.occurences = occurences
    self.links = links
    self.success_rating = links/occurences
  def __str__(self):
      return "name: " + str(self.name)  + " occurences: " + str(self.occurences) + " links " + str(self.links) + " success rating " + str(self.success_rating)
  def update_success_rating(self):
      self.success_rating = self.links / self.occurences



with open("final.csv", "r") as in_file:
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
        elif trimmed_location in abbreviations or trimmed_location in states:
            trimmed_location = "USA"
        elif trimmed_location in indian_states:
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
        elif(trimmed_location == "CA and the world"):
            trimmed_location = "USA"

        links = [row[8], row[9], row[10], row[11], row[12]]
        print(links)
        valid_links = len(links)
        for link in links:
            if link == "n/a":
                valid_links = valid_links - 1
        print( trimmed_location + " " + str(valid_links))
        if (len(country_links) == 0):
            country_links.append(Country(trimmed_location, 1, valid_links))
            country_links[0].update_success_rating()
        for i in range(0, len(country_links)):
            country = country_links[i]
            if(country.name == trimmed_location):
                country.occurences = country.occurences + 1
                country.links = country.links + valid_links
                country.update_success_rating()
                break
            if(i == len(country_links)-1):
                country_links.append(Country(trimmed_location, 1, valid_links))
                country.update_success_rating()

    with open("success_location_correlation.tsv", "a") as out_file:
        csv_writer = csv.writer(out_file, delimiter="\t", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for country in country_links:
            csv_writer.writerow([country.name, country.occurences, country.links, country.success_rating])
