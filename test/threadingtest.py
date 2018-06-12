import threading
import os
import psycopg2

from treq import get
from twisted.internet import reactor

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

# urls = [urls.replace('http://', '') for w in words]
# print(urls)
from gevent import monkey; monkey.patch_socket()
import gevent
from gevent import socket
from urllib.request import urlopen
import os

from gevent.pool import Pool
pool = Pool(30)
N = 30

# f = open('images-urllist.txt')
# data = f.readlines()
# f.close()

# urls = []
# for d in data:
#     urls.append(d[:-1])

finished = 0

def download_file(url):
    global finished
    print('starting %s' % url)
    try:
        data = urlopen(url, timeout=10000)
    except urllib.error.URLError as e:
        print('e : %s' % e)
    else:
        data = data.read()
        filename = os.path.basename(url)
        f = open(filename, 'wb')
        f.write(data)
        f.close()
    finally:
        finished += 1


with gevent.Timeout(10000000, False):
    for x in range(10, 10 + N):
        jobs = [pool.spawn(download_file, url) for url in urls]
        pool.join(jobs, type(jobs))

print('Finished {0} {1}'.format(finished, N))
















