import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, render_template, request, redirect, url_for, g
import psycopg2

from app import db

# Get the camera and image counts from the database
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='allow').cursor()
all_cameras_query = "SELECT COUNT(*) FROM cameras"
conn.execute(all_cameras_query)
camera_count = conn.fetchall()

all_cameras_query = "SELECT COUNT(*) FROM images"
conn.execute(all_cameras_query)
total_image_count = conn.fetchall()

all_cameras_query = "SELECT COUNT(*) FROM images WHERE Date(curr_time) = '" + \
    str(datetime.today().strftime('%Y-%m-%d')) + "'"
conn.execute(all_cameras_query)
image_count = conn.fetchall()

#disk space available
#cpu load--> processing
stats = os.statvfs('../../../pless_nfs')
print(stats.f_blocks)
print(stats.f_bfree)

free = str(float(stats.f_bfree)/float(stats.f_blocks))
print("Percent free = " + free)


# Stuff for actually emailing
# fromaddr = "kylerood16@gmail.com"
# toaddr = "krood20@gwmail.gwu.edu"
# cc0 = "robert.pless@gmail.com"
# cc1 = "shahsuraj261@gmail.com"
#
# msg = MIMEMultipart()
# msg['From'] = fromaddr
# msg['To'] = toaddr
# msg['Cc'] = cc
# subj = "LOG FOR " + str(datetime.now())
# msg['Subject'] = subj
#
# body = "LOG FILE FOR " + str(datetime.now()) + "\nNumber of Cams: " + str(camera_count[0][0]) + "\nNumber of Images total: " + str(total_image_count[0][0]) + "\nNumber of Images Captured Today: " + str(image_count[0][0])
# msg.attach(MIMEText(body, 'plain'))
#
# server = smtplib.SMTP('smtp.gmail.com', 587)
# server.starttls()
# server.login(fromaddr, "Andreschurrle9")
# text = msg.as_string()
# server.sendmail(fromaddr, [toaddr, cc0, cc1], text)
# server.quit()
# exit()
