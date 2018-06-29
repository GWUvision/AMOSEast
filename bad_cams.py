import psycopg2
import os
import datetime
import csv
import pandas as pd


DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='allow').cursor()

all_cameras_query = "SELECT cameraid, name, url, latitude, longitude FROM cameras ORDER BY cameraid"
conn.execute(all_cameras_query)
all_cameras = conn.fetchall()

today = datetime.date.today()

last_updated_list = []

print("getting all cameras...")
for camera in all_cameras:
    last_updated_query = "SELECT cameraid, curr_time FROM images WHERE cameraid=%d ORDER BY curr_time DESC LIMIT 40" % (camera[0])
    conn.execute(last_updated_query)
    last_updated_list.append(conn.fetchall())


print("removing all empty lists from list...")
list2 = [x for x in last_updated_list if x != []]

print("checking which cameras have not been captured today")
new_list = [it for it in list2 if it[0][1].date() != today]


with open("out.csv","w") as f:
    wr = csv.writer(f,delimiter="\n")
    wr.writerow(new_list)

# print("creating dataframe")
# df = pd.DataFrame(new_list, columns=['tuple'])

# print("changing from one column to two")
# df[['cameraid', 'last_captured']] = df['tuple'].apply(pd.Series)
# df.drop('tuple', axis=1, inplace=True)
# print(df.head())

# print("copying to csv")
# df.to_csv('bad_cams.csv')


