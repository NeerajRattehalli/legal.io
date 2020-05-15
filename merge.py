compDict = {}
count = 0

with open('final_updated.tsv','r') as in_file:
    for line in in_file:
        count = count + 1
        if (count>1):
            compName, date, hq, visible, category, audience, model, description, main_url, twitter_url, angellist_url, crunchbase_url, tags = line.split("\t")
            compName = compName.lower()
            compDict[compName] = {"date": [date], 
                                "hq": [hq], 
                                "visible": [visible], 
                                "category":[category], 
                                "audience":[audience], 
                                "model":[model], 
                                "description":[description], 
                                "main_url": [main_url], 
                                "twitter_url":[twitter_url], 
                                "angellist_url":[angellist_url], 
                                "crunchbase_url":[crunchbase_url], 
                                "tags":[tags]}


correspondingTags = {
    "main_url": "homepage_url",
    "crunchbase_url": "cb_url",
    
}

with open('in_odm.csv','r') as in_file:
    for line in in_file:
        uuid,name,compType,primary_role,cb_url,domain,homepage_url,logo_url,facebook_url,twitter_url,linkedin_url,combined_stock_symbols,city,region,country_code,short_description =  line.split(",")
        name = name.lower()
        
        if homepage_url:
            name = name.lower()
            if(compDict[name][main_url]==0):
                compDict[name][main_url] = [homepage_url]
            elif (compDict[name][main_url] == "n/a"):
                compDict[name][main_url] = [homepage_url]
            elif (compDict[name][main_url][0] == homepage_url):
                continue
            elif (compDict[name][main_url][0] in homepage_url) or (homepage_url in compDict[name][main_url][0]):    
                continue
            else:
                compDict[name][main_url].append(homepage_url)


def mergeItem(companyName, updatedTag, odmTag):
    if odmTag:
        if(compDict[companyName][updatedTag]==0):
            compDict[companyName][updatedTag] = [odmTag]
        elif (compDict[companyName][updatedTag] == "n/a"):
            compDict[companyName][updatedTag] = [odmTag]
        elif (compDict[companyName][updatedTag][0] == odmTag):
            return
        elif (compDict[companyName][updatedTag][0] in odmTag) or (odmTag in compDict[companyName][updatedTag][0]):    
            return 
        else:
            compDict[companyName][updatedTag].append(odmTag)
