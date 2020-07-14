companyMainDict = {}

# Read Input Data
with open('./final/finalWithStatus/final.tsv','r') as in_file:
    for line in in_file:
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
        print(name)

for company in companyMainDict:
    category = companyMainDict[company]["category"].split(" -")[0]
    companyMainDict[company]["category"] = category