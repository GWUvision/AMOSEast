import threading
import os
import psycopg2

# def worker():
#     """thread worker function"""
#     print('Worker')
#     return
#
# threads = []
# for i in range(10000):
#     t = threading.Thread(target=worker)
#     threads.append(t)
#     t.start()
#
# for i in range(10000):
#     worker()

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

urls = [urls.replace('http://', '') for w in words]

# 
# from gevent import monkey; monkey.patch_all()
# from time import time
# import requests
# from PIL import Image
# from io import BytesIO
# import os
# import urlparse
# from gevent.pool import Pool
# 
# def download(url):
#     try:
#         response = session.get(url)
#     except Exception as e:
#         print(e)
#     else:
#         if response.status_code == requests.codes.ok:
#             # file_name = urlparse(url).path.rsplit('/',1)[-1]
#             file_name = "hello"
#             return (response.content)
#         response.raise_for_status()
# 
# def process(img):
#     if img is None:
#         return None
#     # img, name = img
#     img = Image.open(BytesIO(img))
#     path = os.path.join(base_folder, "Hello")
#     try:
#         img.save(path)
#     except Exception as e:
#         print(e)
#     else:
#         return True
# 
# def run(urls):        
#     consumer.map(process, producer.imap_unordered(download, urls))
# 
# if __name__ == '__main__':
#         POOL_SIZE = 300
#         producer = Pool(POOL_SIZE)
#         consumer = Pool(POOL_SIZE)
# 
#         session = requests.Session()
#         http_adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
#         session.mount('http://', http_adapter)
# 
#         test_urls = urls
#         base_folder = 'download_temp'
#         t1 = time()
#         run(test_urls)
#         print(time() - t1)  