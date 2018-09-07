import json
import requests
import urllib.request

import pandas as pd
import numpy as np
from pprint import pprint

# TODO: add leading 0's, 999000, all cameras should have six digit

import os

data = pd.read_csv('../new_interesting_cams.csv')

#first change the name of the files
for root, dirs, files in os.walk('../test_images'):
    path = root.split(os.sep)
    print('Subdir: ', (len(path) - 1) * '---', os.path.basename(root))

    for i in range(0, len(data['cameraid'])):

        # print(str(data['cameraid'][i]))
        # print(os.path.basename(root))

        if(os.path.basename(root) == str(int(data['cameraid'][i]))):
            # print('here')
            for f in files:
                old_file = list(f)
                index = f.index('_')
                new_num = str(data['old_cameraid'][i])
                # print(new_num)
                new_file = new_num.zfill(6) + f[index:]
                # print(new_file)
                os.rename(os.path.join(root, f), os.path.join(root, new_file))

#then give the folders a temporary name to avoid collisions
for root, dirs, files in os.walk('../test_images'):
    path = root.split(os.sep)
    cwd = os.getcwd()
    size = len(path) - 1

    if(str(path[size]) != 'test_images'):
        os.rename(cwd + '/../test_images/' + path[size], cwd + '/../test_images/a' + path[size])

#lastly put the actual directory name in
for root, dirs, files in os.walk('../test_images'):
    path = root.split(os.sep)
    cwd = os.getcwd()
    size = len(path) - 1

    if(str(path[size]) != 'test_images'):
        d = str(path[size])
        d = d[1:]
        final = ''

        for i in range(0, len(data['cameraid'])):
            if(d == str(data['cameraid'][i])):
                final_dir = str(data['old_cameraid'][i])
                final = final_dir.zfill(6)
                os.rename(cwd + '/../test_images/' + path[size], cwd + '/../test_images/' + final)
