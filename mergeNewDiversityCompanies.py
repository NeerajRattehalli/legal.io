import random

companyMainDict = {}

# Read Input Data
with open('./final/finalV5-WithMissingUrlsFilled/final.tsv','r') as in_file:
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

with open('./diversity_copy.tsv','r') as in_file:
    for line in in_file:
        Status, name, date, hq, USbased, category, audience, model, description, main_url, twitter_url, angellist_url, crunchbase_url, linkedin_url, facebook_url, tags, status = line.split("\t")
        if name not in companyMainDict:
            companyMainDict[name] = {}
        
        if "dead" in status.lower():
            status = "inactive"

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

def getTopTags(tagList):
    returnTags = []
    for i in range(3):
        maxTag = random.choice(list(tagList.keys()))
        maxVal = tagList[maxTag]

        for item in tagList:
            if tagList[item] > maxVal:
                maxVal = tagList[maxTag]
                maxTag = item
        
        if maxVal > 0:
            returnTags.append(maxTag)
            del tagList[maxTag]

    return returnTags
            

with open('./diversity_data_blanks_final.tsv','r') as in_file:
    start = False

    for line in in_file:
        if start:
            name, compDict, tagDict = line.split("\t")
            compDict = eval(compDict)
            tagDict = eval(tagDict[:-1])
            topTags = ""

            if not isinstance(tagDict, int) and len(tagDict.keys())>3:
                topTags = " ".join(getTopTags(tagDict))

            for item in compDict:
                companyMainDict[name][item] = compDict[item]
            
            companyMainDict[name]["tags"] = topTags
        
        start = True


# Writing Final Files
with open('final/finalV6-mergedKristenData/final.csv', 'w') as out_file:
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

with open('final/finalV6-mergedKristenData/final.tsv', 'w') as out_file:
    out_file.write("name\t"+"\t".join(list(companyMainDict['Correa Porto'].keys()))+"\n")
    for compName in companyMainDict:
        line = compName
        for description in companyMainDict[compName]:
            line += "\t" + companyMainDict[compName][description].replace("\n", "")
            if companyMainDict[compName][description] == "":
                line += "n/a"

        line += "\n"

        out_file.write(line)