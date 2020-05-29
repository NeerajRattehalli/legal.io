import re

def check(urlString, compName, url):
    # checks if the required string is in the url link itself
    if urlString not in url:
        return False
    
    # Case 1: Company Name has no spaces
    if " " not in compName:

        # splits at uppercase letters
        splitName = re.findall('[A-Z][^A-Z]*', compName)

        #lowercase url
        url = url.lower()

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


# CHECKS

print(check("facebook", "Chapter 11 Dockets", " https://www.chapter11dockets.com/"))
print(check("twitter", "Corporize",  " https://twitter.com/corporatize"))
print(check("twitter", "DISCO", "twitter"))
print(check("facebook", "MyCourthouse", " https://www.facebook.com/courthouseclubs/videos/on-the-second-day-of-christmas-my-trainer-brought-to-me-push-ups-how-many-can-yo/569793773433336/"))
print(check("twitter", "PayMyTrustee", " https://twitter.com/paymytrustee"))

# with open('compananiesWithSocialsNoDups.csv','r') as in_file:
#     for line in in_file:
#         compName = line.split(", ")[0]
#         jsonDump = eval(line.split(", ")[-1])

#         relationArr = {
#             " twitter_url": "twitter",
#             " angellist_url": "angel",
#             " facebook_url": "facebook",
#             " linkedin_url": "linkedin",
#             " crunchbase_url": "crunchbase",
#             " main_url": ""
#         }

#         for item in jsonDump:
#             check(relationArr[item], compName, jsonDump[item])



