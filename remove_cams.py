import psycopg2
import os
import Pandas
import csv

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='allow').cursor()

csvfile = "good_cam.csv"

cameras = []

#get the second column
with open(filename, 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    cameras = [float(row[1]) for row in reader]

for i in range(0, len(cameras)):
    print("Deleting ", cameras[i])
    query = "DELETE FROM cameras WHERE cameraid = " % (cameras[i])
    conn.execute(query)

print("Cameras Deleted.")
