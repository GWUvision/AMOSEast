import json
import requests
import urllib.request

import pandas as pd
import numpy as np
from pprint import pprint


for i in range(1, 71, 1):

    url = 'http://amos.cse.wustl.edu/REST/webcams/?page={0}&format=json'.format(i)
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())

    df = pd.DataFrame.from_dict(data['results'])
    print(df.head())
    df.to_csv('output.csv', mode='a', header=False)
    print('Page {0} done...'.format(i))

df1 = pd.read_csv('output.csv')    





# df = pd.read_csv('plessurl_list.csv')
# df = df[np.isfinite(df['roberts auto-rating'])]
# 
# df.drop(['roberts auto-rating', 'index2'], axis=1, inplace=True)
# 
# df['want_kept'] = np.where((df['rating'] != df['extraKeeps']), df['extraKeeps'], np.nan)
# df = df[np.isfinite(df['want_kept'])]
# 
# df.drop(['extraKeeps', 'rating'], axis=1, inplace=True)
# 
# 
# df.to_csv('test.csv')
# print(df.to_string())
# print(df.to_string())



