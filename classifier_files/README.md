# Generic-Web-Classifier

## A Generic Classifier for any image


https://www.pyimagesearch.com/2017/12/11/image-classification-with-keras-and-deep-learning/

The goal of the Generic Web Classifier is an upgrade from @Arkidillo and @benfernandez "generic incremental classifier": [Github Repository](https://github.com/Arkidillo/generic-incremental-classifier)

Using LeNet architecture as the convolutional neural network of choice, with Keras and Tensorflow backend, a more accurate, but specified classifier is implemented for the user

This web application is a pipeline for all of the steps required in classification. The user simply types in the object they wish to classify, and the program will go to work downloading test images using Google Images, and training the classifier on our test classes as well as the new test data. The user can then upload an image to test the model on a separate page.

Readme will be updated and organized as project progresses...

TODO: find dataset with many images all tagged and original images such that when user asks for a specific *thing* the neural network will test against all pictures not associated with *thing*

TODO: work on scraping online all image searches of the specific *thing* they want

TODO: essentially, goal is to make this generic and web based
