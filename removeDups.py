
with open('compData.tsv','r') as in_file, open('updatedData.tsv','w') as out_file:
    seen = set() # set for fast O(1) amortized lookup
    for line in in_file:
        compName = line.split("\t")[0]
        if compName in seen: continue # skip duplicate

        seen.add(compName)
        out_file.write(line)
