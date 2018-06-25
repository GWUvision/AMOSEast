from app import db


class Camera(db.Model):
    __tablename__ = 'cameras'

    cameraid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    url = db.Column(db.String())
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    last_width = db.Column(db.Integer)
    last_height = db.Column(db.Integer)
    mhash = db.Column(db.String())

    def __init__(self, name, url, latitude, longitude, last_width, last_height, mhash):
        self.name = name
        self.url = url
        self.latitude = latitude
        self.longitude = longitude
        self.last_width = last_width
        self.last_height = last_height
        self.mhash = mhash

    def __repr__(self):
        return '<image id={},name={}>'.format(self.cameraid, self.name)


class Image(db.Model):
    __tablename__ = 'images'

    rowid = db.Column(db.Integer, primary_key=True)
    filepath = db.Column(db.String())
    curr_time = db.Column(db.DateTime)
    cameraid = db.Column(db.Integer, db.ForeignKey('cameras.cameraid'))

    def __init__(self, filepath, curr_time, cameraid):
        self.filepath = filepath
        self.curr_time = curr_time
        self.cameraid = cameraid

    def __repr__(self):
        return '<image id={}>'.format(self.rowid)


# new class specifically for reviewing submitted cameras
# make sure this is right
class SubmitCam(db.Model):
    __tablename__ = 'submit_cams'

    submitid = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    description = db.Column(db.String())
    curr_time = db.Column(db.DateTime)

    def __init__(self, url, description, curr_time):
        self.url = url
        self.description = description
        self.curr_time = curr_time

    def __repr__(self):
        return '<image id={}>'.format(self.submitid)
