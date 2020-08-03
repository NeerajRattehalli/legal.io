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
            date = companyMainDict[name]["date"]
            hq = companyMainDict[name]["hq"]
            category = companyMainDict[name]["category"]
            audience = companyMainDict[name]["audience"]
            model = companyMainDict[name]["model"]
            description = companyMainDict[name]["description"]
            main_url = companyMainDict[name]["main_url"]
            linkedin_url = companyMainDict[name]["linkedin_url"]
            facebook_url = companyMainDict[name]["facebook_url"]
            tags = companyMainDict[name]["tags"]
            status = companyMainDict[name]["status"]

            finalCompDict[name] = { "Status": Status,
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


print(len(finalCompDict))