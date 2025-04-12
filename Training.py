import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import os

# ✅ Enable Eager Execution (Fix for Dataset Iteration Error)
tf.compat.v1.enable_eager_execution()

# Initialize CNN
classifier = Sequential()

# Input Layer
classifier.add(Input(shape=(128, 128, 3)))

# Convolution + Pooling Layers
classifier.add(Conv2D(32, (3, 3), activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2, 2)))
classifier.add(Conv2D(32, (3, 3), activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2, 2)))

# Flattening + Fully Connected Layers
classifier.add(Flatten())
classifier.add(Dense(units=128, activation='relu'))
classifier.add(Dense(units=10, activation='softmax'))  # Use softmax for multi-class classification

# Compile Model
classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Data Augmentation
train_datagen = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
test_datagen = ImageDataGenerator(rescale=1./255)

# Load Data
training_set = train_datagen.flow_from_directory('Dataset/train', target_size=(128, 128), batch_size=6, class_mode='categorical')
valid_set = test_datagen.flow_from_directory('Dataset/val', target_size=(128, 128), batch_size=3, class_mode='categorical')

# Print Class Labels
labels = training_set.class_indices
print(labels)

# ✅ Fix: Use `steps_per_epoch=len(training_set)` to avoid errors
classifier.fit(training_set, steps_per_epoch=len(training_set), epochs=50, validation_data=valid_set)

# Save Model
classifier_json = classifier.to_json()
with open("model1.json", "w") as json_file:
    json_file.write(classifier_json)

classifier.save_weights("my_model_weights.h5")
classifier.save("model.h5")
print("Saved model to disk")
