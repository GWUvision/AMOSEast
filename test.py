import pandas as pd

df = pd.read_csv('ratings.csv')


print(df['rating'], df['url'])
