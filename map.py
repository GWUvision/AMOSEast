import sqlite3

DATABASE = 'allimages.db'
db = sqlite3.connect(DATABASE)
conn = db.cursor()
all_cameras = "SELECT latitude, longitude FROM image_info"
conn.execute(all_cameras)
data = conn.fetchall()

print(data[0])

