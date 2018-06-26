import math
import psycopg2
import os
import pysal
from pysal.cg.kdtree import KDTree    

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='allow').cursor()
all_cameras_query = "SELECT cameraid, name, url, latitude, longitude FROM cameras ORDER BY cameraid"

conn.execute(all_cameras_query)

all_cameras = conn.fetchall()


for i in all_cameras:
    current_point = (all_cameras[i][3], all_cameras[i][4])
    
    

    
tree = KDTree(all_cameras, distance_metric='Arc', radius=pysal.cg.RADIUS_EARTH_MILES)
# current_point = (44.478739, -73.19164)

# get all points within 1 mile of 'current_point'
indices = tree.query_ball_point(current_point, 20)

for i in indices:
    print(all_cameras[i])