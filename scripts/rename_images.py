import os

import os
import pandas as pd

mhash_to_correct_cam_id = {}
path_to_all_im_folder = 'images/'
df = pd.read_csv("../csv_data/new_interesting_cams.csv")

def create_mhashid_dict():
    df['mhash'] = df['mhash'].astype(int)
    for mh in df['mhash']:
        loc = df.loc[df['mhash'] == mh,'cameraid'].values[0]
        mhash_to_correct_cam_id[mh] = loc


def rename_folder(folder_name,camera_id):
    new_folder_name = camera_id.zfill(8)
    os.rename(folder_name, os.path.join(path_to_all_im_folder, new_folder_name))

def rename_im_in_folder(path_to_folder, correct_cam_id):
	for subdir, dirs, files in os.walk(path_to_folder):
		for file in files:
			# Split off first token, rename to correct id, concatenate back
			filename_split = file.split("_")
			filename_split[0] = str(correct_cam_id)
			new_filename = '_'.join(filename_split)

			os.rename(os.path.join(path_to_folder, file), os.path.join(path_to_folder, new_filename))

	rename_folder(path_to_folder, correct_cam_id)

if __name__ == "__main__":
	create_mhashid_dict()

	for subdir, dirs, files in os.walk(path_to_all_im_folder):
		for dr in dirs:
			# Look at map to get correct cam_id from dir name
			correct_cam_id = str(mhash_to_correct_cam_id[int(dr)])
			# Rename all the images in this folder
			rename_im_in_folder(os.path.join(path_to_all_im_folder, dr), correct_cam_id)