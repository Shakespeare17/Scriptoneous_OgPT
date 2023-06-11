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
model.add(Conv2D(32, (3, 3), input_shape=(img_width, img_height, 3)))  # Add a 2D convolutional layer with 32 filters and a 3x3 kernel
model.add(Activation('relu'))  # Apply ReLU activation function to introduce non-linearity
model.add(MaxPooling2D(pool_size=(2, 2)))  # Apply max pooling to reduce spatial dimensions

# Alternative: You can add more convolutional and pooling layers to increase the model's complexity and capacity.

model.add(Conv2D(32, (3, 3)))  # Add another 2D convolutional layer
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))  # Add one more 2D convolutional layer
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())  # Flatten the output from the previous layer
model.add(Dense(64))  # Add a fully connected layer with 64 units
model.add(Activation('relu'))  # Apply ReLU activation function
model.add(Dropout(0.5))  # Apply dropout regularization to prevent overfitting
model.add(Dense(1))  # Add a final fully connected layer with a single unit
model.add(Activation('sigmoid'))  # Apply sigmoid activation for binary classification

model.compile(loss='binary_crossentropy',  # Configure the model with binary cross-entropy loss
              optimizer='rmsprop',  # Use the RMSprop optimizer
              metrics=['accuracy'])  # Track accuracy as a metric

#configure data generator
train_datagen = ImageDataGenerator(
    rescale=1. / 255,  # Rescale pixel values between 0 and 1
    shear_range=0.2,  # Apply random shear transformations
    zoom_range=0.2,  # Apply random zoom transformations
    horizontal_flip=True)  # Flip images horizontally

test_datagen = ImageDataGenerator(rescale=1. / 255)  # Only rescale pixel values for the validation set

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')  # Generate batches of augmented image data with binary labels

validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

#train the model
model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size)

