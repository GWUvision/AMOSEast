import psycopg2
import datetime
import os

from flask import Flask, render_template, request, redirect, url_for, g
from pager import Pager
from flask_sqlalchemy import SQLAlchemy


STATIC_FOLDER = 'static'
APPNAME = 'AMOS East'

app = Flask(__name__, static_folder=STATIC_FOLDER)
app.config.update(APPNAME=APPNAME,)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

#DATABASE_URL = os.environ['DATABASE_URL']
# database = psycopg2.connect(DATABASE_URL, sslmode='require')

# all_cameras = "SELECT cameraID, name, url, latitude, longitude FROM image_info"
# conn.execute(all_cameras)
# data = conn.fetchall()
# pager = Pager(len(data))
#


# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = psycopg2.connect(DATABASE_URL, sslmode='require')
#     return db


@app.route('/')
def homepage():

    conn = get_db().cursor()
    count = "SELECT count(*) from cameras"
    conn.execute(count)
    data3 = conn.fetchone()

    camera_count = data3[0]
    camera_count = '{:,}'.format(camera_count)
    return render_template('home.html', camera_count=camera_count)


# @app.route('/cameras/<int:ind>/')
# def directory_view(ind=None):
#     conn = get_db().cursor()
#
#     query2 = "SELECT filepath, curr_time from all_images WHERE cameraID=%d" %(data[ind][0])
#     conn.execute(query2)
#     data2 = conn.fetchall()
#
#     if ind >= pager.count:
#         return render_template("404.html"), 404
#     else:
#         pager.current = ind
#         return render_template('dirview.html', index=ind, pager=pager, data=data[ind], data2=data2[-1])
#
#
# @app.route('/cameras/<int:ind>/<int:ind2>/')
# def image_view(ind=None, ind2=None):
#
#     conn = get_db().cursor()
#     query2 = "SELECT filepath, curr_time from all_images WHERE cameraID=%d" % (
#         pager.current)
#     conn.execute(query2)
#     data2 = conn.fetchall()
#     pager2 = Pager(len(data2))
#
#     if ind2 >= pager2.count or ind >= pager.count:
#         return render_template("404.html"), 404
#     else:
#         pager.current = ind
#         pager2.current = ind2
#         return render_template('imageview.html', index=ind2, pager=pager, pager2=pager2, data2=data2[ind2], data=data[ind])
#
#
# @app.route('/goto', methods=['POST', 'GET'])
# def goto():
#     return redirect('/cameras/' + request.form['index'])
#
#
# @app.route('/about')
# def aboutpage():
#     return render_template('about.html')
#
# @app.route('/map')
# def mappage():
#     # implement google map api functionality here
#     return render_template('map.html')
#
# @app.route('/submitcam')
# def sumbitcam():
#     return render_template('submitcam.html')
#
# @app.route('/moreinfo')
# def moreinfo():
#     return render_template('moreinfo.html')


# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()


if __name__ == '__main__':
    app.run(debug=True)
