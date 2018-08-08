import json
import requests
import urllib.request

import pandas as pd
import numpy as np
from pprint import pprint


# for i in range(1, 71, 1):
#
#     url = 'http://amos.cse.wustl.edu/REST/webcams/?page={0}&format=json'.format(i)
#     with urllib.request.urlopen(url) as url:
#         data = json.loads(url.read().decode())
#
#     df = pd.DataFrame.from_dict(data['results'])
#     print(df.head())
#     df.to_csv('output.csv', mode='a', header=False)
#     print('Page {0} done...'.format(i))

# df1 = pd.read_csv('interesting_cams.csv')
# df2 = pd.read_csv('old_data.csv')
# df = pd.merge(df1, df2, on=['url'], how='left', indicator='old_cameraid')
# # print(df.head(200).to_string())
# df.to_csv('output.csv')


# =========================================================

# df1 = pd.read_csv('interesting_images.csv')

# df2 = pd.read_csv('cameraid_data.csv')
# df = pd.merge(df1, df2, on=['cameraid'], how='left', indicator='test')

# df.to_csv('new_image_data.csv')

# print(df.head())

# =============================================================

# df = pd.read_csv('new_image_data.csv')
# # df.apply(lambda x: x['filepath'].replace(,x['b']), axis=1)
#
# df['filepath'] = df['old_cameraid'].astype(str) + '/' + df['filepath'].astype(str).map(lambda x: x.split('/')[-1])
#
# df.to_csv('new_interesting_images.csv')

# print(df.head())


# TODO: add leading 0's, 999000, all cameras should have six digit

import os

for root, dirs, files in os.walk('flaskapp/static/images'):
    path = root.split(os.sep)
    print((len(path) - 1) * '---', os.path.basename(root))
    for file in files:
        print(len(path) * '---', file)


