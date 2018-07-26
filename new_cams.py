import csv
import pandas as pd
import numpy as np

new_cams_col = ['cameraid']
all_cams_col = ['cameraid', 'name', 'url', 'latitude', 'longitude', 'last_width', 'last_height', 'mhash']

new_cams = pd.read_csv('combined_sets.csv', names=new_cams_col)
all_cams = pd.read_csv('all_cams.csv', names=all_cams_col)

new_cams_id = new_cams.cameraid.tolist()
all_cams_id = all_cams.cameraid.tolist()
all_cams_name = all_cams.name.tolist()
all_cams_url = all_cams.url.tolist()
all_cams_latitude = all_cams.latitude.tolist()
all_cams_longitude = all_cams.longitude.tolist()
all_cams_last_width = all_cams.last_width.tolist()
all_cams_last_height = all_cams.last_height.tolist()
all_cams_mhash = all_cams.mhash.tolist()

all_cams_list = [['cameraid', 'name', 'url', 'latitude', 'longitude', 'last_width', 'last_height', 'mhash']]

for i in range(1, len(all_cams_id)):
    all_cams_list.append([all_cams_id[i], all_cams_name[i], all_cams_url[i], all_cams_latitude[i], all_cams_longitude[i], all_cams_last_width[i], all_cams_last_height[i], all_cams_mhash[i]])



series = pd.Series(all_cams_list)

print(series)

df = series.isin(new_cams_id)
print(df)






all_cams_output = [['cameraid', 'name', 'url', 'latitude', 'longitude', 'last_width', 'last_height', 'mhash']]

with open('new_cams.csv', 'w') as myfile:
    wr = csv.writer(myfile, lineterminator='\n', delimiter=',')
    for row in all_cams_output:
        print(row)
        wr.writerow(row)


# mysqlimport --ignore-lines=1 --fields-terminated-by=, --verbose --local -u root AMOSEast /Users/kylerood/AMOSEast/csv_data/all_cams.csv
#
#
#
# delete from all_cams where cameraid not in (select cameraid from cameras);



# #add the image to the list if the image id appears in cameras
# for i in range(1, len(all_cams_id)):
#     for j in range(0, len(new_cams_id)):
#         print(all_cams_id[i])
#         print(new_cams_id[j])
#         if(all_cams_id[i] == new_cams_id[j]):
#             all_cams_output.append([all_cams_id[i], all_cams_name[i], all_cams_url[i], all_cams_latitude[i], all_cams_longitude[i], all_cams_last_width[i], all_cams_last_height[i], all_cams_mhash[i]])
