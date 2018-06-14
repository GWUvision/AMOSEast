import psycopg2
import os
from weather import Weather, Unit



DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require').cursor()
all_cameras_query = "SELECT cameraid, name, url, latitude, longitude FROM cameras ORDER BY cameraid"
conn.execute(all_cameras_query)
all_cameras = conn.fetchall()

print(all_cameras[0][3])
print(all_cameras[0][4])

weather = Weather(unit=Unit.FAHRENHEIT)


for cameras in all_cameras[:2]:
    # print(cameras[3])
    try:
        print(cameras)
        lookup = weather.lookup_by_latlng(cameras[3],cameras[4])
        condition = lookup.condition
        print(condition.temp, condition.text)
    except AttributeError as e:
        print("No latitude/longitude given")
    except KeyError as e:
        print(e)
        
    
    

