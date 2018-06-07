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

# def get_image(the_id):
#     # return Image.query.filter(Image.id == the_id).first()
#     return Image.query.get_or_404(the_id)
#
#
# def get_images(params=None):
#     if not params:
#         return Image.query.all()
#     else:
#         raise Exception('Filtering not implemented yet.')
#
#
# def add_image(camera_dict):
#     new_image = Camera(name=camera_dict['name'],
#                         url=camera_dict['url'],
#                         latitude=camera_dict['latitude'],
#                         longitude=camera_dict['longitude'],
#                         last_width=camera_dict['last_width'],
#                         last_height=camera_dict['last_height'])
#
#     db.session.add(new_image)
#     db.session.commit()
