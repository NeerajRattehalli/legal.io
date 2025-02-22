compDict = {}

# takes the two pieces of data and merges them by relevant category
def merge(name, ourData, cbData):
    goodData = {}
    for item in ourData:
        validData  = check(name, item, ourData[item], cbData[item])
        goodData[item] = validData
    return goodData

# a diciotnary containing all data points that should be checked and validted manually
thingsToManuallyCheck = {}

# determine what is the right value and which to go with
def check(name, field, ourItem, cbItem):
    if (ourItem == "0" and cbItem == "0"):
        if name not in thingsToManuallyCheck.keys():
            thingsToManuallyCheck[name] = []
        thingsToManuallyCheck[name].append(field)
        return "0"
    if (ourItem == "0"):
        return cbItem
    if (cbItem == "0"):
        return ourItem
    if (ourItem in cbItem) or (cbItem in ourItem):
        return ourItem
    else:
        return ourItem

notIncluded = []

#this reads the data from our 2000+ db of items and creates an object like structure containing all the details
with open('compData.tsv','r') as in_file:
    count = 0
    for line in in_file:
        count = count + 1
        if (count>1):
            compName, date, hq, visible, category, audience, model, description, main_url, twitter_url, angellist_url, crunchbase_url, tags = line.split("\t")
            compDict[compName] = {"date": date, 
                                "hq": hq, 
                                "category":category, 
                                "audience":audience, 
                                "model":model, 
                                "description": description, 
                                "main_url": main_url, 
                                "twitter_url": twitter_url, 
                                "angellist_url": angellist_url, 
                                "crunchbase_url": crunchbase_url,
                                "linkedin_url": "0",
                                "facebook_url": "0",
                                "tags": tags}
            if date == "1900":
                if compName not in thingsToManuallyCheck:
                    thingsToManuallyCheck[compName] = []
                thingsToManuallyCheck[compName].append(date)


#this reads from a crunchbase database and gathers any additional information
with open('in_odm.csv','r') as in_file:
    count = 0
    for line in in_file:
        uuid,name,compType,primary_role,cb_url,domain,homepage_url,logo_url,height,width,address,facebook_url,twitter_url,linkedin_url,combined_stock_symbols,city,region,country_code =  line.split(",")[:18]

        if name in compDict.keys():
            ourCSVDetails = compDict[name]

            cbDBDetails = {"date": "0", 
                            "hq": city, 
                            "category": "0", 
                            "audience": "0", 
                            "model": "0", 
                            "description": "0", 
                            "main_url": homepage_url, 
                            "twitter_url": twitter_url, 
                            "angellist_url": "0", 
                            "crunchbase_url": cb_url, 
                            "linkedin_url": linkedin_url,
                            "facebook_url": facebook_url,
                            "tags": "0"}
            merged = merge(name, ourCSVDetails, cbDBDetails)
            compDict[name] = merged
        else:
            thingsToManuallyCheck[name] = ["everything"]
            


# creates merged output file
with open('merged.tsv','w') as out_file:
    for key in compDict:
        line = str(key) + "\t"
        for item in compDict[key]:
            if "n/a" in compDict[key][item] or compDict[key][item]=="0" or compDict[key][item]=="":
                if key not in thingsToManuallyCheck:
                    thingsToManuallyCheck[key] = []
                thingsToManuallyCheck[key].append(item)
            line = line + compDict[key][item] + "\t"
        out_file.write(line)


# creates things to check manually file
with open('thingsToCheckManually.csv', 'w') as out_file:
    for comp in thingsToManuallyCheck:
        line = comp
        for item in thingsToManuallyCheck[comp]:
            line += ", " + item
        line += "\n"
        out_file.write(line)



