
with open('compData.csv','r') as in_file, open('updatedData.csv','w') as out_file:
    seen = set() # set for fast O(1) amortized lookup
    for line in in_file:
        compName = line.split(",")[0]
        if compName in seen: continue # skip duplicate

        seen.add(compName)
        out_file.write(line)
