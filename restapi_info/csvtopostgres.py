import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
database = psycopg2.connect(DATABASE_URL, sslmode='require')

cur = database.cursor()

print("Connected to database...")

try:
    cur.execute("""COPY cameras(cameraid, name, url, latitude, longitude, last_width, last_height)
            FROM '/pless_nfs/home/suraj98/AMOSEast/restapi_info/data3.csv' DELIMITER ',' CSV HEADER """)
    print("Copied data from csv to postgres database...")

    # psql -c "\copy cameras FROM '/pless_nfs/home/suraj98/AMOSEast/restapi_info/data2.csv' delimiter ',' csv header"


except Exception as e:
    print ("Unable to copy data...")
    print(e)


database.commit()
