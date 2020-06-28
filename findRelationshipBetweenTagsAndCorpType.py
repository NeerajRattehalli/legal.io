# Tags finding

tags = []

with open("tags.txt", "r") as in_file:
    for line in in_file:
        newLine = line.replace("\n", "")
        tags.append(newLine)

# Company Finding

compTypes = []
    
with open("stanford_tags.txt", "r") as in_file:
    for line in in_file:
        newLine = line.replace("\n", "")
        compTypes.append(newLine)

# Initialize relationship dict
compToTagsDict = {}

for comp in compTypes:
    compToTagsDict[comp] = {}

with open("./output_files/final.tsv") as in_file:
    count = 0
    for line in in_file:
        if count>0:
            parts = line.split("\t")
            companyType = parts[3]
            for comp in compTypes:
                if comp in companyType:
                    companyType = comp
            companyTags = parts[-1]

            if companyType not in compTypes:
                continue


            for tag in companyTags.split(", "):
                newTag = tag.replace("\n", "")
                if newTag not in tags:
                    continue
                if newTag not in compToTagsDict[companyType]:
                    compToTagsDict[companyType][newTag] = 0
                compToTagsDict[companyType][newTag] += 1
            
        count += 1


# with open("think.tsv", "w") as out_file:
#     for key in compToTagsDict:
#         out_file.write(key + "\t" + str(compToTagsDict[key]) + "\n")

relationShipDict = {}
with open("thinkManual.tsv", "r") as in_file:
    for line in in_file:
        compType, compDict  = line.split("\t")
        compDict = eval(compDict)
        for tag in compDict:
            relationShipDict[tag] = compType

print(relationShipDict)