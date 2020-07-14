companyMainDict = {}

# Read Input Data
with open('./final/finalWithCompType/final2.tsv','r') as in_file:
    for line in in_file:
        name, date, hq, category, audience, model, description, homepage_url, twitter_url, angellist_url, cb_url, linkedin_url, facebook_url, tags = line.split("\t")
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
                                    "tags": tags}

# Status Dict
statusDict = {
    "0": "active",
    "1": "inactive",
    "2": "acquired",
}

# CSV Merge
def mergeFileCSV(inputPath):
    with open(inputPath, "r") as in_file:
        for line in in_file:
            commaSplitLine = line.split(", ")
            compStatusDict = commaSplitLine[-1]
            compUrl = commaSplitLine[-2]
            compName = ", ".join(commaSplitLine[0:-2])
            compStatusDict = eval(compStatusDict)
            status = compStatusDict["status"]
            if (status == "3"):
                del companyMainDict[compName]
            else:
                status = statusDict[status]
                companyMainDict[compName]["status"] = status
                companyMainDict[compName]["main_url"] = compUrl

# Neel Merge
def mergeFileTSVNeel(inputPath):
    with open(inputPath, "r") as in_file:
        for line in in_file:
            tabSplitLine = line.split("\t")
            compStatusDict = tabSplitLine[1]
            compName = tabSplitLine[0]
            compStatusDict = eval(compStatusDict)
            status = statusDict[compStatusDict["status"]]
            companyMainDict[compName]["status"] = status

# David Merge
def mergeFileTSVDavid(inputPath):
    with open(inputPath, "r") as in_file:
        for line in in_file:
            tabSplitLine = line.split("\t")
            compStatusDict = tabSplitLine[-2]
            compUrl = tabSplitLine[-3]
            compName = ",".join(tabSplitLine[0:-3])
            compStatusDict = eval(compStatusDict)
            status = compStatusDict["status"]
            if (status == "3"):
                del companyMainDict[compName]
            else:
                status = statusDict[status]
                companyMainDict[compName]["status"] = status
                companyMainDict[compName]["main_url"] = compUrl

# Merging Files
mergeFileCSV("TXTFiles/neeraj/neerajFinal.csv")
mergeFileTSVNeel("TXTFiles/neel/neel_no_mainUrl_final.tsv")
mergeFileTSVDavid("TXTFiles/david/david200.csv")
mergeFileCSV("TXTFiles/david/david300.csv")

# Writing Final Files
with open('final/finalWithStatus/final.csv', 'w') as out_file:
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

with open('final/finalWithStatus/final.tsv', 'w') as out_file:
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