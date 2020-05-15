
with open('updatedWithBlanks.tsv','r') as in_file, open('final_updated.tsv','w') as out_file:
    count = 0
    for line in in_file:
        count +=  1
        if (count >= 2289):
            items = line.split("\t")
            for i in range(len(items)):
                if items[i] == "n/a":
                    items[i] = 0
            newline = "\t".join([str(item) for item in items])
            out_file.write(newline)
