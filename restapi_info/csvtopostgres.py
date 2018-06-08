import os
import psycopg2

<<<<<<< HEAD
DATABASE_URL = os.environ['DATABASE_URL']
database = psycopg2.connect(DATABASE_URL, sslmode='require')
=======
>>>>>>> 6a744b9fcb4d3239dc104eca6b566347cf971660

def copied():

    DATABASE_URL = os.environ['DATABASE_URL']
    database = psycopg2.connect(DATABASE_URL, sslmode='require')

<<<<<<< HEAD
try:
    cur.execute("""COPY cameras(cameraid, name, url, latitude, longitude, last_width, last_height)
            FROM '/pless_nfs/home/krood20/AMOSEast/restapi_info/data2.csv' DELIMITER ',' CSV HEADER """)
    print("Copied data from csv to postgres database...")

except:
    print ("Unable to copy data...")


database.commit()
=======
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
>>>>>>> 6a744b9fcb4d3239dc104eca6b566347cf971660
