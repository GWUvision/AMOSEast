import csv
import pandas as pd
import numpy as np
# 

# df2 = pd.read_csv('all_cams.csv')
# df1 = pd.read_csv('combined_sets.csv')
# 
# df2['good'] = df2.cameraid.map(df1.set_index('cameraid')['good'].to_dict())
# df2 = df2[np.isfinite(df2['good'])]
# df2.good = df2.good.astype(int)
# df2.reset_index(drop=True, inplace=True)
# df2.index.name = 'index'


# df2.to_csv('test.csv')

df1 = pd.read_csv('csv_data/interesting_cams.csv')
df2 = pd.read_csv('csv_data/images.csv')

# print(df2.columns)

df = pd.merge(df1, df2, on=['cameraid'], how='left', indicator='Exist')
df['Exist'] = np.where(df.Exist == 'both', True, False)

good_bye_list = ['Exist', 'name', 'url', 'latitude', 'longitude', 'last_width', 'last_height', 'mhash', 'rowid']
df.drop(good_bye_list, axis=1, inplace=True)

df.index.name = 'rowid'

df = df[['filepath', 'curr_time', 'cameraid']]

print(df.head())

df.to_csv('test.csv')


