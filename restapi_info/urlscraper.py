import eventlet
import json
import requests
import sqlite3
import urllib.request
from socket import timeout

from bs4 import BeautifulSoup
from urllib.parse import urlparse

db = sqlite3.connect('pless.db')
conn = db.cursor()
eventlet.monkey_patch()

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

# from page 1 to 70
url = 'http://amos.cse.wustl.edu/REST/webcams/?page=1&format=json'


class URLExtractor(object):

    def __init__(self, url):
        self.url = url

    def get_status_code(self, url):
        try:
            with eventlet.timeout.Timeout(1):
                response = requests.get(url)
                return response.status_code
        except requests.exceptions.ReadTimeout:
            print("READ TIMED OUT -", url)
        except requests.exceptions.ConnectionError:
            print("CONNECT ERROR -", url)
        except eventlet.timeout.Timeout:
            print("TOTAL TIMEOUT -", url)
        except requests.exceptions.RequestException:
            print("OTHER REQUESTS EXCEPTION -", url)

    def info_extractor(self):

        info = []
        # use a with loop and open the url
        with urllib.request.urlopen(self.url) as url:
            # get the json data and read it
            data = json.loads(url.read().decode())
            for entry in data['results']:
                for index, key in entry.items():
                    value = entry[key]
                    if(key == 'url'):
                        # if the key is the url, check the status code
                        if(self.get_status_code(value) == 200):

                            print("Camera #%d works. Adding to list..." %
                                  entry['id'])

                            query = 'INSERT INTO image_info(cameraID, name, url, latitude, longitude, last_width, last_height) VALUES (?, ?, ?, ?, ?, ?, ?)'

                            conn.execute(query, (index+1, entry['title'], value, entry['latitude'], entry['longitude'], entry['last_width'], entry['last_height']))

                            db.commit()