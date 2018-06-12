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

import os
import urllib.request
 
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
 
 
def downloader(url):
    """
    Downloads the specified URL and saves it to disk
    """
    req = urllib.request.urlopen(url)
    filename = os.path.basename(url)
    ext = os.path.splitext(url)[1]
    if not ext:
        raise RuntimeError('URL does not contain an extension')
 
        
    with open(filename, 'wb') as file_handle:
        # while True:
        chunk = req.read()
        # if not chunk:
        #     break
        file_handle.write(chunk)
        msg = 'Finished downloading {filename}'.format(filename=filename)
    print(msg)
    
    
 
 
def main(urls):
    """
    Create a thread pool and download specified urls
    """
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        return executor.map(downloader, urls, timeout=2)



 
if __name__ == '__main__':
    results = main(urls)
    for result in results:
        print(result)






