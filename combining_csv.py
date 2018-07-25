import csv
import pandas as pd

# good_cams = pd.read_csv('good_cams.csv', usecols=[5])
# distance = pd.read_csv('distance.csv', usecols=[0])

# ratings = csv.reader(open('ratings.csv', 'rt'), delimiter=",")
# distance = csv.reader(open('distance.csv', 'rt'), delimiter=",")

#this output is just the values in distance which are not
output = []
count = 0

distance_col = ['cameraid']
ratings_col = ['ID', 'name', 'url', 'latitude', 'longitude', 'cameraid', 'last_width', 'last_height', 'rating', 'inuse']

distance = pd.read_csv('distance.csv', names=distance_col)
ratings = pd.read_csv('ratings.csv', names=ratings_col)

distance_id = distance.cameraid.tolist()
camera_id = ratings.cameraid.tolist()
good_ratings = ratings.rating.tolist()


#first get the good cams
for i in range(0, len(camera_id)):
    if(good_ratings[i] == '1'):
        output.append([camera_id[i]])

print(output)

#this will prevent it from adding things again and again
size = len(output)

#then add all of the distance ones
for i in range(1, len(distance_id)):
    found = False
    for j in range(0, size):
        if(distance_id[i] == output[j]):
            found = True

    if(found):
        continue
    else:
        output.append([distance_id[i]])


print(output)

with open('combined_sets.csv', 'w') as myfile:
    wr = csv.writer(myfile, lineterminator='\n', delimiter=',')
    for row in output:
        print(row)
        wr.writerow(row)



# result.drop(columns=['inuse', 'longitude', 'latitude', 'name'])

# print(result.head())

#print(df['cameraid'][0])

# for row in distance:
#     found = False
#     for line in ratings:
#         #print(line[5])
#         #print(row)
#
#         #if the cameraid in distance and ratings
#         if(line[5] == row[0]):
#             found = True
#
#     #if the program finds the id
#     if(found):
#         continue
#     else:
#         output.append(line[5])
#
#     count = count + 1
#
# print(output)
# print(count)


# print(distance.iloc[1][0])
#
# for i in range(0, len(good_cams.iloc[0])):
#     print(distance.iloc[i][0])
#     print(good_cams.iloc[i]['cameraid'])

# with open(myfilepath, 'rb') as f:
#     mycsv = csv.reader(f)
#     for row in mycsv:
#         text = row[1]
