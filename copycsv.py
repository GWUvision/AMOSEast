# import psycopg2
#
# conn = psycopg2.connect("host=localhost dbname=kylerood user=kylerood")
# cur = conn.cursor()
# with open('data2.csv', 'r') as f:
#     # Notice that we don't need the `csv` module.
#     next(f)  # Skip the header row.
#     cur.copy_from(f, 'cameras', sep=',')
# 
# conn.commit()
# conn.close()



import psycopg2

#DATABASE_URL = os.environ['DATABASE_URL']

try:
    conn = psycopg2.connect(host='localhost', database='kylerood', user='kylerood',  password='')
    print("I am here")

    cur = conn.cursor()

    try:
        cur.execute("""COPY cameras(cameraid, name, url, latitude, longitude, last_width, last_height)
                FROM '/Users/kylerood/AMOSEast/restapi_info/data2.csv' DELIMITER ',' CSV HEADER """)
        print("hello there")
    except:
        print ("COPY failed")

except:
    print ("I am unable to connect to the database")

finally:
        if conn is not None:
            conn.close()
