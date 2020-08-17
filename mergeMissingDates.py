companyMainDict = {}

# Read Input Data
with open('final/ManualFinalV2/8-14-20-final.tsv','r') as in_file:
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


def getBestDate(dates):
    maxDateCount = -2
    maxDate = 0
    cond = True

    for date in dates:
        if dates[date] > maxDateCount:
            prevCount = maxDateCount
            maxDate = date
            maxDateCount = dates[date]
            cond = (maxDateCount - prevCount) > 3
    
    if cond:
        return maxDate
    else:
        return ""

    
with open('company_founding_date.csv', 'r') as in_file:
    for line in in_file:
        try:
            if "\"" in line:
                company, dateDict = line.split(",\"")
                if "\"" in company:
                    company = company[1:-1]
                company = eval(company)[0]
                dateDict = eval(dateDict[:-2])
                bestDate = getBestDate(dateDict)
                companyMainDict[company]["date"] = bestDate
            else:
                company, dateDict = line.split(",")
                company = eval(company)[0]
                dateDict = eval(dateDict)
                bestDate = getBestDate(dateDict)
                companyMainDict[company]["date"] = bestDate
        except:

            continue



# Update files

with open('final/finalV8-AddedMissingDates/final.csv', 'w') as out_file:
    out_file.write("name,"+",".join(list(companyMainDict['Correa Porto'].keys()))+"\n")
    for compName in companyMainDict:
        line = ""
        if "," in compName:
            line = "\"" + compName + "\""
        else:
            line = compName
        for description in companyMainDict[compName]:
            item = str(companyMainDict[compName][description])
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

with open('final/finalV8-AddedMissingDates/final.tsv', 'w') as out_file:
    out_file.write("name\t"+"\t".join(list(companyMainDict['Correa Porto'].keys()))+"\n")
    for compName in companyMainDict:
        line = compName
        for description in companyMainDict[compName]:
            line += "\t" + str(companyMainDict[compName][description])
            if companyMainDict[compName][description] == "":
                line += "n/a"
        if "\n" in line:
            line = line[:-1]
        line += "\n"
        out_file.write(line)

with open('davidManualDateCheck.tsv', 'w') as out_file:
    for compName in companyMainDict:
        if companyMainDict[compName]["date"] == "":
            returnDict = {}
            returnDict["date"] = ""
            returnDict["crunchbase_url"] = companyMainDict[compName]["crunchbase_url"]
            out_file.write(compName + "\t" + str(returnDict) + "\n")
