import psycopg2
import os
import pandas as pd
import csv

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='allow')
cur = conn.cursor()

df = pd.read_csv('cameras_to_remove.csv')
df.columns = ['index', 'cameraid']
bad_cams_list = df['cameraid'].values.tolist()

for camera in bad_cams_list:
	print(camera)
	print("Deleting ", camera)

	query = "DELETE FROM images WHERE cameraid=%d" %(camera)
	cur.execute(query)

	query2 = "DELETE FROM cameras WHERE cameraid=%d" %(camera)
	cur.execute(query2)


conn.commit()

print("Cameras Deleted.")
