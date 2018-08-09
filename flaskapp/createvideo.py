
import cv2
import imageio
import os

def video_dir():

    list_of_images = []
    rootDir = '6/'
    for dirpath, dirnames, files in os.walk(rootDir, topdown=True):
        dirnames.sort(key=int)
        list_of_images.append(files)

    for i in range(1, len(list_of_images), 1):
        images_in_folder = []
        os.makedirs('videos/%d' % (i), exist_ok=True)

        for j in range(len(list_of_images[i])):
            print(list_of_images[i][j])
            file_path = os.path.join('6/%d' %
                                     (i), list_of_images[i][j])

            images_in_folder.append(imageio.imread(file_path))
        imageio.mimsave('videos/%d/movie%d.mp4' %
                        (i, i), images_in_folder)

video_dir()
