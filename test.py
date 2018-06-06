import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
database = psycopg2.connect(DATABASE_URL, sslmode='require')

cur = database.cursor()

try:
    cur.execute("""COPY cameras(cameraid, name, url, latitude, longitude, last_width, last_height)
            FROM '/home/suraj/Documents/GWU/AMOSEast/restapi_info/data.csv' DELIMITER ',' CSV HEADER """)
    print("hello there")
    
except:
    print ("COPY failed")
    
    
database.commit()