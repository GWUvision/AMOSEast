import csv
import pandas as pd
import numpy as np
# 

df2 = pd.read_csv('all_cams.csv')
df1 = pd.read_csv('combined_sets.csv')

df2['good'] = df2.cameraid.map(df1.set_index('cameraid')['good'].to_dict())
df2 = df2[np.isfinite(df2['good'])]
df2.good = df2.good.astype(int)
df2.reset_index(drop=True, inplace=True)
df2.index.name = 'index'


df2.to_csv('test.csv')
