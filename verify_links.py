import re

def check(urlString, compName, url):
    # checks if the required string is in the url link itself
    if urlString not in url:
        return False

    #lowercase url
    url = url.lower()

    # Case 1: Company Name has no spaces
    
        
    if " " not in compName:
        
        if "." in compName:
            # Splits companies names
            compNameWord = compName.split(".")

            # prelim parsing
            for word in compNameWord:

                # lowers each element
                lowerWord = word.lower()
                
                #checks that it's not a useless word
                if "inc" in lowerWord or "llc" in lowerWord or "p.c." in lowerWord:
                    continue
                else:
                    #checks that each word is part of url
                    if lowerWord not in url:
                        return False

        # all conditions work for len > 1
        return True
        # splits at uppercase letters
        splitName = re.findall('[A-Z][^A-Z]*', compName)

        # edge cases that need direct checking
        if len(splitName) == 1:
            compName = compName.lower()
            return compName in url
        if len(splitName) == len(compName):
            return False
        else:
            # index system that checks for increasing pattern in text
            prevIndex = -1

            # verification for each part of the name
            for item in splitName:
                # lowers so easy compare
                modified = item.lower()
                # direct check
                if modified not in url:
                    return False
                #does the increase index checking
                index = url.find(modified)
                if prevIndex > index:
                    return False
                prevIndex = index   
        # passed all the tests for len = 1 
        return True
    else:

        # Splits companies names
        compNameWord = compName.split(" ")

        # prelim parsing
        for word in compNameWord:

            # lowers each element
            lowerWord = word.lower()
            
            #checks that it's not a useless word
            if "inc" in lowerWord or "llc" in lowerWord or "p.c." in lowerWord:
                continue
            else:
                #checks that each word is part of url
                if lowerWord not in url:
                    return False

        # all conditions work for len > 1
        return True
            

# CHECKS

# print(check("facebook", "Chapter 11 Dockets", " https://www.chapter11dockets.com/"))
# print(check("twitter", "Corporize",  " https://twitter.com/corporatize"))
# print(check("twitter", "DISCO", "twitter"))
# print(check("facebook", "MyCourthouse", " https://www.facebook.com/courthouseclubs/videos/on-the-second-day-of-christmas-my-trainer-brought-to-me-push-ups-how-many-can-yo/569793773433336/"))
# print(check("twitter", "PayMyTrustee", " https://twitter.com/paymytrustee"))

# print(check("twitter", "Free Law Project", ' https://twitter.com/FreeLawProject?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor'))
# print(check("twitter", "PSS Systems", " https://twitter.com/pss_systems?lang=en"))
# print(check("twitter", "Legal.io", " https://twitter.com/Legal_io?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor"))
# print(check("twitter", "Legal Passage", " https://help.twitter.com/en/rules-and-policies/twitter-legal-faqs"))

verifiedDict = {}
thingsToManuallyCheck = {}

with open('companiesWithSocialsNoDups.csv','r') as in_file:
    for line in in_file:
        compName = line.split(", ")[0]
        startCurl = line.find("{")
        endCurl = line.find("}")
        if startCurl < 0:
            continue

        jsonDump = eval(line[startCurl: endCurl+1])

        relationArr = {
            " twitter_url": "twitter",
            " angellist_url": "angel",
            " facebook_url": "facebook",
            " linkedin_url": "linkedin",
            " crunchbase_url": "crunchbase",
            " main_url": ""
        }

        for item in jsonDump:
            if item ==" main_url":
                continue
            if check(relationArr[item], compName, jsonDump[item]):
                if compName not in verifiedDict:
                    verifiedDict[compName] = {}
                verifiedDict[compName][item[1:]] = jsonDump[item]
            else:
                if compName not in thingsToManuallyCheck:
                    thingsToManuallyCheck[compName] = []
                thingsToManuallyCheck[compName].append(item[1:])


# line = 'Brightleaf, 1900, date, category, audience, model,"{" twitter_url": " https://twitter.com/brightleaf", " angellist_url": " https://angel.co/company/brightleaf-power-1", " main_url": " https://www.brightleaf.com/"}'
# startCurl = line.find("{")
# endCurl = line.find("}")
# print(eval(line[startCurl:endCurl+1])[' twitter_url'])
#  ADD MAIN URL CHECKING NOT THERE YET

