import numpy as np
from numpy import mean
from numpy import std
import seaborn as sns
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Dropout
from keras.layers import Conv1D
from keras.layers import Conv2D
from keras.layers import MaxPooling1D
from keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
import pandas as pd
import string
import re
import random
import hashlib

dataset_path = 'YOUR_PATH'
model_path = 'YOUR_PATH'


save_model = 0

def read_and_norm(dataset_path, type_,type):
    with open('{}/{}/{}.txt'.format(dataset_path, type_,type), 'rb') as f:
        matrix = [[float(x) for x in line.split()] for line in f]
    matrix = np.array(matrix)
    min_m = matrix.min().min()
    max_m = matrix.max().max()
    matrix = ((matrix - min_m) / (max_m - min_m))
    return matrix

def load_full_dataset(type_):
	classification = np.loadtxt('{}/{}/classification.txt'.format(dataset_path, type_))
	classification = np.array(classification).reshape(-1,1)

	with open('{}/{}/hr.txt'.format(dataset_path, type_), "r") as file:
		hr = []
		righe_con_9_colonne = []
		for indice, riga in enumerate(file):
			colonne = riga.split()
			if len(colonne) == 9:
				righe_con_9_colonne.append(indice)
			else:
				hr.append(colonne)
	hr = [[float(string) for string in inner] for inner in hr]
	hr = np.array(hr)


	shape = read_and_norm(dataset_path, type_,'shape')
	el = read_and_norm(dataset_path, type_,'el')
	dist = read_and_norm(dataset_path, type_,'dist')

	classification = np.delete(classification, righe_con_9_colonne, 0)
	shape = np.delete(shape, righe_con_9_colonne, 0)
	el = np.delete(el, righe_con_9_colonne, 0)
	dist = np.delete(dist, righe_con_9_colonne, 0)


	data_X = np.array([p for p in zip(shape, dist, el, hr)])
	data_X = data_X.reshape(data_X.shape[0], data_X.shape[1], data_X.shape[2], 1)

	return(data_X,classification)


# fit and evaluate a model
def evaluate_model_2dconv(trainX, trainy, testX, testy):
	verbose, epochs, batch_size = 1, 300, 1
	n_outputs = trainy.shape[1]
	model = Sequential()

	model.add(Conv2D(filters=9, kernel_size=(4,1), input_shape=trainX.shape[1:],activation='relu'))
	model.add(Dropout(0.25))
	model.add(Conv2D(filters=3, kernel_size=(1,3), activation='relu')) #(1,5)

	model.add(Dropout(0.25))

	model.add(Flatten())
	model.add(Dense(30, activation='relu'))
	model.add(Dropout(0.2))
	model.add(Dense(30, activation='relu'))
	model.add(Dropout(0.2))
	model.add(Dense(n_outputs, activation='sigmoid'))
	model.summary()
	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

	es = EarlyStopping(monitor='val_accuracy',
				   mode='max',
				   patience=50,
				   restore_best_weights=True)

	history = model.fit(trainX, trainy, epochs=epochs, batch_size=batch_size, verbose=verbose,validation_split=.2,callbacks=[es])#,callbacks=rlronp)#) #,callbacks=[es])

	# evaluate model
	_, accuracy = model.evaluate(testX, testy, batch_size=batch_size, verbose=1)

	pred_label_ = model.predict(testX,batch_size=batch_size)

	pred_label = [1. if x >= 0.5 else 0. for x in pred_label_]
	results = pd.DataFrame({'Pred': pred_label,'Prob':pred_label_.reshape(-1), 'True': testy.reshape(-1)})



	if save_model:
		model.save('{}/my_model.keras'.format(model_path))

	return accuracy, history



# summarize scores
def summarize_results(scores):
	print(scores)
	m, s = mean(scores), std(scores)
	print('Accuracy: %.3f%% (+/-%.3f)' % (m, s))

# run an experiment
def run_experiment(repeats=1):
	#load data
	trainX, trainy = load_full_dataset('train')
	testX, testy = load_full_dataset('test')


	# repeat experiment
	scores = list()
	for r in range(repeats):
		score,history = evaluate_model_2dconv(trainX, trainy, testX, testy)

		score = score * 100.0
		print('>#%d: %.3f' % (r+1, score))
		scores.append(score)

	summarize_results(scores)


run_experiment()
