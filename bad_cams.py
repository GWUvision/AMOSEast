import psycopg2
import os


DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='allow').cursor()

all_cameras_query = "SELECT cameraid, name, url, latitude, longitude FROM cameras ORDER BY cameraid"
conn.execute(all_cameras_query)
all_cameras = conn.fetchall()


last_updated_list = []

for camera in all_cameras[:3]:    
    last_updated_query = "SELECT cameraid, curr_time FROM images WHERE cameraid=%d ORDER BY curr_time DESC" %(camera[0])
    conn.execute(last_updated_query)
    last_updated_list.append(conn.fetchall())
    
print(last_updated_list)

