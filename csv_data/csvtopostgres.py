import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
database = psycopg2.connect(DATABASE_URL, sslmode='allow')

cur = database.cursor()
root = '/home/suraj/Documents/GWU/AMOSEast/csv_data/interesting_cams.csv'
path = '/home/suraj/Desktop/interesting_images.csv'
print("Connected to database...")

# psql -c "\copy cameras FROM 'root' delimiter ',' csv header"

try:
    sql = "COPY cameras FROM '%s' DELIMITER ',' CSV HEADER" % (root)
    cur.execute(sql)
    print("Copied data from csv to postgres database...")

    # sql = "COPY images FROM '%s' DELIMITER ',' CSV HEADER" % (path)
    # cur.execute(sql)
    # print("Copied image data...")

except Exception as e:
    print ("Unable to copy data. ", e)


database.commit()
