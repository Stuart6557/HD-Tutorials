import numpy as np
import pickle
import sys
import os
import math
from copy import deepcopy
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier as KNN


"""
Each value in base_matrix is converted to -1 if negative and to 1 otherwise.
"""
def binarize(base_matrix):
	return np.where(base_matrix < 0, -1, 1)


"""
Random projection
Encodes each data point in X_data (2D array) by mulitplying it with base_matrix.
Prints percentage completed every 20 iterations.
Binarizes encoding if signed=True.
"""
def encoding_rp(X_data, base_matrix, signed=False):
	enc_hvs = []
	for i in range(len(X_data)):
		if i % int(len(X_data)/20) == 0:
			sys.stdout.write(str(int(i/len(X_data)*100)) + '% ')
			sys.stdout.flush()
		hv = np.matmul(base_matrix, X_data[i])
		if signed:
			hv = binarize(hv)
		enc_hvs.append(hv)
	return enc_hvs


"""
ID-level encoding
Encodes each data point in X_data (2D array) with the given variables:
	lvl_hvs, id_hvs, bin_len, and x_min.
Prints percentage completed every 20 iterations.
"""
def encoding_idlv(X_data, lvl_hvs, id_hvs, D, bin_len, x_min, L=64):
	enc_hvs = []
	for i in range(len(X_data)):
		if i % int(len(X_data)/20) == 0:
			sys.stdout.write(str(int(i/len(X_data)*100)) + '% ')
			sys.stdout.flush()
		sum_ = np.array([0] * D)
		for j in range(len(X_data[i])):
			bin_ = min(np.floor((X_data[i][j] - x_min)/bin_len), L-1)
			bin_ = int(bin_)
			sum_ += lvl_hvs[bin_]*id_hvs[j]
		enc_hvs.append(sum_)
	return enc_hvs


"""
Permutation encoding
Encodes each data point in X_data (2D array) with the given variables:
	lvl_hvs, bin_len, and x_min.
Prints percentage completed every 20 iterations.
"""
def encoding_perm(X_data, lvl_hvs, D, bin_len, x_min, L=64):
	enc_hvs = []
	for i in range(len(X_data)):
		if i % int(len(X_data)/20) == 0:
			sys.stdout.write(str(int(i/len(X_data)*100)) + '% ')
			sys.stdout.flush()
		sum_ = np.array([0] * D)
		for j in range(len(X_data[i])):
			bin_ = min(np.floor((X_data[i][j] - x_min)/bin_len), L-1)
			bin_ = int(bin_)
			sum_ += np.roll(lvl_hvs[bin_], j)
		enc_hvs.append(sum_)
	return enc_hvs


"""
Finds and returns the index of the best class match for the given encoded hypervector enc_hv.
"""
def max_match(class_hvs, enc_hv, class_norms):
		max_score = -np.inf
		max_index = -1
		for i in range(len(class_hvs)):
			score = np.matmul(class_hvs[i], enc_hv) / class_norms[i]
			if score > max_score:
				max_score = score
				max_index = i
		return max_index


