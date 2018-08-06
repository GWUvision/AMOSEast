# USAGE
# python train_network.py --dataset images --model santa_not_santa.model

# https://www.pyimagesearch.com/2017/12/11/image-classification-with-keras-and-deep-learning/


# set the matplotlib backend so figures can be saved in the background
import matplotlib
matplotlib.use("Agg")

# import the necessary packages
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import img_to_array
from keras.utils import to_categorical
from lenet import LeNet
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import argparse
import random
import cv2
import os
from PIL import Image


# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-d", "--dataset", required=True,
#                 help="path to input dataset")
# ap.add_argument("-m", "--model", required=True,
#                 help="path to output model")
# ap.add_argument("-p", "--plot", type=str, default="{0}_plot.png".format(IMAGE_LABEL),
#                 help="path to output loss/accuracy plot")
# args = vars(ap.parse_args())

# initialize the number of epochs to train for, initia learning rate,
# and batch size
EPOCHS = 5
INIT_LR = 1e-3
BS = 32
path = '256_ObjectCategories'


master_data = []
master_labels = []

categories = []
for root, dirs, files in os.walk(path, topdown=False):
    for name in dirs:
        categories.append(name.split('.'))
        # print(name.split('.'))

data = []
labels = []
user_word = ''

print(categories)

for c in categories:
    # initialize the data and labels
    print("[INFO] loading images from " + str(c[1]))

    path = '256_ObjectCategories/' + str(c[0]) + '.' + str(c[1])

    if(c[0] == 258):
        user_word = c[1]
        print(user_word)

    # grab the image paths and randomly shuffle them
    imagePaths = sorted(list(paths.list_images(path)))
    random.seed(42)
    random.shuffle(imagePaths)

    for index, imagePath in enumerate(imagePaths):
        # print(imagePath)
        try:
            im = Image.open(imagePath)

            image = cv2.imread(imagePath)
            image = cv2.resize(image, (28, 28))
            image = img_to_array(image)
            data.append(image)

            label = imagePath.split(os.path.sep)[-2]

            #print("label:" + label)
            #print("category:" + c[1])

            if(label[4:] == c[1]):  # c is the category
                # take first part of path, convert from str to int
                label = int(c[0])
            else:
                label = 0

            labels.append(label)

        except IOError as e:
            print(e)
            pass
        except SyntaxError as e:
            print(e)
            pass

# scale the raw pixel intensities to the range [0, 1]
data = np.array(data, dtype="float") / 255.0
labels = np.array(labels)

# partition the data into training and testing splits using 75% of
# the data for training and the remaining 25% for testing
(trainX, testX, trainY, testY) = train_test_split(
    data, labels, test_size=0.25, random_state=42)


# convert the labels from integers to vectors
print(trainY)
trainY = to_categorical(trainY, num_classes=259)
testY = to_categorical(testY, num_classes=259)

# construct the image generator for data augmentation
aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
                         height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
                         horizontal_flip=True, fill_mode="nearest")

# initialize the model
print("[INFO] compiling model...")
model = LeNet.build(width=28, height=28, depth=3, classes=259)
opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
model.compile(loss="binary_crossentropy", optimizer=opt,
              metrics=["accuracy"])

# train the network
print("[INFO] training network...")
H = model.fit_generator(aug.flow(trainX, trainY, batch_size=BS),
                        validation_data=(testX, testY), steps_per_epoch=len(
                            trainX) // BS,
                        epochs=EPOCHS, verbose=1)

# save the model to disk
print("[INFO] serializing network...")
model.save("example_model")

# plot the training loss and accuracy
plt.style.use("ggplot")
plt.figure()
N = EPOCHS
plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
plt.plot(np.arange(0, N), H.history["acc"], label="train_acc")
plt.plot(np.arange(0, N), H.history["val_acc"], label="val_acc")
plt.title(
    "Training Loss and Accuracy on {0}".format("butt"))
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="lower left")
plt.savefig("accuracy.png")
