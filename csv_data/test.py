import json
import requests
import urllib.request

import pandas as pd
import numpy as np
from pprint import pprint
import datetime as dt

# for i in range(1, 71, 1):
#
#     url = 'http://amos.cse.wustl.edu/REST/webcams/?page={0}&format=json'.format(i)
#     with urllib.request.urlopen(url) as url:
#         data = json.loads(url.read().decode())
#
#     df = pd.DataFrame.from_dict(data['results'])
#     print(df.head())
#     df.to_csv('old_data.csv', mode='a', header=False)
#     print('Page {0} done...'.format(i))

# df1 = pd.read_csv('interesting_cams.csv')
# df2 = pd.read_csv('old_data.csv')
# df = pd.merge(df1, df2, on=['url'], how='left', indicator='old_cameraid')
# # print(df.head(200).to_string())
# df.to_csv('cameraid_data.csv')


# =========================================================

# df1 = pd.read_csv('/home/suraj/Desktop/all_images.csv')
# 
# df1.columns = ['rowid', 'filepath', 'curr_time', 'cameraid']
# 
# 
# df2 = pd.read_csv('new_interesting_cams.csv')
# df = pd.merge(df1, df2, on=['cameraid'], how='left', indicator='test')
# 
# # print(df)
# 
# df.to_csv('new_image_data.csv')

# df.to_csv('new_image_data.csv')

# print(df.head())

# =============================================================


# df = pd.read_csv('new_image_data.csv')
# 
# df.drop(['rowid', 'name', 'url', 'latitude', 'longitude', 'last_width', 'last_height', 'mhash', 'test', 'Unnamed: 0'], axis=1, inplace=True)
# # print(df.head().to_string())
# 
# df.index.name = 'rowid'
# print(df.head())
# df.to_csv('new_image_data.csv')

# df = pd.read_csv('new_image_data.csv')
# # df.apply(lambda x: x['filepath'].replace(,x['b']), axis=1)

# df['filepath'] = df['old_cameraid'].astype(str) + '/' + df['filepath'].astype(str).map(lambda x: x.split('/')[-1])
#
# df.to_csv('new_interesting_images.csv')

# print(df.head())

# df1 = pd.read_csv('/home/suraj/Desktop/new_interesting_cams.csv')
# 
# df1['old_cameraid'] = df1['old_cameraid'].astype(str).str.zfill(6)
# 
# print(df1.head())
# df1.to_csv('new_interesting_cams.csv')


df2 = pd.read_csv('/home/suraj/Documents/GWU/AMOSEast/csv_data/new_image_data.csv')

df2.set_index('rowid', inplace=True)


# print(df2.head())
# df2.columns = ['rowid', 'filepath', 'curr_time', 'cameraid']
df2['curr_time'] = pd.to_datetime(df2['curr_time'])
# 
# 
df2['filepath'] = df2['old_cameraid'].astype(str).str.zfill(6) + '/' + df2['old_cameraid'].astype(str).str.zfill(6) + '_' + df2['curr_time'].dt.strftime('%Y%m%d_%H%M%S')
# # 
# print(df2.head())

df2.drop('cameraid', axis=1, inplace=True)
df2.columns = ['filepath', 'curr_time', 'cameraid']

print(df2.head())
print(len(df2.index))

df2.to_csv('all_new_images.csv')




