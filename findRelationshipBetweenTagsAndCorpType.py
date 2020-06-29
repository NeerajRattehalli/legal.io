# Tags finding

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


for key in relationShipDict:
    print(key, relationShipDict[key])

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


for company in companyMainDict:
    tags = companyMainDict[company]["tags"]
    tags = tags.replace("\n", "")
    companyMainDict[company]["tags"] = tags

