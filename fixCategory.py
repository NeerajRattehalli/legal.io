companyMainDict = {}

# Read Input Data
with open('./final/finalWithStatus/final.tsv','r') as in_file:
    start = False
    for line in in_file:
        if (start):
            name, date, hq, category, audience, model, description, homepage_url, twitter_url, angellist_url, cb_url, linkedin_url, facebook_url, tags, status = line.split("\t")
            companyMainDict[name] = {"date": date, 
                                    "hq": hq, 
                                    "category": category, 
                                    "audience": audience, 
                                    "model": model, 
                                    "description": description, 
                                    "main_url": homepage_url, 
                                    "twitter_url": twitter_url, 
                                    "angellist_url": angellist_url, 
                                    "crunchbase_url": cb_url, 
                                    "linkedin_url": linkedin_url,
                                    "facebook_url": facebook_url,
                                    "tags": tags,
                                    "status": status}
                                    
        start = True

for company in companyMainDict:
    category = companyMainDict[company]["category"].split(" -")[0]
    companyMainDict[company]["category"] = category


# Writing Final Files
with open('final/finalWithModifiedCategory/8-14-20-final.csv', 'w') as out_file:
    out_file.write("name,"+",".join(list(companyMainDict['Correa Porto'].keys()))+"\n")
    for compName in companyMainDict:
        line = ""
        if "," in compName:
            line = "\"" + compName + "\""
        else:
            line = compName
        for description in companyMainDict[compName]:
            item = companyMainDict[compName][description]
            if "\n" in item:
                item = item[:-1]
            if "," in item:
                line += ",\"" + item + "\""
            else:
                line += "," + item
            if item == "":
                line += "n/a"
        line += "\n"
        out_file.write(line)

with open('final/finalWithModifiedCategory/final.tsv', 'w') as out_file:
    out_file.write("name\t"+"\t".join(list(companyMainDict['Correa Porto'].keys()))+"\n")
    for compName in companyMainDict:
        line = compName
        for description in companyMainDict[compName]:
            line += "\t" + companyMainDict[compName][description].replace("\n", "")
            if companyMainDict[compName][description] == "":
                line += "n/a"

        line += "\n"

        out_file.write(line)