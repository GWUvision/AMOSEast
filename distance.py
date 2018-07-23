from math import radians, cos, sin, asin, sqrt
import psycopg2
import os
import pysal
import sys
import csv
from pysal.cg.kdtree import KDTree
from gevent import monkey, socket
from gevent.pool import Pool
import pandas as pd
from gmplot import gmplot

# monkey.patch_socket()
# pool = Pool(30)
# sys.setrecursionlimit(10000)
csvfile = "distance.csv"

# Place map
gmap = gmplot.GoogleMapPlotter(0, 0, 13)

#Get info from the database
# DATABASE_URL = os.environ['DATABASE_URL']
# conn = psycopg2.connect(DATABASE_URL, sslmode='allow').cursor()
# all_cameras_query = "SELECT cameraid, name, url, latitude, longitude FROM cameras ORDER BY cameraid"
# conn.execute(all_cameras_query)
# all_cameras = conn.fetchall()

#reding from csv instead of database
df = pd.read_csv('ratings.csv')
print(df)

locations = []

for index, row in df.iterrows():
    locations.append((row['latitude'], row['longitude']))

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
radius = 30.0 # in kilometer
good_cams = [(locations[0][0], locations[0][1])]
index = []

for i in range(1, len(locations)):
    print("Checking cam " + str(i))

    lat1 = locations[i][0]
    lon1 = locations[i][1]
    good = True #0 means it is a good camera

    if(lat1 == 0 and lon1 == 0):
        good = False

    for j in range(1, len(good_cams)):
        lat2 = good_cams[j][0]
        lon2 = good_cams[j][1]

        a = haversine(lon1, lat1, lon2, lat2)

        #print('Distance (km) : ', a)
        if(a <= radius and a != 0):
            good = False #1 means it is no longer a default good cam

    lat, lon = locations[i][0], locations[i][1]
    if(good):
        print(str(i) + " is a good cam!")
        good_cams.append((locations[i][0], locations[i][1]))
        index.append(str(i))

        #add marker to map
        gmap.marker(lat, lon, 'cornflowerblue')
    else:
        #add marker to map
        gmap.marker(lat, lon, 'red')

for cam in good_cams:
    # Marker
    hidden_gem_lat, hidden_gem_lon = 37.770776, -122.461689
    gmap.marker(hidden_gem_lat, hidden_gem_lon, 'cornflowerblue')


with open(csvfile, "a") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in index:
        writer.writerow([val])

# Draw
gmap.draw("my_map.html")



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
