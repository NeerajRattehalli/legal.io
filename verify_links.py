import re

def check(urlString, compName, url):
    if urlString not in url:
        return False
    if len(compName) == 1:
        splitName = re.findall('[A-Z][^A-Z]*', compName)
        url = url.lower()
        if len(splitName) == 1 or len(splitName) == len(compName):
            compName = compName.lower()
            return compName in url
        else:
            prevIndex = -1
            for item in splitName:
                modified = item.lower()
                if modified not in url:
                    return False
                index = url.find(modified)
                if prevIndex > index:
                    return False
                prevIndex = index    
        return True
    

with open('compananiesWithSocialsNoDups.csv','r') as in_file:
    for line in in_file:
        compName = line.split(", ")[0]
        jsonDump = eval(line.split(", ")[-1])

        relationArr = {
            " twitter_url": "twitter",
            " angellist_url": "angel",
            " facebook_url": "facebook",
            " linkedin_url": "linkedin",
            " crunchbase_url": "crunchbase",
            " main_url": ""
        }

        for item in jsonDump:
            check(relationArr[item], compName, jsonDump[item])


