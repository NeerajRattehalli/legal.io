import csv
from pprint import pprint
import collections

year_data = {}
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
years_to_check = ["1982", "1989", "1996", "1929", "1993", "1983", "1874", "1990", "`1980", "1952"]
with open("final.csv", "r") as in_file:
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

    ordered_year_data = collections.OrderedDict(sorted(collections.OrderedDict(year_data).items(), key=lambda key_value: key_value[0]))
    for key in ordered_year_data:
        with open("companies_by_year.csv", 'a') as out_file:
            writer = csv.writer(out_file,  delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([(str(key) + "," + str(ordered_year_data[key]))])

