import os
import datetime

root = "/home/suraj/Documents/GWU/AMOSEast/flaskapp/static/images"

for path, subdirs, files in os.walk(root):
    for name in files:
        # print(os.path.join(path, name))
        filepath = os.path.join(path, name).split('images/')[1]
        print(filepath)
        name = os.path.splitext(os.path.basename(name))[0]
        cameraid, date, time = name.split('_')
        date = datetime.datetime.strptime(date, '%Y%m%d').date().isoformat()
        # date = '-'.join([date[:4], date[4:6], date[6:]])
        time = ':'.join(a + b for a, b in zip(time[::2], time[1::2]))
        curr_time = date + ' ' + time
        print(cameraid, curr_time, filepath)
