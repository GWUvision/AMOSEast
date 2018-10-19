import os
import pandas as pd

dict = {}
df = pd.read_csv("AMOSEast/csv_data/new_interesting_cams.csv")

def create_mhashid_dict(df):
    df['mhash'] = df['mhash'].astype(int)
    for mh in df['mhash']:
        loc = df.loc[df['mhash'] == mh,'cameraid'].values[0]
        dict[mh] = loc


def rename_folder(folder_name,camera_id):
    new_folder_name = camera_id.zfill(8)
    os.rename(folder_name,new_folder_name)
