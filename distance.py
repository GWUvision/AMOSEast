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


csvfile = "distance.csv"

# Place map
gmap = gmplot.GoogleMapPlotter(0, 0, 13)

#reding from csv instead of database
df = pd.read_csv('ratings.csv')
print(df)

#getting the locations and camera ids
locations = []
ids = []

for index, row in df.iterrows():
    locations.append((row['latitude'], row['longitude']))
    ids.append(row['cameraid'])

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
good_index = [ids[0]]

for i in range(1, len(locations)):
    print("Checking cam " + str(ids[i]))

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
        print(str(ids[i]) + " is a good cam!")
        good_cams.append((locations[i][0], locations[i][1]))
        good_index.append(ids[i])

        #add marker to map
        gmap.marker(lat, lon, 'cornflowerblue')
    else:
        #add marker to map
        gmap.marker(lat, lon, 'red')

with open(csvfile, "a") as output:
    writer = csv.writer(output, delimiter=',', lineterminator='\n')
    for val in good_index:
        writer.writerow([val])

# Draw
gmap.draw("my_map.html")
