from flask import Flask, render_template, request, redirect, url_for, g
from pager import Pager
# import sqlite3
import datetime


STATIC_FOLDER = 'static'
APPNAME = 'AMOS East'

app = Flask(__name__, static_folder=STATIC_FOLDER)
app.config.update(APPNAME=APPNAME,)

@app.route('/')
def homepage():
    
    camera_count = 10
    return render_template('home.html', camera_count=camera_count)

if __name__ == '__main__':
    app.run(debug=True)
