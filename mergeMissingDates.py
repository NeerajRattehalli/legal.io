companyMainDict = {}

# Read Input Data
with open('final/ManualFinalV2/8-14-20-final.tsv','r') as in_file:
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


def getBestDate(dates):
    maxDateCount = -2
    maxDate = 0
    cond = True

    for date in dates:
        if dates[date] > maxDateCount:
            prevCount = maxDateCount
            maxDate = date
            maxDateCount = dates[date]
            cond = (maxDateCount - prevCount) > 3
    
    if cond:
        return maxDateCount
    else:
        return ""

    
with open('company_founding_date.csv', 'r') as in_file:
    for line in in_file:
        try:
            if "\"" in line:
                company, dateDict = line.split(",\"")
                if "\"" in company:
                    company = company[1:-1]
                company = eval(company)[0]
                print(company)
                dateDict = eval(dateDict[:-2])
                bestDate = getBestDate(dateDict)
                companyMainDict[company]["date"] = bestDate
            else:
                company, dateDict = line.split(",")
                company = eval(company)[0]
                dateDict = eval(dateDict)
                bestDate = getBestDate(dateDict)
                companyMainDict[company]["date"] = bestDate
        except:
            continue

