import os
import sys
import numpy as np
import cv2
import time
from keras.applications.densenet import DenseNet201
from keras.models import Model, load_model, Sequential
from keras.layers import Dense, GlobalMaxPooling2D, Flatten, Dropout, GlobalAveragePooling2D, concatenate, Input
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import SGD
from keras.callbacks import EarlyStopping, ModelCheckpoint
from attention import CoAttentionPara
import keras
import gc
import csv


image_file_dir = './RGBall/'
mani_dir = './manis/data/'
labelfile = './labelfinal2.csv'
labels = {}
apps = []
with open(labelfile, 'r') as f:
	freader = csv.reader(f)
	header = next(freader)
	for r in freader:
		temp = r[1].strip('[').strip(']').split(', ')
		labels[r[0]] = temp
		apps.append(r[0])
images = os.listdir(image_file_dir)
manis = os.listdir(mani_dir)
X1 = []
X2 = []
Y = []
count = 1
for app in apps:
	print('Reading: ' + app + '..........' + str(count) + '/' + str(len(images)))
	img = cv2.imread(image_file_dir + app + '.jpg', 1)
	img = cv2.resize(img, (300, 300))
	img = img / 255.0
	X1.append(img)
	name = app
	label = []
	for l in labels[name]:
		if l == "'0'":
			label.append(0)
		if l == "'1'":
			label.append(1)
		# if l == '0':
		# 	label.append(0)
		# if l == '1':
		# 	label.append(1)
	Y.append(label)
	mani = np.loadtxt(mani_dir + name + '.txt')
	X2.append(mani)
	count += 1
X1 = np.array(X1)
X2 = np.array(X2)
Y = np.array(Y)

gc.collect()

# order = np.argsort(np.random.random(Y.shape[0]))
# X1[order]
# X2[order]
# Y[order]
print('---------------------------------')
print(len(X1), len(X2), len(Y))
print('---------------------------------')
X1_train = X1[:2500]
X2_train = X2[:2500]
Y_train = Y[:2500]
X1_test = X1[2501:]
X2_test = X2[2501:]
Y_test = Y[2501:]

NB_CLASSES = 8
EPOCH = 50
BATCH_SIZE = 64
DIM = 3303

def build_image_vec(base_model):
	x = base_model.output
	x = GlobalMaxPooling2D()(x)
	# x = MaxPooling2D()(x)
	# x = Flatten()(x)
	# print(x.shape)
	# x = Dropout(0.2)(x)
	# x = Dense(3000, activation='relu')(x)
	# x = Dropout(0.2)(x)
	# x = Dense(3000, activation='relu')(x)
	# x = Dropout(0.2)(x)
	y = Dense(3000, activation='relu')(x)
	# x = Dropout(0.2)(x)
	# print(x.shape)
	# y = Dense(nb_classes, activation = "sigmoid")(x)
	model = Model(inputs = base_model.input, outputs = y)
	return model
def build_mani_vec(dim):
	model = Sequential()
	model.add(Dense(3000, input_dim = dim, activation = 'relu'))
	# model.add(Dropout(0.2))
	model.add(Dense(3000, activation = 'relu'))
	# model.add(Dropout(0.2))
	model.add(Dense(3000, activation = 'relu'))

	# x = keras.layers.Input(shape = (dim,))
	# x = Dense(2000, input_dim = dim, kernel_initializer='normal', activation='relu')(x)
	# x = Dropout(0.2)(x)
	# x = Dense(2000, kernel_initializer='normal', activation='relu')(x)
	# x = Dropout(0.2)(x)
	# y = Dense(2000, kernel_initializer='normal', activation='relu')(x)
	# model = Model(inputs = x, outputs = y)
	return model
model1 = DenseNet201(include_top = False, input_shape = (300, 300, 3))
model1 = build_image_vec(model1)
model2 = build_mani_vec(DIM)
x = concatenate([model1.output, model2.output])
# print(model1.output_shape, model2.output_shape)
# xx1, xx2 = CoAttentionPara(dim_k = 3000, name="feature")([model1.output, model2.output])
# x = concatenate([xx1, xx2])
x = Dense(3000, activation = 'relu')(x)
# x = Dropout(0.5)(x)
x = Dense(1500, activation = 'relu')(x)
# x = Dropout(0.5)(x)
x = Dense(500, activation = 'relu')(x)
x = Dropout(0.25)(x)
y = Dense(NB_CLASSES, activation = 'sigmoid')(x)
model = Model(inputs = [model1.input, model2.input], outputs = y)
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# model = load_model("/home/sxy599/DeepAndroidMalware/sample_test/checkpoint-49e-val_accuracy_0.87.hdf5")
output_model_file = './model/checkpoint-{epoch:02d}e-val_accuracy_{val_accuracy:.2f}.hdf5'
checkpoint = ModelCheckpoint(output_model_file, monitor='val_accuracy', verbose=1, save_best_only=True)
early_stop = keras.callbacks.EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True)
history = model.fit([X1_train, X2_train], Y_train, batch_size = 128, epochs = 40, validation_data = ([X1_test, X2_test], Y_test), callbacks = [early_stop, checkpoint])

