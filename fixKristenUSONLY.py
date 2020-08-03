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

importantIdentifiers = []
finalCompDict = {}


with open('USONLY/Data 7_20_20 - Diversity Working Copy - US Only Order Preserved.tsv') as in_file:
    start = False
    for line in in_file:
        if not start:
            importantIdentifiers = line.split("\t")
            importantIdentifiers[-1] = importantIdentifiers[-1][:-1]
            start = True
        else:
            Status, name, date, hq, USbased, category, audience, model, description, main_url, twitter_url, angellist_url, crunchbase_url, linkedin_url, facebook_url, tags, status = line.split("\t")
            compDictItem = companyMainDict[name] 

            date = companyMainDict[name]["date"] if (date=="n/a") else date
            hq = companyMainDict[name]["hq"] if (hq=="n/a") else hq
            category = companyMainDict[name]["category"] if (category=="n/a") else category
            audience = companyMainDict[name]["audience"] if (audience=="n/a") else audience
            model = companyMainDict[name]["model"] if (model=="n/a") else model
            description = companyMainDict[name]["description"] if (description=="n/a") else description
            main_url = companyMainDict[name]["main_url"] if (main_url=="n/a") else main_url
            linkedin_url = companyMainDict[name]["linkedin_url"] if (date=="n/a") else linkedin_url
            facebook_url = companyMainDict[name]["facebook_url"] if (date=="n/a") else facebook_url
            tags = companyMainDict[name]["tags"] if (tags=="n/a") else tags
            status = companyMainDict[name]["status"] if (status=="n/a") else status

            finalCompDict[name] = { "Status": Status,
                                    "name": name,
                                    "date": date, 
                                    "hq": hq, 
                                    "US based?": USbased,
                                    "category": category, 
                                    "audience": audience, 
                                    "model": model, 
                                    "description": description, 
                                    "main_url": main_url, 
                                    "twitter_url": twitter_url, 
                                    "angellist_url": angellist_url, 
                                    "crunchbase_url": cb_url, 
                                    "linkedin_url": linkedin_url,
                                    "facebook_url": facebook_url,
                                    "tags": tags,
                                    "status": status}

# Writing Final Files
with open('USONLYFINAL/finalV1/USOnly.csv', 'w') as out_file:
    out_file.write(",".join(list(finalCompDict['AfterIGo'].keys()))+"\n")
    for compName in finalCompDict:
        line = ""
        for description in finalCompDict[compName]:
            item = finalCompDict[compName][description]
            if "\n" in item:
                item = item[:-1]
            if "," in item:
                line += "\"" + item + "\","
            else:
                line += item + "," 
            if item == "":
                line += "n/a"
        line += "\n"
        out_file.write(line)

with open('USONLYFINAL/finalV1/USOnly.tsv', 'w') as out_file:
    out_file.write("\t".join(list(finalCompDict['AfterIGo'].keys()))+"\n")
    for compName in finalCompDict:
        line = ""
        for description in finalCompDict[compName]:
            line += finalCompDict[compName][description].replace("\n", "") + "\t" 
            if finalCompDict[compName][description] == "":
                line += "n/a"

        line += "\n"

        out_file.write(line)