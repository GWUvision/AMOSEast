import os
import psycopg2

import Queue
import threading
import urllib2
import time
from BeautifulSoup import BeautifulSoup
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

hosts = []
for row in rows:
    hosts.append(row[2])
 
from gevent import monkey; monkey.patch_socket()
import gevent
from gevent import socket
import urllib2
import os

from gevent.pool import Pool
pool = Pool(30)
N = 30

f = open('images-urllist.txt')
data = f.readlines()
f.close()

urls = []
for d in data:
    urls.append(d[:-1])

finished = 0

def download_file(url):
    global finished
    print('starting %s' % url)
    try:
        data = urllib2.urlopen(url, timeout=10000)
    except urllib2.URLError, e:
        print 'e : ' % e
    else:
        data = data.read()
        filename = os.path.basename(url)
        f = open(filename, 'wb')
        f.write(data)
        f.close()
    finally:
        finished += 1


with gevent.Timeout(10000000, False):
    for x in xrange(10, 10 + N):
        jobs = [pool.spawn(download_file, url) for url in urls]
        pool.join(jobs)

print('Finished %s' % (finished, N))
 
 
# queue = Queue.Queue()
# out_queue = Queue.Queue()
# 
# 
# class ThreadUrl(threading.Thread):
#     """Threaded Url Grab"""
#     def __init__(self, queue, out_queue):
#         threading.Thread.__init__(self)
#         self.queue = queue
#         self.out_queue = out_queue
# 
#     def run(self):
#         while True:
#             #grabs host from queue
#             host = self.queue.get()
# 
#             filename = host.replace('http://', '')
#             #grabs urls of hosts and then grabs chunk of webpage
#             url = urllib2.urlopen(host)
#             chunk = urllib.urlretrieve(url, filename)
#             #place chunk into out queue
#             self.out_queue.put(chunk)
# 
#             #signals to queue job is done
#             self.queue.task_done()
# 
# class DatamineThread(threading.Thread):
#     """Threaded Url Grab"""
#     def __init__(self, out_queue):
#         threading.Thread.__init__(self)
#         self.out_queue = out_queue
# 
#     def run(self):
#         while True:
#             #grabs host from queue
#             chunk = self.out_queue.get()
# 
#             #parse the chunk
#             # soup = BeautifulSoup(chunk)
#             # print soup.findAll(['title'])
# 
#             #signals to queue job is done
#             self.out_queue.task_done()
# 
# start = time.time()
# def main():
# 
#     #spawn a pool of threads, and pass them queue instance
#     for i in range(5):
#         t = ThreadUrl(queue, out_queue)
#         t.setDaemon(True)
#         t.start()
# 
#     #populate queue with data
#     for host in hosts:
#         queue.put(host)
# 
#     for i in range(5):
#         dt = DatamineThread(out_queue)
#         dt.setDaemon(True)
#         dt.start()
# 
# 
#     #wait on the queue until everything has been processed
#     queue.join()
#     out_queue.join()
# 
# main()
# print "Elapsed Time: %s" % (time.time() - start)