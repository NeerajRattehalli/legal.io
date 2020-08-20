from final_code.research_pipeline_updated_success import ResearchPipeline

# type_success = ResearchPipeline.company_type_success_correlation("final/google-sheets/8:18:20.tsv", "\t")
# for key in type_success:
#     print(type_success[key].__str__())

# country = ResearchPipeline.success_location_correlation("final/google-sheets/8:18:20.tsv", "\t")
# for key in country:
#     print(country[key].__str__())

arr = ResearchPipeline.most_common_company_types("final/google-sheets/8:18:20.tsv", "\t")
for element in arr:
    print(str(element) + "," + str(arr[element]))
