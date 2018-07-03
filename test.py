import pandas as pd

df = pd.read_csv('out2.csv', sep='delimiter', header=None)

# print(df)

df.columns = ['cameraid']

df['cameraid'] = df['cameraid'].str.strip('[(')

df.to_csv('cameras_to_remove.csv', sep=',', header=None)

# print(df)