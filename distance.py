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

locations = []
for cameras in all_cameras:
    locations.append((cameras[3], cameras[4]))

good_cams = []

for i in range(0, len(all_cameras)):
    current_point = (all_cameras[i][3], all_cameras[i][4])

    for j in range(0, len(all_cameras)):
        tree = KDTree(locations, distance_metric='Arc', radius=pysal.cg.RADIUS_EARTH_MILES)

        # # get all points within 1 mile of 'current_point'
        indices = tree.query_ball_point(current_point, 20)
    #if there are no indices, then add it to the list, because this means there are no cams in 20 mile radius
    if(!indices):
        good_cams.append(i)
        print(str(i) + " is a good cam!")
    # print(current_point)

    #for i in indices:
        #print(all_cameras[i])
