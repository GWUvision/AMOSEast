#!/pless_nfs/home/suraj98/GWU-Pless/env/bin/python
import datetime
import sqlite3
import os
import requests
import hashlib
import base64
import urllib.request
import http.client
# import cv2
# import imageio

from urllib.parse import urlparse
from socket import timeout
from socket import error as SocketError

# from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize

db = sqlite3.connect('allimages.db')
conn = db.cursor()

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

DATABASE_URL = os.environ['DATABASE_URL']
database = psycopg2.connect(DATABASE_URL, sslmode='require')
# df = pd.read_sql_query("SELECT * FROM history", database)


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()



# def video_dir():
# 
#     # threading.Timer(86400.0, self.video_dir).start()
#     list_of_images = []
#     rootDir = 'images/'
#     for dirpath, dirnames, files in os.walk(rootDir, topdown=True):
#         dirnames.sort(key=int)
#         list_of_images.append(files)
# 
#     for i in range(1, len(list_of_images), 1):
#         images_in_folder = []
#         os.makedirs('videos/%d' % (i), exist_ok=True)
# 
#         for j in range(len(list_of_images[i])):
#             print(list_of_images[i][j])
#             file_path = os.path.join('images/%d' %
#                                      (i), list_of_images[i][j])
# 
#             images_in_folder.append(imageio.imread(file_path))
#         imageio.mimsave('videos/%d/movie%d.mp4' %
#                         (i, i), images_in_folder)


def image_insert():

    query = "SELECT * FROM image_info"
    conn.execute(query)
    data = conn.fetchall()

    for val in data:

        try:
            query2 = "SELECT md5_hash from all_images WHERE cameraID=%d;" % (
                val[0])
            conn.execute(query2)
            data2 = conn.fetchall()

            a = data2[-2][0]
            b = data2[-1][0]

            if(a == b):
                print("Pictures are the same. Skipping image...")
                pass
            else:
                print("Pictures are different.", end=" ")
                try:

                    # use datetime to get current time for the files
                    dt = str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
                    print('Adding %s to file#%s...' % (val[2], val[0]))

                    # creates new directory
                    os.makedirs('static/images/%s' % (val[0]), exist_ok=True)

                    myrequest = urllib.request.Request(val[2], None, headers)
                    response = urllib.request.urlopen(myrequest, timeout=5)
                    f = open('static/images/%s/%s.jpg' % (val[0], dt), 'wb')

                    # gets the filepath and the filename and puts it into the database
                    filepath = ('%s/%s.jpg' % (val[0], dt))
                    f.write(response.read())
                    f.close()

                    # after connecting to the db, execute the query for the variables and curr_time
                    query = 'INSERT INTO all_images(filepath, url, curr_time, cameraID, md5_hash) VALUES (?, ?, ?, ?, ?)'

                    conn.execute(query, (filepath, val[2], dt, val[0], md5(
                        'static/images/%s' % filepath)))

                    db.commit()

                except urllib.error.HTTPError as err:
                    pass
                except urllib.error.URLError as err:
                    pass
                except timeout:
                    pass
                except http.client.HTTPException as err:
                    pass
                except http.client.IncompleteRead as err:
                    pass
                except http.client.ImproperConnectionState as err:
                    pass
                except http.client.RemoteDisconnected as err:
                    pass
                except ConnectionResetError as err:
                    pass
                except SocketError as err:
                    pass

        except IndexError as e:
            pass

# image_insert()

