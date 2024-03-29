!pip install kaggle

#configurating the path of kaggle.json file
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets download -d girinathrs211555/aadhaar-datasets

# extrcing the compossed Dataset
from zipfile import ZipFile
dataset = '/content/aadhaar-datasets.zip'

with ZipFile(dataset,'r') as zip:
  zip.extractall()
  print('The dataset is extracted')

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
from google.colab.patches import cv2_imshow
from PIL import Image
from sklearn.model_selection import train_test_split

Aadhaar_card_files = os.listdir('/content/Aaadhaar AND Non aadhaar/Aadhaar')
print(Aadhaar_card_files[0:5])

print(Aadhaar_card_files[-5:])

Non_aadhaar_card_files = os.listdir('/content/Aaadhaar AND Non aadhaar/Non Aadhaar')
print(Non_aadhaar_card_files[0:5])

print(Non_aadhaar_card_files[-5:])

print('Number of with Aadhaar_card_files:', len(Aadhaar_card_files))
print('Number of without Non_aadhaar_card_files:', len(Non_aadhaar_card_files))

#create the labels

Aadhaar_card_labels = [1]*5009

Non_aadhaar_card_labels = [0]*5021

# Checking wheather the labels are created as expected
print(Aadhaar_card_labels[0:5])

print(Non_aadhaar_card_labels[0:5])

# I am Concanating  the  two class as labels

labels = Aadhaar_card_labels + Non_aadhaar_card_labels

print(len(labels))
print(labels[0:5])
print(labels[-5:])

# Convert images to numpy arrays

Aadhaar_card__path = '/content/Aaadhaar AND Non aadhaar/Aadhaar/'

data = []
for img_file in Aadhaar_card_files:

  image = Image.open(Aadhaar_card__path + img_file)
  image = image.resize((128,128))
  image = image.convert("RGB")
  image = np.array(image)
  data.append(image)


Non_aadhaar_card_path = '/content/Aaadhaar AND Non aadhaar/Non Aadhaar/'

for img_file in Non_aadhaar_card_files:

  image = Image.open(Non_aadhaar_card_path + img_file)
  image = image.resize((128,128))
  image = image.convert("RGB")
  image = np.array(image)
  data.append(image)

# Coverting image list and the label list to numpy arrays

X = np.array(data)
Y = np.array(labels)

type(X)

type(Y)

print(X.shape)
print(Y.shape)

print(Y)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)

#Scaling the data

X_train_scaled = X_train/255

X_test_scaled = X_test/255

import tensorflow as tf
from tensorflow import keras

num_of_classes = 2

model = keras.Sequential()

model.add(keras.layers.Conv2D(300, kernel_size=(3,3), activation='relu', input_shape=(128,128,3)))
model.add(keras.layers.MaxPooling2D(pool_size=(2,2)))

model.add(keras.layers.Conv2D(600, kernel_size=(3,3), activation='relu'))
model.add(keras.layers.MaxPooling2D(pool_size=(2,2)))

model.add(keras.layers.Conv2D(800, kernel_size=(3,3), activation='relu'))
model.add(keras.layers.MaxPooling2D(pool_size=(2,2)))

model.add(keras.layers.Flatten())

model.add(keras.layers.Dense(128, activation='relu'))
model.add(keras.layers.Dropout(0.5))

model.add(keras.layers.Dense(64, activation='relu'))
model.add(keras.layers.Dropout(0.5))

model.add(keras.layers.Dense(num_of_classes, activation='sigmoid'))

# Compile the neural network

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['acc'])

#traing the neural network
history = model.fit(X_train_scaled, Y_train, validation_split=0.2, epochs=20)

loss, accuracy = model.evaluate(X_test_scaled, Y_test)
print('Test Accuracy=', accuracy)

h = history

#plot the loss value
plt.plot(h.history['loss'], label='train loss')
plt.plot(h.history['val_loss'], label='validation loss')
plt.legend()
plt.show()

#plot the accuracy value
plt.plot(h.history['acc'], label='train accuracy')
plt.plot(h.history['val_acc'], label='validation accuracy')
plt.legend()
plt.show()

input_image_path = input('Path of the image to be predicted: ')

input_image = cv2.imread(input_image_path)

cv2_imshow(input_image)

input_image_resized = cv2.resize(input_image, (128, 128))

input_image_scaled = input_image_resized/255

input_image_reshaped = np.reshape(input_image_scaled, [1,128,128,3])

input_prediction = model.predict(input_image_reshaped)

print(input_prediction)

input_pred_label = np.argmax(input_prediction)

print(input_pred_label)

if input_pred_label == 1:

  print('This is an aadhaar card')

else:

  print('This not an aadhaar card')
