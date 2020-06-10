# read from final_updated.tsv
compDict = {}

# general checking function 
def check(items):
    for key in items:
        if items[key] == "n/a" or items[key] == "0" or items[key] == "Unknown":
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

# merging neel checked files
with open('new_links.tsv', 'r') as in_file:
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

# generalized merge func
def merge(raw, additional):
    for data in additional:
        if "Unknown" in additional[data]:
            continue
        if raw[data] == "":
            if additional[data] == "Unknown -":
                print(additional[data]) 
            raw[data] = additional[data]
            
    return raw


itemsToDelete = []

with open('compData.tsv','r') as in_file:
    count = 0
    for line in in_file:
        count = count + 1
        if (count>1):
            compName = line.split("\t")[0]
            for company in compDict:
                if (((company + " ") == compName[0:len(company)+1]) or ((company + ",") == compName[0:len(company)+1]) or ((company + ".") == compName[0:len(company)+1]) or ((company + "'") == compName[0:len(company)+1])) and compName!=company:
                    compDict[compName] = compDict[company].copy()
                    itemsToDelete.append(company)


for item in itemsToDelete:
    if item in compDict.keys():
        del compDict[item]

# merge with original data
with open('compData.tsv','r') as in_file:
    count = 0
    for line in in_file:
        count = count + 1
        if (count>1):
            compName, date, hq, visible, category, audience, model, description, main_url, twitter_url, angellist_url, crunchbase_url, tags = line.split("\t")
            data = {"date": date, 
                    "hq": hq, 
                    "category":category, 
                    "audience":audience, 
                    "model":model, 
                    "description": description, 
                    "main_url": main_url, 
                    "twitter_url": twitter_url, 
                    "angellist_url": angellist_url, 
                    "crunchbase_url": crunchbase_url,
                    "linkedin_url": "",
                    "facebook_url": "",
                    "tags": tags}

            if compName not in compDict.keys():
                continue

            data = merge(compDict[compName], data)


            compDict[compName] = data

for compName in compDict:
    for item in compDict[compName]:
        if "Unknown" in compDict[compName][item]:
            compDict[compName][item] = ""

for compName in compDict:
    for item in compDict[compName]:
        if len(compDict[compName][item])>0:
            if " " == compDict[compName][item][0]:
                compDict[compName][item] =  compDict[compName][item][1:]
            if "\n" == compDict[compName][item][-2:]:
                compDict[compName][item] =  compDict[compName][item][:-2]

with open('final.tsv', 'w') as out_file:
    out_file.write("name\t"+"\t".join(list(compDict['Correa Porto'].keys()))+"\n")
    for compName in compDict:
        line = compName
        for description in compDict[compName]:
            line += "\t" + compDict[compName][description]
            if compDict[compName][description] == "":
                line += "n/a"
        if "\n" in line:
            line = line[:-1]
        line += "\n"
        out_file.write(line)

thingsToManuallyCheck = {}

for compName in compDict:
    if compDict[compName]["main_url"]=="":   
        for item in compDict[compName]:
            if "url" in item and compDict[compName][item]=="":
                if compName not in thingsToManuallyCheck:
                    thingsToManuallyCheck[compName] = {}
                thingsToManuallyCheck[compName][item] = ""

            
with open('thingsToManuallyCheck.tsv', 'w') as out_file:
    for company in thingsToManuallyCheck:
        line = company + "\t" + str(thingsToManuallyCheck[company]) + "\n"
        out_file.write(line)