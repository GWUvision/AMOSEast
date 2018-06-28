from math import radians, cos, sin, asin, sqrt
import psycopg2
import os
import pysal
import sys
import csv
from pysal.cg.kdtree import KDTree
from gevent import monkey, socket
from gevent.pool import Pool

# monkey.patch_socket()
# pool = Pool(30)
# sys.setrecursionlimit(10000)
csvfile = "good_cams.csv"

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='allow').cursor()
all_cameras_query = "SELECT cameraid, name, url, latitude, longitude FROM cameras ORDER BY cameraid"
conn.execute(all_cameras_query)
all_cameras = conn.fetchall()

locations = []
for camera in all_cameras:
    locations.append((camera[3], camera[4]))

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

#some globals we need
radius = 10.0 # in kilometer
good_cams = []

for i in range(0, len(all_cameras)):
    print("Checking cam " + str(i))

    lat1 = locations[i][0]
    lon1 = locations[i][1]
    good = True #0 means it is a good camera

    for j in range(1, len(all_cameras)):
        lat2 = locations[j][0]
        lon2 = locations[j][1]

        a = haversine(lon1, lat1, lon2, lat2)

        #print('Distance (km) : ', a)
        if a <= radius:
            good = False #1 means it is no longer a default good cam

    if(good):
        print(str(i) + " is a good cam!")
        good_cams.append(i)
        #write to the csv
        with open(csvfile, "a") as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerow(i)

print(good_cams)






# def get_cams(latitude, longitude):
#     for i in range(0, len(all_cameras)):
#         #current_point = (all_cameras[i][3], all_cameras[i][4])
#         current_point = (latitude, longitude)
#         print("Checking cam " + str(i))
#         indices = None
#
#         for j in range(0, len(all_cameras)):
#             if(i == j):
#                 break
#             else:
#                 tree = KDTree(locations, distance_metric='Arc', radius=pysal.cg.RADIUS_EARTH_MILES)
#                 # # get all points within 20 mile of 'current_point'
#                 indices = tree.query_ball_point(current_point, 20)
#
#         #if there are no indices, then add it to the list, because this means there are no cams in 20 mile radius
#         if not indices:
#             good_cams.append(i)
#             print(str(i) + " is a good cam!")
#
#
#     #write to the csv
#     with open(csvfile, "a") as output:
#         writer = csv.writer(output, lineterminator='\n')
#         for val in good_cams:
#             writer.writerow([val])
#
# jobs = [pool.spawn(get_cams, latitude, longitude)
#             for latitude, longitude in locations]
# print("Acquired cams")
