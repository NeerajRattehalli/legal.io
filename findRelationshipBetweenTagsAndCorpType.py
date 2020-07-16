# Tags finding
#stanford tags and our
#find relationship between gunst and stanford tag
#creates relationship matrix between old categories and new categories
#if company type is missing call it
#tags to category
#check to see if these tags exist

tagList = []

with open("tags.txt", "r") as in_file:
    for line in in_file:
        newLine = line.replace("\n", "")
        tagList.append(newLine)

# Company Finding

compTypes = []
    
with open("stanford_tags.txt", "r") as in_file:
    for line in in_file:
        newLine = line.replace("\n", "")
        compTypes.append(newLine)

# Initialize relationship dict
compToTagsDict = {}

for comp in compTypes:
    compToTagsDict[comp] = {}

with open("./output_files/final.tsv") as in_file:
    count = 0
    for line in in_file:
        if count>0:
            parts = line.split("\t")
            companyType = parts[3]
            for comp in compTypes:
                if comp in companyType:
                    companyType = comp
            companyTags = parts[-1]

            if companyType not in compTypes:
                continue


            for tag in companyTags.split(", "):
                newTag = tag.replace("\n", "")
                if newTag not in tagList:
                    continue
                if newTag not in compToTagsDict[companyType]:
                    compToTagsDict[companyType][newTag] = 0
                compToTagsDict[companyType][newTag] += 1
            
        count += 1


# with open("think.tsv", "w") as out_file:
#     for key in compToTagsDict:
#         out_file.write(key + "\t" + str(compToTagsDict[key]) + "\n")

relationShipDict = {}
with open("thinkManual.tsv", "r") as in_file:
    for line in in_file:
        compType, compDict  = line.split("\t")
        compDict = eval(compDict)
        for tag in compDict:
            relationShipDict[tag] = compType


# for key in relationShipDict:
#     print(key, relationShipDict[key])

companyMainDict = {}

with open('./output_files/final.tsv','r') as in_file:
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


count = 0
newCompTypeList = []

for company in companyMainDict:
    category = companyMainDict[company]["category"]
    if "n/a" not in companyMainDict[company]["category"]:
        if "n/a" not in companyMainDict[company]["tags"]:
            allTags = companyMainDict[company]["tags"].split(", ")
            for tag in allTags:
                if tag in tagList:
                    predCategory = relationShipDict[tag]
                    category = predCategory
                    count += 1
                    newCompTypeList.append(company)
                    break


    companyMainDict[company]["category"] = category

for company in newCompTypeList:
    print(company, companyMainDict[company]["category"])

for company in companyMainDict:
    tags = companyMainDict[company]["tags"]
    tags = tags.replace("\n", "")
    companyMainDict[company]["tags"] = tags

# Update files

with open('final/final.csv', 'w') as out_file:
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

with open('final/final.tsv', 'w') as out_file:
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

def makeDict(company, compDict):
    returnDict = {}
    returnDict["category"] = ""

    if "n/a" not in compDict["description"]:
        returnDict["description"] = compDict["description"]
    if "n/a" not in compDict["tags"]:
        returnDict["tags"] = compDict["tags"]
    

    return returnDict

with open("davidWork/companiesToFindType.tsv", "w") as out_file:
    for company in companyMainDict:
        if "n/a" in companyMainDict[company]["category"]:
            smallDict = makeDict(company, companyMainDict[company])
            out_file.write(company + "\t" + str(smallDict) + "\n")
