import csv
status_dict_by_location = {}
import collections


abbreviations = ['AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FM', 'FL', 'GA', 'GU', 'HI', 'ID', 'IL',
                 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MH', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH',
                 'NJ', 'NM', 'NY', 'NC', 'ND', 'MP', 'OH', 'OK', 'OR', 'PW', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX',
                 'UT', 'VT', 'VI', 'VA', 'WA', 'WV', 'WI', 'WY']
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
    
    return trimmed_location

with open("final/ManualFinalV5/final.tsv") as in_file:
    reader = csv.reader(in_file, delimiter = "\t", quotechar = '"', quoting = csv.QUOTE_MINIMAL)
    for row in reader:
        try:
            if (row[2] == ""):
                print(row)
            location = fix_loc(row[2])
            status = row[14]
        except IndexError:
            continue
        if status == "n/a" or location == "":
            continue

        if location not in status_dict_by_location:
            status_dict_by_location[location] = {}
        if status not in status_dict_by_location[location]:
            status_dict_by_location[location][status] = 1
        else:
            status_dict_by_location[location][status] += 1


with open("output_files/new_research_questions/companies_by_status_by_location.tsv", "w") as out_file:
    out_file.write("location\tacquired\tactive\tinactive\n")
    for category in status_dict_by_location:
        try:
            acquired =  str(status_dict_by_location[category]["acquired"])
        except:
            acquired = str(0)

        try:
            active =  str(status_dict_by_location[category]["active"])
        except:
            active = str(0)

        try:
            inactive =  str(status_dict_by_location[category]["inactive"])
        except:
            inactive = str(0)


        out_file.write(category + "\t" + acquired + "\t" + active + "\t" + inactive + "\n")

