companyMainDict = {}

with open("./final/finalWithModifiedCategory/final.tsv", "r") as in_file:
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

missingCompanies = []

for company in companyMainDict:
    if "n/a" in companyMainDict[company]["main_url"]:
        missingCompanies.append(company)

with open("./missingCompanies/missing.tsv", "w") as out_file:
    for company in missingCompanies:
        out_file.write(company + "\t" + str({"main_url": ""}) + "\n")