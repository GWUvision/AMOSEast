# ---- importing libraries to connect with database and flask and other necessary packages -----

import psycopg2
import datetime
import os
from os.path import isfile, join, exists
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

# functions to get the prev and next cams
def prev_cam(cid):
    count = db.engine.execute(
        'select count(cameraid) from cameras').scalar()
    while (count > 0):
        prev_cam = None
        cid = cid - 1
        if db.session.query(Camera).get(cid) is not None and (exists("./static/images/" + str(cid)) or exists("./static/images/" + str(cid).zfill(8))):#adding check to make sure folder exists
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
        if db.session.query(Camera).get(cid) is not None and (exists("./static/images/" + str(cid)) or exists("./static/images/" + str(cid).zfill(8))): #adding check to make sure folder exists
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

    #image metadata
    image_meta = Image.query.filter_by(cameraid=ind).order_by(Image.curr_time.desc()).first()
    results = Camera.query.filter_by(cameraid=ind).first()
    count = db.engine.execute('select count(cameraid) from cameras').scalar()

    #need to get filepath --> 19/19_20180625_132516.jpg
    main_path = "./static/images/" + str(ind).zfill(8)

    #accounts for fact many palces dont have zfilled folder
    if(not exists(main_path)):
        #skips over all indexs that arent zfilled
        while(not exists("./static/images/" + str(ind).zfill(8))):
            ind = next_cam(ind).cameraid
        # main_path = "./static/images/" + str(ind) #this will get cams that are not zfilled

    all_files = [f for f in os.listdir(main_path) if isfile(join(main_path, f))]
    first_file = all_files[0]
    filepath = str(ind).zfill(8) + "/" + first_file

    next = next_cam(ind)
    prev = prev_cam(ind)

    print("Next cam: " + str(next))
    print("Prev cam: " + str(prev))

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

            return render_template('dirview.html', index=ind, results=results,image_meta=image_meta,
                                    weather=temp, lng=lng,lat=lat, next=nextid, prev=previd,
                                    current=str(current).zfill(8), filepath=filepath)

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

    #new way
    #need to get filepath --> 19/19_20180625_132516.jpg
    main_path = "./static/images/" + str(ind).zfill(8)
    all_files = [f for f in os.listdir(main_path) if isfile(join(main_path, f))]
    print("File list:")
    print(all_files[:5])

    try:

        if ind2 >= pager2.count or ind >= pager.count:
            flash('Image did not exist')
            return render_template('dirview.html', index=ind, pager=pager)
        else:
            pager.current = ind
            pager2.current = ind2
            filepath = str(ind).zfill(8) + "/" + all_files[ind2] #getting the next image
            print("Indexs: " + str(ind) + " " + str(ind2))
            print("Filepath: " + filepath)

            return render_template('imageview.html', index=ind2, pager=pager, pager2=pager2, data2=images[ind2], data=data, filepath=filepath)

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


@app.route('/projectparticipants')
def aboutpage():
    return render_template('projectparticipants.html')


@app.route('/aboutAMOS')
def historypage():
    return render_template('aboutAMOS.html')


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

@app.route('/datasetaccess')
def datasetaccess():
     return render_template('datasetaccess.html')

@app.route('/overviewofimages')
def overviewofimages():
     return render_template('overviewofimages.html')

@app.route('/overviewofimages2')
def overviewofimages2():
     return render_template('overviewofimages2.html')

@app.route('/overviewofimages3')
def overviewofimages3():
     return render_template('overviewofimages3.html')

@app.route('/overviewofimages4')
def overviewofimages4():
     return render_template('overviewofimages4.html')

@app.route('/overviewofimages5')
def overviewofimages5():
     return render_template('overviewofimages5.html')

@app.route('/overviewofimages6')
def overviewofimages6():
     return render_template('overviewofimages6.html')

@app.route('/overviewofimages7')
def overviewofimages7():
     return render_template('overviewofimages7.html')

@app.route('/overviewofimages8')
def overviewofimages8():
     return render_template('overviewofimages8.html')

@app.route('/overviewofimages9')
def overviewofimages9():
     return render_template('overviewofimages9.html')

@app.route('/overviewofimages10')
def overviewofimages10():
     return render_template('overviewofimages10.html')

@app.route('/publications')
def moreinfo():
    return render_template('publications.html')

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True, ssl_context=('./ssl_info/amostest_seas_gwu_edu_cert.cer', './ssl_info/amostest.seas.gwu.edu.key'), port=443)
