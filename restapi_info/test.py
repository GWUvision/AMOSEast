import csv
with open('data.csv', 'rb') as inp, open('data_edit.csv', 'wb') as out:
    writer = csv.writer(out)
    for row in csv.reader(inp):
        string = row[2]
        if string[:4] == "http":
            writer.writerow(row)
