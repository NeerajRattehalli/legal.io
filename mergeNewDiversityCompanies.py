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

with open('./diversity_data_blanks_final.tsv','r') as in_file:
    start = False

    for line in in_file:
        if start:
            print(line.split("\t"))
            name, compDict, tagDict = line.split("\t")
            compDict = eval(compDict)

            for item in compDict:
                companyMainDict[name][item] = compDict[item]
        
        start = True

print(len(companyMainDict))