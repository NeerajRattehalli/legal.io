import csv
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

years_to_check = ["1982", "1989", "1996", "1929", "1993", "1983", "1874", "1990", "`1980", "1952"]

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

abbrev_us_state = dict(map(reversed, us_state_abbrev.items()))

def getUSLocation(location):
    for abbreviation in abbreviations:
        if abbreviation in location:
            return abbrev_us_state[abbreviation]
    for state in states:
        if state in location:
            return state
    return "USA"

def fix_loc(location):
    trimmed_location = ""
    rev_location = ''.join(reversed(location))
    if "," not in location:
        trimmed_location = location.strip()
        return ""
    if (rev_location == "a/n"):
        return ""
    for i in range(0, len(rev_location)):
        if (rev_location[i] == ","):
            trimmed_location = ''.join(reversed(rev_location[0:i])).strip()
            break
    trimmed_location = ''.join([i for i in trimmed_location if not i.isdigit()]).strip()
    trimmed_location = trimmed_location[0].upper() + trimmed_location[1:]
    trimmed_location = trimmed_location.replace(".", "")

    # check for variations in spelling bewteen location names
    if (trimmed_location == "United States"):
        trimmed_location = getUSLocation(location)
    elif trimmed_location in abbreviations or trimmed_location in states:
        trimmed_location = getUSLocation(location)
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
    elif (trimmed_location == "CA and the world"):
        trimmed_location = "USA"
    elif (trimmed_location == "BC"):
        trimmed_location = "Canada"
    elif (trimmed_location == "Western US"):
        trimmed_location = "USA"
    elif (trimmed_location == "Toronto ON  MB G"):
        trimmed_location = "Canada"
    elif (trimmed_location == "Fla"):
        trimmed_location = "Canada"
    elif (trimmed_location == "The Netherlands"):
        trimmed_location = "Netherlands"
    return trimmed_location


with open("final/ManualFinalV5/final.tsv") as in_file:
    reader = csv.reader(in_file, delimiter = "\t", quotechar = '"', quoting = csv.QUOTE_MINIMAL)
    category_by_country = {}
    for row in reader:
        country = fix_loc(row[2])
        category = row[3]
        if row == "n/a" or category == "n/a" or country =="":
            continue
        if country not in category_by_country:
            particular_year_categories = {}
            particular_year_categories[category] = 1
            category_by_country[country] = particular_year_categories
        elif category not in category_by_country[country]:
            category_by_country[country][category] = 1
        else:
            category_by_country[country][category] += 1

    for year in category_by_country:
        particular_dict = category_by_country[year]
        max_val = 0
        max_category = ""
        for key in particular_dict:
            if particular_dict[key] > max_val:
                max_val = particular_dict[key]
                max_category = key
        particular_dict = (str(max_category), str(max_val))
        category_by_country[year] = particular_dict
    ordered_by_year = collections.OrderedDict(sorted(collections.OrderedDict(category_by_country).items(), key=lambda key_value: key_value[0]))


with open("output_files/new_research_questions/most_prominent_category_by_country.csv", "a") as out_file:
    writer = csv.writer(out_file, delimiter =",", quotechar = '"', quoting = csv.QUOTE_MINIMAL)
    for key in ordered_by_year:
        writer.writerow([key, ordered_by_year[key][0], ordered_by_year[key][1]])
        if key == "BC":
            print([key, ordered_by_year[key][0], ordered_by_year[key][1]])





