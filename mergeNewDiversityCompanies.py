import random

companyMainDict = {}

# Read Input Data
with open('./final/finalWithMissingUrlsFilledV5/final.tsv','r') as in_file:
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
            print(name)
            if not isinstance(tagDict, int) and len(tagDict.keys())>3:
                topTags = " ".join(getTopTags(tagDict))

            for item in compDict:
                companyMainDict[name][item] = compDict[item]
            
            companyMainDict[name]["tags"] = topTags
        
        start = True

