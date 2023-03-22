# Caleb St.Germain
# COMP5710
# Workshop 7 - Software Forensics
# 03/22/2023

import logging_example

from sklearn.neighbors import KNeighborsClassifier
from sklearn import datasets, linear_model
import pandas as pd
import numpy as np 
import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten
from tensorflow.keras.utils import to_categorical

def readData():
    # Initiated logging object
    logObj = logging_example.giveMeLoggingObject()
    iris = datasets.load_iris()
    # (1) Check for poisoning attacks in iris dataset
    logObj.info('Reading data from iris dataset')
    print(type(iris.data), type(iris.target))
    X = iris.data
    Y = iris.target
    df = pd.DataFrame(X, columns=iris.feature_names)
    print(df.head())

    return df 

def makePrediction():
    # Initiated logging object
    logObj = logging_example.giveMeLoggingObject()
    iris = datasets.load_iris()
    # (2) Check for poisoning attacks in iris dataset
    logObj.info('Reading data from iris dataset to make prediction')
    knn = KNeighborsClassifier(n_neighbors=6)
    knn.fit(iris['data'], iris['target'])
    X = [
        [5.9, 1.0, 5.1, 1.8],
        [3.4, 2.0, 1.1, 4.8],
    ]
    prediction = knn.predict(X)
    print(prediction)
    # (3) Check for model tricking attacks in iris dataset prediction model
    logObj.info('Modeling prediction from iris dataset')

def doRegression():
    # Initiated logging object
    logObj = logging_example.giveMeLoggingObject()
    diabetes = datasets.load_diabetes()
    # (4) Check for poisoning attacks in diabetes dataset
    logObj.info('Reading data from diabetes dataset to do regression')
    diabetes_X = diabetes.data[:, np.newaxis, 2]
    diabetes_X_train = diabetes_X[:-20]
    diabetes_X_test = diabetes_X[-20:]
    diabetes_y_train = diabetes.target[:-20]
    diabetes_y_test = diabetes.target[-20:]
    regr = linear_model.LinearRegression()
    # (5) Check for model tricking attacks in linear regression model
    logObj.info('Modeling regression from diabetes dataset')
    regr.fit(diabetes_X_train, diabetes_y_train)
    diabetes_y_pred = regr.predict(diabetes_X_test)


def doDeepLearning():
    # Initiated logging object
    logObj = logging_example.giveMeLoggingObject()
    train_images = mnist.train_images()
    train_labels = mnist.train_labels()
    test_images = mnist.test_images()
    test_labels = mnist.test_labels()
    # (6) Check for poisoning attacks in mnist dataset
    logObj.info('Reading images from mnist dataset to do deep learning')


    train_images = (train_images / 255) - 0.5
    test_images = (test_images / 255) - 0.5


    train_images = np.expand_dims(train_images, axis=3)
    test_images = np.expand_dims(test_images, axis=3)

    num_filters = 8
    filter_size = 3
    pool_size = 2

    model = Sequential([
    Conv2D(num_filters, filter_size, input_shape=(28, 28, 1)),
    MaxPooling2D(pool_size=pool_size),
    Flatten(),
    Dense(10, activation='softmax'),
    ])

    # Compile the model.
    model.compile(
    'adam',
    loss='categorical_crossentropy',
    metrics=['accuracy'],
    )

    # Train the model.
    model.fit(
    train_images,
    to_categorical(train_labels),
    epochs=3,
    validation_data=(test_images, to_categorical(test_labels)),
    )

    model.save_weights('cnn.h5')
    
    predictions = model.predict(test_images[:5])
    # (7) Check for model tricking attacks in deep learning model
    logObj.info('Modeling deep learning from mnist dataset')
    print(np.argmax(predictions, axis=1)) # [7, 2, 1, 0, 4]

    print(test_labels[:5]) # [7, 2, 1, 0, 4]


if __name__=='__main__': 
    data_frame = readData()
    makePrediction() 
    doRegression() 
    doDeepLearning() 
