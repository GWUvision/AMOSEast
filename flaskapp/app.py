# ---- importing libraries to connect with database and flask and other necessary packages -----

import psycopg2
import datetime
import os
import numpy as np
import urllib.request
from urllib.error import URLError, HTTPError
import validators
from sqlalchemy import engine

from flask import Flask, render_template, request, redirect, url_for, g, flash
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from pager import Pager
from weather import Weather, Unit
from gmplot import gmplot

import time

#for classifier
import requests
import shutil
from flask_uploads import UploadSet, configure_uploads, IMAGES
import test_network
import imghdr


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

# DATABASE_URL = os.environ['DATABASE_URL']
# conn = psycopg2.connect(DATABASE_URL, sslmode='allow').cursor()
# all_cameras_query = "SELECT cameraid, name, url, latitude, longitude FROM cameras ORDER BY cameraid"
# conn.execute(all_cameras_query)
# all_cameras = conn.fetchall()

# # make the map page
# lng = np.array(all_cameras)[:, 4]
# lat = np.array(all_cameras)[:, 3]
#
#
# # Place map
# gmap = gmplot.GoogleMapPlotter(0, 0, 13)
#
# for i in range(0, len(lng)):
#     lt, ln = lat[i], lng[i]
#     if(lt == 0 and ln == 0):
#         continue
#     else:
#         # add marker to map
#         gmap.marker(lt, ln, 'red')

# Draw
# gmap.draw("map.html")
# move to templates
# os.rename("/pless_nfs/home/krood20/AMOSEast/flaskapp/map.html", "/pless_nfs/home/krood20/AMOSEast/flaskapp/templates/map.html")

#functions to get the prev and next cams
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
def directory_view(ind=1):

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
        previd = 1

    if(next == 'None'):
        next = db.engine.execute('SELECT * FROM cameras ORDER BY cameraid DESC LIMIT 1').first()
        nextid = next.cameraid
    else:
        nextid = next.cameraid

    try:

        if ind >= count:
            return redirect(url_for(homepage))
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
            return redirect('/cameras/1')
        else:
            results = Camera.query.filter(Camera.name.ilike(
                '%{0}%'.format(request.form['search']))).all()
            print(results)

            # search_query = "SELECT cameraid FROM cameras WHERE name LIKE {0}".format("%" + str(request.form['search']) + "%")
            # conn.execute(search_query)
            # data2 = conn.fetchall()
            # print(data2)

            return redirect('/cameras/1')


@app.route('/about')
def aboutpage():
    return render_template('about.html')


@app.route('/history')
def historypage():
    return render_template('history.html')


@app.route('/map')
def mappage():
    # need to make sure the api key is on the bottom of the file
    return render_template('map.html')


@app.route('/coolcams')
def allcamspage():


    # camera_count = db.engine.execute('select count(cameraid) from cameras').scalar()
    # cool_cams_list = [i for i in range(camera_count)]


    cool_cams_list = [2, 4, 5, 8, 10, 11, 13, 15, 16]
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
                print('here')
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

#For the clssifier
@app.route('/classifier/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])

        cwd = os.getcwd()
        session['filepath'] = cwd + "/static/" + filename

        return redirect(url_for('result'))

        # return render_template('upload.html', filename=filename, results=results)

    return render_template('upload.html')

@app.route('/classifier/result', methods=['GET', 'POST'])
def result():

    path = '256_ObjectCategories'
    categories = {}
    for root, dirs, files in os.walk(path, topdown=False):
        for name in dirs:
            categories[name.split('.')[0]] = name.split('.')[-1]

    print(categories)
    output = test_network.test_network_classifier(str(session['filepath']), 'example_model')

    # print(str(output).zfill(3))

    result = categories[str(output).zfill(3)]

    # print(categories[str(output)])

    return render_template('result.html', result=result)



@app.route('/classifier')
def index():
    flash('Please enter a word!')
    return render_template('index.html')


@app.route('/classifier', methods=['POST'])
def index_post():

    if request.form['name'] is not None:
        begin = time.time()

        user_word = request.form['name']
        user_word = user_word.replace(" ", "-")
        print("Creating Directory")
        directory = '256_ObjectCategories/258.{0}/'.format(user_word)

        os.makedirs(
            '256_ObjectCategories/258.{0}/'.format(user_word), exist_ok=True)

        # grab urls
        #chromedriver is for mac, chromedriver2 is for linux
        cwd = os.getcwd()
        command = "python ../classifier_files/google_images_download.py --keywords " + user_word + \
            " --limit 200 --chromedriver '{0}/../classifier_files/chromedriver2'".format(cwd)

        os.system(command)

        # download images
        command = "python ../classifier_files/imagedownload.py " + user_word
        os.system(command)

        #check that the images are good
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            filetype = str(imghdr.what(directory + filename))
            if(filetype != 'png' or filetype != 'jpeg'):
                print(filetype)
                os.remove(directory + filename)


        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            filetype = imghdr.what(directory + filename)
            print(filetype)

        # train network
        command = "python ../classifier_files/train_network.py"
        os.system(command)

        # reset the stuff
        # print("Deleting Directory...")
        # shutil.rmtree('256_ObjectCategories/258.{0}/'.format(user_word))
        # os.remove("output.csv")

        # timing
        end = time.time()
        print('Total time: ', end - begin)

        return redirect(url_for('upload'))

    elif request.form['name'] is None:
        flash('Please enter a word!')
        return redirect(url_for('index'))



@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
