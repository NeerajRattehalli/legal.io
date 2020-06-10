# read from final_updated.tsv
compDict = {}

# general checking function 
def check(items):
    for key in items:
        if items[key] == "n/a" or items[key] == "0":
            items[key] = ""
    return items

# consolidate all the merged data
with open('merged.tsv','r') as in_file:
    for line in in_file:
        name, date, hq, category, audience, model, description, homepage_url, twitter_url, angellist_url, cb_url, linkedin_url, facebook_url, tags = line.split("\t")
        
        cbDBDetails = {"date": date, 
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
        
        cbDBDetails = check(cbDBDetails)
    
        compDict[name] = cbDBDetails

# merging david checked files
with open('DAVID_FINAL_CHECK.txt', 'r') as in_file:
    for line in in_file:
        name, queries = line.split("\t")

        queries = eval(queries)

        if name not in compDict.keys():
            cbDBDetails = {"date": "", 
                            "hq": "", 
                            "category": "", 
                            "audience": "", 
                            "model": "", 
                            "description": "", 
                            "main_url": "", 
                            "twitter_url": "", 
                            "angellist_url": "", 
                            "crunchbase_url": "", 
                            "linkedin_url": "",
                            "facebook_url": "",
                            "tags": ""}
            compDict[name] = cbDBDetails

        for query in queries:
            compDict[name][query] = queries[query]

        # General checking method
        # for query in queries:
        #     text = query
        #     if queries[query]:
        #         text = text + queries[query]
            
        #     print(text)

print(compDict)

    

            