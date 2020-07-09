import csv

def modifyFiles(inputPath, outputPath):
    with open(inputPath, "r") as in_file, open(outputPath,'w') as out_file:
        csv_reader = csv.reader(in_file, quotechar='"', delimiter=',',
                     quoting=csv.QUOTE_ALL, skipinitialspace=True)
        for line in csv_reader:
            compName, compUrl, statusCode = line
            out_file.write(", ".join([compName, compUrl]) + ", " + str({"status": ""}) + "\n")

modifyFiles("output_files/200_codes.csv", "TXTFiles/david/david.csv")
modifyFiles("output_files/300_codes.csv", "TXTFiles/neel/neel.csv")
modifyFiles("output_files/400_codes.csv", "TXTFiles/neeraj/neeraj.csv")