import math
import psycopg2
import os
import pysal
import sys
import csv
from pysal.cg.kdtree import KDTree
from gevent import monkey, socket
from gevent.pool import Pool

monkey.patch_socket()
pool = Pool(30)
sys.setrecursionlimit(10000)
csvfile = "good_cams.csv"

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='allow').cursor()
all_cameras_query = "SELECT cameraid, name, url, latitude, longitude FROM cameras ORDER BY cameraid"
conn.execute(all_cameras_query)
all_cameras = conn.fetchall()

locations = []
for camera in all_cameras:
    locations.append((camera[3], camera[4]))


def get_cams(latitude, longitude):
    #list of good camera indexes
    good_cams = []
    locations = []
    locations.append((latitude, longitude))

    for i in range(0, len(all_cameras)):
        current_point = (all_cameras[i][3], all_cameras[i][4])
        print("Checking cam " + str(i))
        indices = None

        for j in range(0, len(all_cameras)):
            if(i == j):
                break
            else:
                tree = KDTree(locations, distance_metric='Arc', radius=pysal.cg.RADIUS_EARTH_MILES)
                # # get all points within 1 mile of 'current_point'
                indices = tree.query_ball_point(current_point, 20)

        #if there are no indices, then add it to the list, because this means there are no cams in 20 mile radius
        if not indices:
            good_cams.append(i)
            print(str(i) + " is a good cam!")


    #write to the csv
    with open(csvfile, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in good_cams:
            writer.writerow([val])

jobs = [pool.spawn(get_cams, latitude, longitude)
            for latitude, longitude in locations]
print("Acquired cams")
