
with open('updatedWithBlanks.tsv','r') as in_file, open('final_updated.tsv','w') as out_file:
    count = 0
    for line in in_file:
        count +=  1
        if (count >= 2289):
            out_file.write(line)
