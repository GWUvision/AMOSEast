import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
database = psycopg2.connect(DATABASE_URL, sslmode='allow')

cur = database.cursor()
root = 'csv_data/data2.csv'

print("Connected to database...")

# psql -c "\copy cameras FROM 'root' delimiter ',' csv header"

try:
    sql = "COPY cameras(cameraid, name, url, latitude, longitude, last_width, last_height) FROM '%s' DELIMITER ',' CSV HEADER" % (root)
    cur.execute(sql)
    print("Copied data from csv to postgres database...")

except Exception as e:
    print ("Unable to copy data. ", e)


database.commit()
