# import aiohttp
# import asyncio
# import async_timeout
# import os

import os
import psycopg2

# import Queue
import threading
# import urllib2
import time
# from BeautifulSoup import BeautifulSoup
# import urllib.request
import urllib


headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

sql = "SELECT * from cameras"
cur.execute(sql)
rows = cur.fetchall()

urls = []
for row in rows:
    urls.append(row[2])
 
from multiprocessing import Pool
from multiprocessing import Pool
from progress.bar import Bar
import urllib.request
from urllib.parse import urlparse
from socket import timeout
from socket import error as SocketError
import requests
import http.client
import datetime


def job(url):
    
    dt = str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    
    try:
        
        # file_name = str(url.split('/')[-1])
        u = urllib.request.urlopen(url, timeout=5)

        # f = open('%s.jpg' % (dt), 'wb')

        f = open(file_name, 'wb')
        print(file_name)
        f.write(u.read())
        f.close()
    except urllib.error.HTTPError as err:
        print(err)
    except urllib.error.URLError as err:
        print(err)
    except timeout as err:
        print(err)
    except http.client.HTTPException as err:
        print(err)
    except http.client.IncompleteRead as err:
        print(err)
    except http.client.ImproperConnectionState as err:
        print(err)
    except http.client.RemoteDisconnected as err:
        print(err)
    except ConnectionResetError as err:
        print(err)
    except SocketError as err:
        print(err)
        

pool = Pool(processes=8)
pool.map(job, urls)

inputs = range(len(urls))
bar = Bar('Processing', max=len(inputs))
for i in pool.imap(job, inputs):
    bar.next()
bar.finish()


