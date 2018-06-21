import os
import psutil
import psycopg2
import smtplib
import time

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, g
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app import db


def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip()))


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


# getting disk and cpu inforamtion
stats = os.statvfs('../../../../../pless_nfs')
free = str(float(stats.f_bfree) / float(stats.f_blocks))
cpu = str(psutil.cpu_percent(interval=1))


# Stuff for actually emailing
fromaddr = "kylerood16@gmail.com"
toaddr = "krood20@gwmail.gwu.edu"
cc0 = "robert.pless@gmail.com"
cc1 = "shahsuraj261@gmail.com"

time.ctime()
curr_time = time.strftime('%b %d, %Y %l:%M%p %Z')

msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
subj = "LOG FOR " + curr_time
msg['Subject'] = subj

body = "LOG FILE FOR " + curr_time + "\nNumber of Cams: " + str(camera_count[0][0]) + "\nNumber of Images total: " + str(
    total_image_count[0][0]) + "\nNumber of Images Captured Today: " + str(image_count[0][0]) + "\nPercent of disk free: " + free + "\nPercent of CPU currently in use: " + cpu
msg.attach(MIMEText(body, 'plain'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "Andreschurrle9")
text = msg.as_string()
server.sendmail(fromaddr, [toaddr, cc0, cc1], text)
server.quit()
exit()
