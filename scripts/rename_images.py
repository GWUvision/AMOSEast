import os

path_to_all_im_folder = 'images/'
map = {75: 26,
       37: 6969420}

def rename_im_in_folder(path_to_folder, correct_cam_id):
	for subdir, dirs, files in os.walk(path_to_folder):
		for file in files:
			# Split off first token, rename to correct id, concatenate back
			filename_split = file.split("_")
			filename_split[0] = str(correct_cam_id)
			new_filename = '_'.join(filename_split)

			os.rename(os.path.join(path_to_folder, file), os.path.join(path_to_folder, new_filename))
			# rename_folder(path_to_folder, correct_cam_id)

if __name__ == "__main__":
	for subdir, dirs, files in os.walk(path_to_all_im_folder):
		for dr in dirs:
			# Look at map to get correct cam_id from dir name
			correct_cam_id = str(map[int(dr)])
			# Rename all the images in this folder
			rename_im_in_folder(os.path.join(path_to_all_im_folder, dr), correct_cam_id)