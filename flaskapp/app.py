# ---- importing libraries to connect with database and flask and other necessary packages -----

import psycopg2
import datetime
import os
import urllib.request
from urllib.error import URLError, HTTPError
import validators
from sqlalchemy import engine

from flask import Flask, render_template, request, redirect, url_for, g, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from pager import Pager
# from weather import Weather, Unit

# --- initial app configuation and initialization such as where images are located and setting database url

STATIC_FOLDER = 'static'
APPNAME = 'AMOS'

app = Flask(__name__, static_folder=STATIC_FOLDER)
app.config.update(APPNAME=APPNAME,)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# photos = UploadSet('photos', IMAGES)
# app.config['UPLOADED_PHOTOS_DEST'] = 'static/'
# configure_uploads(app, photos)

moment = Moment(app)
db = SQLAlchemy(app)

from models import *

# ---- connected to database initially

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='allow').cursor()
all_cameras_query = "SELECT cameraid, name, url, latitude, longitude FROM cameras ORDER BY cameraid"
conn.execute(all_cameras_query)
all_cameras = conn.fetchall()

# functions to get the prev and next cams
def prev_cam(cid):
    count = db.engine.execute(
        'select count(cameraid) from cameras').scalar()
    while (count > 0):
        prev_cam = None
        cid = cid - 1
        if db.session.query(Camera).get(cid) is not None:
            prev_cam = db.session.query(Camera).get(cid)
            break
        else:
            count = count - 1
    return prev_cam

def next_cam(cid):
    count = db.engine.execute(
        'select count(cameraid) from cameras').scalar()
    while (count > 0):
        next_cam = None
        cid = cid + 1
        if db.session.query(Camera).get(cid) is not None:
            next_cam = db.session.query(Camera).get(cid)
            break
        else:
            count = count - 1
    return next_cam


@app.route('/')
def homepage():

    camera_count = db.engine.execute(
        'select count(cameraid) from cameras').scalar()

    image_count = db.engine.execute(
        'select count(cameraid) from images').scalar()

    return render_template('home.html', camera_count="{:,}".format(camera_count), image_count="{:,}".format(image_count))


@app.route('/cameras/<int:ind>/')
def directory_view(ind=19):

    images = Image.query.filter_by(
        cameraid=ind).order_by(Image.curr_time.desc()).first()
    results = Camera.query.filter_by(cameraid=ind).first()
    count = db.engine.execute('select count(cameraid) from cameras').scalar()

    next = next_cam(ind)
    prev = prev_cam(ind)

    #error checking for next and prev
    if(prev):
        previd = prev.cameraid
    else:
        previd = 19

    if(next == 'None'):
        next = db.engine.execute('SELECT * FROM cameras ORDER BY cameraid DESC LIMIT 1').first()
        nextid = next.cameraid
    else:
        nextid = next.cameraid

    try:

        if ind >= count:
            return redirect(url_for('homepage'))
        else:
            current = ind
            try:

                lng = results.longitude
                lat = results.latitude

                weather = Weather(unit=Unit.FAHRENHEIT)

                lookup = weather.lookup_by_latlng(
                    results.__dict__['latitude'], results.__dict__['longitude'])
                condition = lookup.condition
                temp = condition.temp + \
                    '\N{DEGREE SIGN}F and ' + condition.text

            except:
                temp = 'No weather available'
                lng = 0
                lat = 0

            print(current)
            if(current == 1):
                current = 19

            return render_template('dirview.html', index=ind, results=results, images=images, weather=temp, lng=lng, lat=lat, next=nextid, prev=previd, current=current)

    except AttributeError as e:
        # flash('')
        print(e)
        return redirect(url_for('homepage'))


@app.route('/cameras/<int:ind>/<int:ind2>/')
def image_view(ind=None, ind2=None):

    pager = Pager(db.engine.execute(
        'select count(cameraid) from cameras').scalar())

    data = Camera.query.filter_by(cameraid=ind).first()

    images = Image.query.filter_by(
        cameraid=ind).order_by(Image.curr_time.asc()).all()

    pager2 = Pager(len(images))

    try:

        if ind2 >= pager2.count or ind >= pager.count:
            flash('Image did not exist')
            return render_template('dirview.html', index=ind, pager=pager)
        else:
            pager.current = ind
            pager2.current = ind2

            return render_template('imageview.html', index=ind2, pager=pager, pager2=pager2, data2=images[ind2], data=data)

    except IndexError as e:
        return render_template('404.html')


@app.route('/goto', methods=['POST', 'GET'])
def goto():

    if request.method == 'POST':
        if not request.form['search']:
            return redirect('/cameras/19')
        else:
            results = Camera.query.filter(Camera.name.ilike(
                '%{0}%'.format(request.form['search']))).all()
            print(results)

            search_query = "SELECT cameraid FROM cameras WHERE name LIKE {0}".format("%" + str(request.form['search']) + "%")
            conn.execute(search_query)
            data2 = conn.fetchall()
            print(data2)

            return redirect('/cameras/19')


@app.route('/about')
def aboutpage():
    return render_template('about.html')


@app.route('/history')
def historypage():
    return render_template('history.html')


@app.route('/camera_map')
def mappage():
    # need to make sure the api key is on the bottom of the file
    return render_template('camera_map.html')


@app.route('/coolcams')
def allcamspage():

    cool_cams_list = [19, 64, 73, 75, 108, 120, 124, 161, 165, 6767, 7990, 7539]
    # sqlalchemy queries
    cams = [Image.query.filter_by(cameraid=id).order_by(
        Image.curr_time.desc()).first() for id in cool_cams_list]

    camera_name = [Camera.query.filter_by(
        cameraid=id).first() for id in cool_cams_list]

    cameras = list(zip(cams, camera_name))

    # index off by one error subtraction
    for camera in cameras:
        camera[0].__dict__['cameraid'] = camera[0].__dict__['cameraid'] - 1

    return render_template('coolcams.html', cameras=cameras)


@app.route('/submitcam', methods=['POST', 'GET'])
def submitcam():
    error = None
    if request.method == 'POST':
        # get the url and description from the html
        url = request.form['url']

        description = request.form['message']
        curr_time = datetime.datetime.now()
        name = request.form['name']
        lat = request.form['latitude']
        lng = request.form['longitude']

        # connect to the database
        conn = psycopg2.connect(DATABASE_URL, sslmode='allow')
        cur = conn.cursor()

        # check if it is a url first using validators
        if(validators.url(url)):
            # error checking the url
            try:
                code = urllib.request.urlopen(url).code

                # query the database --> usually in the else
                query = "INSERT INTO submit_cams(url, description, curr_time, latitude, longitude) VALUES('%s','%s','%s','%s','%s')" % (
                    url, description, curr_time, lat, lng)
                cur.execute(query)
                conn.commit()
            except HTTPError as e:
                print('Error code: ', e.code)
                error = 'Error code: ', e.code
            except URLError as e:
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
