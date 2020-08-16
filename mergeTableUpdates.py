companyMainDict = {}

# Read Input Data
with open('final/finalV6-mergedKristenData/final.tsv','r') as in_file:
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

with open("Updates.tsv", "r") as in_file:
    for line in in_file:
        status, compName = line.split("\t")
        compName = compName[:-1]
        if status == "acquired":
            companyMainDict[compName]["status"] = "acquired"
        elif "dead" in status.lower():
            companyMainDict[compName]["status"] = "inactive"
        elif "remove" in status.lower():
            del companyMainDict[compName]
        elif "not legal" in status.lower():
            del companyMainDict[compName]


# Update files

with open('final/finalV7-MergedTableUpdates/8-14-20-final.csv', 'w') as out_file:
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

with open('final/finalV7-MergedTableUpdates/final.tsv', 'w') as out_file:
    out_file.write("name\t"+"\t".join(list(companyMainDict['Correa Porto'].keys()))+"\n")
    for compName in companyMainDict:
        line = compName
        for description in companyMainDict[compName]:
            line += "\t" + companyMainDict[compName][description]
            if companyMainDict[compName][description] == "":
                line += "n/a"
        if "\n" in line:
            line = line[:-1]
        line += "\n"
        out_file.write(line)

