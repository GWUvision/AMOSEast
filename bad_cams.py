import psycopg2
import os
import datetime
import csv


DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='allow').cursor()

all_cameras_query = "SELECT cameraid, name, url, latitude, longitude FROM cameras ORDER BY cameraid"
conn.execute(all_cameras_query)
all_cameras = conn.fetchall()

today = datetime.date.today()

last_updated_list = []

for camera in all_cameras:
    last_updated_query = "SELECT cameraid, curr_time FROM images WHERE cameraid=%d ORDER BY curr_time DESC" % (
        camera[0])
    conn.execute(last_updated_query)
    last_updated_list.append(conn.fetchall())


list2 = [x for x in last_updated_list if x != []]

new_list = [it for it in list2 if it[0][1].date() != today]
# print(new_list)

print(new_list)


# with open('bad_cams.csv', 'w') as myfile:
#     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#     wr.writerow(new_list)



