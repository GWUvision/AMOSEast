import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../pless-goog-vision-45710df949d0.json"

import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.join(os.path.dirname(
    __file__), 'static/images/15/20180506_010011.jpg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations

print('Labels:')
for label in labels:
    # if(label.score > .8):
    print(label.description, label.score)