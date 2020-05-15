compDict = {}
count = 0

with open('final_updated.tsv','r') as in_file:
    for line in in_file:
        count = count + 1
        if (count>1):
            compName, date, hq, visible, category, audience, model, description, main_url, twitter_url, angellist_url, crunchbase_url, tags = line.split("\t")
            compName = compName.lower()
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
                                "tags": tags, 
                                "linkedin_url": "0",
                                "facebook_url": "0"}

with open('in_odm.csv','r') as in_file:
    for line in in_file:
        uuid,name,compType,primary_role,cb_url,domain,homepage_url,logo_url,facebook_url,twitter_url,linkedin_url,combined_stock_symbols,city,region,country_code,short_description =  line.split(",")
        name = name.lower()
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
                        "tags": "0", 
                        "linkedin_url": linkedin_url,
                        "facebook_url": facebook_url}

        merged = merge(name, ourCSVDetails, cbDBDetails)
        compDict[name] = merged
        
def merge(name, ourData, cbData):
    goodData = {}
    for item in ourData:
        validData  = check(name, item, ourData[item], cbData[item])
        goodData[item] = validData
    return goodData

thingsToManuallyCheck = {}

def check(name, field, ourItem, cbItem):
    if (ourItem == "0" and cbItem == "0"):
        if not thingsToManuallyCheck[name]:
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
        if not thingsToManuallyCheck[name]:
            thingsToManuallyCheck[name] = []
        thingsToManuallyCheck[name].append(field)
    return "0"

