#import necessary packages
import os
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from django.conf import settings

#configure input parameters
img_width, img_height = 150, 150
train_data_dir = 'data/train'
validation_data_dir = 'data/validation'
nb_train_samples = 1600
nb_validation_samples = 400
epochs = 15
batch_size = 32

#create model
model = Sequential()
#add a convolutional layer with 32 filters, each with a 3x3 kernel size
model.add(Conv2D(32, (3, 3), input_shape=(img_width, img_height, 3)))
#apply the ReLU activation function
model.add(Activation('relu'))
#apply max pooling with a 2x2 pool size
model.add(MaxPooling2D(pool_size=(2, 2)))

#add another convolutional layer with 32 filters and a 3x3 kernel size
model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

#add a third convolutional layer with 64 filters and a 3x3 kernel size
model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

#flatten the output of the convolutional layers to create a 1D feature vector
model.add(Flatten())
#add a fully connected layer with 64 units
model.add(Dense(64))
model.add(Activation('relu'))
#apply dropout regularization to prevent overfitting
model.add(Dropout(0.5))
#add the final output layer with a single unit and sigmoid activation function
model.add(Dense(1))
model.add(Activation('sigmoid'))

#compile the model with binary cross-entropy loss, RMSprop optimizer, and accuracy metric
model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

#configure data generator for training data with data augmentation
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

#configure data generator for validation data without data augmentation
test_datagen = ImageDataGenerator(rescale=1. / 255)

#create generator for training data
train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

#create generator for validation data
validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

#train the model using the fit_generator function
model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size)

#save the trained model weights to a file
model.save_weights(os.path.join(settings.MODEL_ROOT, 'model_weights.h5'))