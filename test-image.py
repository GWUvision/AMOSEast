import os

root = "/home/suraj/Documents/GWU/AMOSEast/flaskapp/static/images"

for path, subdirs, files in os.walk(root):
    for name in files:
        print(os.path.join(path, name))
        print(name)
        # print(os.path.splitext(os.path.basename(name)))
        index, date, time = name.split('_')
        print(index, date, time)
        