"""
Trains model given data, dimension, algorithm, epoch, learning rate, and number of levels.
Returns accuracy.
"""
def train(X_train, y_train, X_test, y_test, D=500, alg='rp', epoch=20, lr=1.0, L=64):
	
	# Randomly select 20% of train data as validation
	permvar = np.arange(0, len(X_train))
	np.random.shuffle(permvar)
	X_train = [X_train[i] for i in permvar]
	y_train = [y_train[i] for i in permvar]
	cnt_vld = int(0.2 * len(X_train))
	X_validation = X_train[0:cnt_vld]
	y_validation = y_train[0:cnt_vld]
	X_train = X_train[cnt_vld:]
	y_train = y_train[cnt_vld:]

	# Encodings
	if alg in ['rp', 'rp-sign']:
		# Create D x len(X_train[0]) base matrix, around half the values will be 1 and the other half will be -1
		# Basically create a D dimensional hv for each X_train
		base_matrix = np.random.rand(D, len(X_train[0]))
		base_matrix = np.where(base_matrix > 0.5, 1, -1)
		base_matrix = np.array(base_matrix, np.int8)
		# Encode training data using idlv algorithm
		print('\nEncoding ' + str(len(X_train)) + ' train data')
		train_enc_hvs = encoding_rp(X_train, base_matrix, signed=(alg == 'rp-sign'))
		print('\n\nEncoding ' + str(len(X_validation)) + ' validation data')
		validation_enc_hvs = encoding_rp(X_validation, base_matrix, signed=(alg == 'rp-sign'))
	
	elif alg in ['idlv', 'perm']:
		# Create level matrix
		lvl_hvs = []
		# Create list temp where half the values are -1s and the other half are 1s (shuffled)
		# This will be the first hv of lvl_hvs
		temp = [-1]*int(D/2) + [1]*int(D/2)
		np.random.shuffle(temp)
		lvl_hvs.append(temp)
		# Create list change_list whose values are 0 to D (shuffled)
		change_list = np.arange(0, D)
		np.random.shuffle(change_list)
		cnt_toChange = int(D/2 / (L-1))
		for i in range(1, L):
			# Assign temp to be the previous hv in lvl_hvs
			temp = np.array(lvl_hvs[i-1])
			# Flip the sign on cnt_toChange random values in temp
			# In each iteration, the values whose sign is flipped have never had their sign flipped before
			# By the end of the last iteration, half the values in temp will have had their sign flipped
			temp[change_list[(i-1)*cnt_toChange : i*cnt_toChange]] = -temp[change_list[(i-1)*cnt_toChange : i*cnt_toChange]]
			lvl_hvs.append(list(temp))
		
    # Each value in lvl_hvs should be an 8 bit signed integer
		lvl_hvs = np.array(lvl_hvs, dtype=np.int8)
		x_min = min( np.min(X_train), np.min(X_validation) )
		x_max = max( np.max(X_train), np.max(X_validation) )
		bin_len = (x_max - x_min)/float(L)
		
		# Need to create id hypervectors if encoding is level-id
		if alg == 'idlv':
			cnt_id = len(X_train[0])
			# id_hvs is a cnt_id x D array where half of each array's values is -1 and the other half is 1 (shuffled)
			id_hvs = []
			for i in range(cnt_id):
				temp = [-1]*int(D/2) + [1]*int(D/2)
				np.random.shuffle(temp)
				id_hvs.append(temp)
			id_hvs = np.array(id_hvs, dtype=np.int8)
			# Encode training data using idlv algorithm
			print('\nEncoding ' + str(len(X_train)) + ' train data')
			train_enc_hvs = encoding_idlv(X_train, lvl_hvs, id_hvs, D, bin_len, x_min, L)
			print('\n\nEncoding ' + str(len(X_validation)) + ' validation data')
			validation_enc_hvs = encoding_idlv(X_validation, lvl_hvs, id_hvs, D, bin_len, x_min, L)
		elif alg == 'perm':
			# Encode training data using perm algorithm
			print('\nEncoding ' + str(len(X_train)) + ' train data')
			train_enc_hvs = encoding_perm(X_train, lvl_hvs, D, bin_len, x_min, L)
			print('\n\nEncoding ' + str(len(X_validation)) + ' validation data')
			validation_enc_hvs = encoding_perm(X_validation, lvl_hvs, D, bin_len, x_min, L)
	
	# Training, initial model
  # class_hvs is initialized to be a (max(y_train) + 1) x D array of 0s
	class_hvs = [[0.] * D] * (max(y_train) + 1)
	# Trains model by adding encoded hvs to different hvs in class_hvs
	for i in range(len(train_enc_hvs)):
		class_hvs[y_train[i]] += train_enc_hvs[i]
	# Default np.linalg.norm is Frobenius norm
  # Frobenius norm: the square root of the sum of the squares of all the matrix entries
	class_norms = [np.linalg.norm(hv) for hv in class_hvs]
	class_hvs_best = deepcopy(class_hvs)
	class_norms_best = deepcopy(class_norms)
	
	# Retraining
	if epoch > 0:
		acc_max = -np.inf
		print('\n\n' + str(epoch) + ' retraining epochs')
		for i in range(epoch):
			sys.stdout.write('epoch ' + str(i) + ': ')
			sys.stdout.flush()
			# Shuffle data during retraining
			pickList = np.arange(0, len(train_enc_hvs))
			np.random.shuffle(pickList)
			for j in pickList:
				predict = max_match(class_hvs, train_enc_hvs[j], class_norms)
				if predict != y_train[j]:
					class_hvs[predict] -= np.multiply(lr, train_enc_hvs[j])
					class_hvs[y_train[j]] += np.multiply(lr, train_enc_hvs[j])
			class_norms = [np.linalg.norm(hv) for hv in class_hvs]
			
      # Use validation data to pick the best class hvs and class norms
			correct = 0
			for j in range(len(validation_enc_hvs)):
				predict = max_match(class_hvs, validation_enc_hvs[j], class_norms)
				if predict == y_validation[j]:
					correct += 1
			acc = float(correct)/len(validation_enc_hvs)
			sys.stdout.write("%.4f " %acc)
			sys.stdout.flush()
			if i > 0 and i%5 == 0:
				print('')
			if acc > acc_max:
				acc_max = acc
				class_hvs_best = deepcopy(class_hvs)
				class_norms_best = deepcopy(class_norms)
	
	del X_train
	del X_validation
	del train_enc_hvs
	del validation_enc_hvs

  # Test model accuracy
  # Encode test data
	print('\n\nEncoding ' + str(len(X_test)) + ' test data')
	if alg == 'rp' or alg == 'rp-sign':
		test_enc_hvs = encoding_rp(X_test, base_matrix, signed=(alg == 'rp-sign'))
	elif alg == 'idlv':
		test_enc_hvs = encoding_idlv(X_test, lvl_hvs, id_hvs, D, bin_len, x_min, L)
	elif alg == 'perm':
			test_enc_hvs = encoding_perm(X_test, lvl_hvs, D, bin_len, x_min, L)
  # Make predictions and calculate model accuracy
	correct = 0
	for i in range(len(test_enc_hvs)):
		predict = max_match(class_hvs_best, test_enc_hvs[i], class_norms_best)
		if predict == y_test[i]:
			correct += 1
	acc = float(correct)/len(test_enc_hvs)
	return acc
