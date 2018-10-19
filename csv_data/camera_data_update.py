import pandas as pd
import numpy as np

df = pd.read_csv('cams_update.csv')

# print(df.head())

# print(len(df))

# df2 = df.drop_duplicates(subset='cameraid', keep='first', inplace=False)

# print(df2.to_csv('cams_update.csv'))

# name = df['name']

print(len(df))

df['name'].replace(' ', np.nan, inplace=True)
df = df.dropna(subset=['name'])

# print(len(df))

df2 = df[df.duplicated(['name'], keep=False)]
# df2 = df[df.duplicated(keep=False)]

print(df2)