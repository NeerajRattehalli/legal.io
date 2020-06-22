compDict = {}

with open("found_tags.csv") as in_file:
    for line in in_file:
        company = line.split(",")[0]
        tagDict = eval(line.split("\"")[1])
        compDict[company] = tagDict

def getMax(tags):
    tagCopy = tags.copy()
    bestTag, maxVal = tagCopy.popitem()
    for tag in tagCopy:
        if tagCopy[tag]>maxVal:
            maxVal = tagCopy[tag]
            bestTag = tag
    return (bestTag, maxVal)

def getTop3Tag(tags):
    tagCopy = tags.copy()
    bestList = []
    for i in range(3):
        bestTag, val = getMax(tagCopy)
        bestList.append([bestTag, val])
        print(tagCopy)
        del tagCopy[bestTag]
        print("here", bestList)
    return bestList

top3TagDict = {}
for company in compDict:
    top3TagDict[company] = getTop3Tag(compDict[company])

for company in top3TagDict:
    tags = top3TagDict[company][:]
    for tagPair in top3TagDict[company]:
        if tagPair[1] == 0:
            tags.remove(tagPair)
        top3TagDict[company] = tags

with open("top_tags.tsv", "w") as out_file:
    for company in top3TagDict:
        out_file.write(company + "\t" + str(top3TagDict[company]) + "\n")