import csv
socials = {}

with open("final/ManualFinalV4/final.tsv") as in_file:
    reader = csv.reader(in_file, delimiter = "\t", quotechar = '"', quoting = csv.QUOTE_MINIMAL)
    for row in reader:
        try:
            subSocials = {"twitter": row[8],
                         "angellist": row[9],
                         "crunchbase": row[10],
                         "linkedin": row[11],
                         "facebook": row[12] }
        except IndexError:
            continue

        for social in subSocials:
            if social not in socials:
                socials[social] = 0
            url = subSocials[social]
            if "n/a" not in url:
                socials[social] += 1
        
with open("output_files/new_research_questions/most_prominent_socials.csv", "w") as out_file:
    for social in socials:
        out_file.write(social + ", " + str(socials[social]) + "\n")

