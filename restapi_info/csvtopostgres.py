import os
import psycopg2


def copied():

    DATABASE_URL = os.environ['DATABASE_URL']
    database = psycopg2.connect(DATABASE_URL, sslmode='require')

    cur = database.cursor()

    print("Connected to database...")

    try:
        cur.execute("""COPY cameras(cameraid, name, url, latitude, longitude, last_width, last_height)
                FROM '/home/suraj/Documents/GWU/AMOSEast/restapi_info/data2.csv' DELIMITER ',' CSV HEADER """)
        print("Copied data from csv to postgres database...")

    except:
        print ("Unable to copy data...")

    database.commit()


copied()
