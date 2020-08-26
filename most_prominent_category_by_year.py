import csv
import collections



with open("final/ManualFinalV4/final.tsv") as in_file:
    reader = csv.reader(in_file, delimiter = "\t", quotechar = '"', quoting = csv.QUOTE_MINIMAL)
    category_by_year = {}
    for row in reader:
        year = row[1]
        category = row[3]
        if row == "n/a" or category == "n/a" or year =="date":
            continue
        if year not in category_by_year:
            particular_year_categories = {}
            particular_year_categories[category] = 1
            category_by_year[year] = particular_year_categories
        elif category not in category_by_year[year]:
            category_by_year[year][category] = 1
        else:
            category_by_year[year][category] += 1

    for year in category_by_year:
        particular_dict = category_by_year[year]
        max_val = 0
        max_category = ""
        for key in particular_dict:
            if particular_dict[key] > max_val:
                max_val = particular_dict[key]
                max_category = key
        particular_dict = (str(max_category), str(max_val))
        category_by_year[year] = particular_dict
    print(category_by_year)
    ordered_by_year = collections.OrderedDict(sorted(collections.OrderedDict(category_by_year).items(), key=lambda key_value: key_value[0]))
    print(ordered_by_year)


with open("output_files/new_research_questions/most_prominent_category_by_year.csv", "a") as out_file:
    writer = csv.writer(out_file, delimiter =",", quotechar = '"', quoting = csv.QUOTE_MINIMAL)
    for key in ordered_by_year:
        writer.writerow([key, ordered_by_year[key][0], ordered_by_year[key][1]])





