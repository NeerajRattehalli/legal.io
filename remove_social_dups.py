

with open('companiesWithSocials.csv', 'r') as in_file, open('companiesWithSocialsNoDups.csv', 'w') as out_file:
    seen = set() #
    # set for fast O(1) amortized lookup
    for line in in_file:
        name = line.split(",")[0]
        if name in seen: continue # skip duplicate
        seen.add(name)
        out_file.write(line)