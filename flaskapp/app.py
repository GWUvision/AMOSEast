# ---- importing libraries to connect with database and flask and other necessary packages -----

import psycopg2
import datetime
import os
import numpy as np
import urllib.request
from urllib.error import URLError, HTTPError
import validators

from flask import Flask, render_template, request, redirect, url_for, g, flash
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from pager import Pager
from weather import Weather, Unit

import time


# --- initial app configuation and initialization such as where images are located and setting database url

STATIC_FOLDER = 'static'
APPNAME = 'AMOS'

app = Flask(__name__, static_folder=STATIC_FOLDER)
app.config.update(APPNAME=APPNAME,)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

moment = Moment(app)
db = SQLAlchemy(app)

from models import *


# ---- connected to database initially

begin1 = time.time()

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='allow').cursor()
all_cameras_query = "SELECT cameraid, name, url, latitude, longitude FROM cameras ORDER BY cameraid"
conn.execute(all_cameras_query)
all_cameras = conn.fetchall()
pager = Pager(len(all_cameras))

end1 = time.time()

print('First Time: ', end1-begin1)

begin2 = time.time()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = psycopg2.connect(DATABASE_URL, sslmode='allow')
        return db
end2 = time.time()

print("Second time: ", end2-begin2)

begin3 = time.time()

@app.route('/')
def homepage():

    conn = get_db().cursor()
    sql1 = "SELECT count(*) FROM cameras"
    conn.execute(sql1)
    camera_count = conn.fetchone()[0]
    camera_count = '{:,}'.format(camera_count)

    sql2 = "SELECT count(*) FROM images"
    conn.execute(sql2)
    image_count = conn.fetchone()[0]
    image_count = '{:,}'.format(image_count)

    return render_template('home.html', camera_count=camera_count, image_count=image_count)
end3 = time.time()

print("Third time: ", end3-begin3)



begin4 = time.time()

@app.route('/cameras/<int:ind>/')
def directory_view(ind=1):
    conn = get_db().cursor()

    camera_images_query = "SELECT filepath, curr_time from images WHERE cameraid=%d ORDER BY curr_time ASC" % (
        all_cameras[ind][0])

    conn.execute(camera_images_query)
    camera_images = conn.fetchall()
    
    lng = np.array(all_cameras)[:, 4]
    lat = np.array(all_cameras)[:, 3]

    try:

        if ind >= pager.count:
            return render_template("404.html"), 404
        else:
            pager.current = ind

            try:

                weather = Weather(unit=Unit.FAHRENHEIT)

                lookup = weather.lookup_by_latlng(
                    all_cameras[ind][3], all_cameras[ind][4])
                condition = lookup.condition
                w_info = [condition.temp +
                          '\N{DEGREE SIGN}F and ' + condition.text]

            except AttributeError as e:
                w_info = ['No weather information available']
                return render_template('dirview.html', index=ind, pager=pager, data=all_cameras[ind], data2=camera_images[-1], weather=w_info, lg=lng, lt=lat)

            except KeyError as e:
                w_info = ['No weather information available']
                return render_template('dirview.html', index=ind, pager=pager, data=all_cameras[ind], data2=camera_images[-1], weather=w_info, lg=lng, lt=lat)

            except UnboundLocalError as e:
                w_info = ['No weather information available']
                return render_template('dirview.html', index=ind, pager=pager, data=all_cameras[ind], data2=camera_images[-1], weather=w_info, lg=lng, lt=lat)

            return render_template('dirview.html', index=ind, pager=pager, data=all_cameras[ind], data2=camera_images[-1], weather=w_info, lg=lng, lt=lat)

    except IndexError as e:
        return render_template('404.html'), 404

end4 = time.time()

print("Fourth time: ", end4-begin4)


begin5 = time.time()


@app.route('/cameras/<int:ind>/<int:ind2>/')
def image_view(ind=None, ind2=None):

    conn = get_db().cursor()
    camera_images_query = "SELECT filepath, curr_time from images WHERE cameraid=%d ORDER BY curr_time ASC" % (
        all_cameras[ind][0])
    conn.execute(camera_images_query)
    data2 = conn.fetchall()
    pager2 = Pager(len(data2))

    try:

        if ind2 >= pager2.count or ind >= pager.count:
            return render_template("404.html"), 404
        else:
            pager.current = ind
            pager2.current = ind2

            return render_template('imageview.html', index=ind2, pager=pager, pager2=pager2, data2=data2[ind2], data=all_cameras[ind])

    except IndexError as e:
        return render_template('404.html'), 404

end5 = time.time()

print("Five time: ", end5-begin5)


@app.route('/goto', methods=['POST', 'GET'])
def goto():

    if request.method == 'POST':
        if not request.form['index']:
            return redirect('/cameras/0')
        else:
            return redirect('/cameras/' + request.form['index'])


@app.route('/about')
def aboutpage():
    return render_template('about.html')


@app.route('/history')
def historypage():
    return render_template('history.html')


@app.route('/map')
def mappage():
    lng = np.array(all_cameras)[:, 4]
    lat = np.array(all_cameras)[:, 3]

    return render_template('map.html', lg=lng, lt=lat)


@app.route('/coolcams')
def allcamspage():

    conn = get_db().cursor()

    # change ONLY this list to get the coolest cameras
    # cool_cams_list = [1, 2, 5, 2501, 2503, 2512, 2514, 4038, 4053, 4077, 9, 3]
    cool_cams_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    list_for_webpage = []

    for cameraid in cool_cams_list:
        current_image_query = "SELECT filepath from images where cameraid=%d ORDER BY curr_time DESC" % (
            cameraid)
        conn.execute(current_image_query)
        current_image = conn.fetchone()[0]

        # index subtract by 1 because all_cams starts at 0 while the camera list starts at 1; getting the name for each camera
        camera_name = all_cameras[cameraid - 1][1]
        cameraid_website = cameraid - 1
        list_for_webpage.append([current_image, camera_name, cameraid_website])

    return render_template('coolcams.html', data=list_for_webpage)


@app.route('/submitcam', methods=['POST', 'GET'])
def submitcam():
    error = None
    if request.method == 'POST':
        # get the url and description from the html
        url = request.form['url']
        print(url)
        description = request.form['message']
        curr_time = datetime.datetime.now()
        name = request.form['name']
        lat = request.form['latitude']
        long = request.form['longitude']

        print(url, name, curr_time)

        # connect to the database
        conn = get_db()
        cur = conn.cursor()

        #check if it is a url first using validators
        if(validators.url(url)):
            # error checking the url
            try:
                print('here')
                code = urllib.request.urlopen(url).code

                # query the database --> usually in the else
                query = "INSERT INTO submit_cams(url, description, curr_time, latitude, longitude) VALUES('%s','%s','%s','%s','%s')" % (url, description, curr_time, lat, long)
                cur.execute(query)
                conn.commit()
            except HTTPError as e:
                print('Error code: ', e.code)
                error = 'Error code: ', e.code
            except URLError as e:
                # do something (set req to blank)
                print('Reason: ', e.reason)
                error = 'Reason: ', e.reason
        else:
            flash('Not a valid url.')

    return render_template('submitcam.html', error=error)


@app.route('/moreinfo')
def moreinfo():
    return render_template('moreinfo.html')


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
