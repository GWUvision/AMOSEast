import csv

input_file = "ratings.csv"
output_file = "good_cams.csv"

data = csv.reader(open(input_file))

with open(input_file, 'r') as data_csv:
    data = csv.reader(data_csv)

    for line in data:
        if(line[8] == '1'):
            string = ''
            for i in range(0, len(line)):
                string = string + str(line[i]) + ','

            fd = open('output.csv','a+')
            fd.write(string + "\n")
            fd.close()
            print(line[5])
