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


companyMainDict = {}

def check(array, string):
    for item in array:
        if item in string:
            return True
    return False

# consolidate all the merged data
with open('./output_files/final.tsv','r') as in_file:
    count = 0
    companies = []
    for line in in_file:
        name, date, hq, category, audience, model, description, homepage_url, twitter_url, angellist_url, cb_url, linkedin_url, facebook_url, tags = line.split("\t")
        tags = tags.replace("\n", "")
        if "n/a" not in category:
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
        
        elif "n/a" not in tags:
            tagItems = tags.split(", ")
            condition = True
            for tag in tagItems:
                if tag in tagList:
                    mainTag = tag
                    mainTag.replace("\n", "")
                    if mainTag in relationShipDict:
                        count += 1
                        companies.append(name)
                        condition = False
                        expectedType = relationShipDict[mainTag]
                        companyMainDict[name] = {"date": date, 
                                            "hq": hq, 
                                            "category": expectedType, 
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
                        continue
                else:
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
        else:
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
                    
        
        
        
for company in companies:
    print(company, companyMainDict[company]["category"])
