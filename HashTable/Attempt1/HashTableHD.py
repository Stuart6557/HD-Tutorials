import math
import numpy as np
from numpy import dot
from numpy.linalg import norm
import sys


"""
Each value in base_matrix is converted to -1 if negative and to 1 otherwise.
"""
def binarize(base_matrix):
	return np.where(base_matrix < 0, -1, 1)


"""
Random projection
Encodes each data point in X_data by mulitplying it with a base_matrix.
X_data is a num_kmers x k 2D array containing num_kmers k-mers.
Binarizes encoding if signed=True.
Returns encoded data in a num_kmers x D 2D array.
"""
def encoding_rp(X_data, base_matrix, signed=False):
	num_kmers = len(X_data)
	
	enc_hvs = []
	for i in range(num_kmers):
		# Print percentage completed every 20 iterations
		if i % int(num_kmers/20) == 0:
			print(str(int(i/num_kmers*100)) + '%', end=' ')
		hv = np.matmul(X_data[i], base_matrix)
		if signed:
			hv = binarize(hv)
		enc_hvs.append(hv)
	
	print()
	return enc_hvs


"""
ID-level encoding
Encodes each data point in X_data (2D array) with the given variables:
	lvl_hvs, id_hvs, bin_len, and x_min.
"""
def encoding_idlv(X_data, lvl_hvs, id_hvs, D, bin_len, x_min, L=64):
	enc_hvs = []
	for i in range(len(X_data)):
		# Print percentage completed every 20 iterations
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
"""
def encoding_perm(X_data, lvl_hvs, D, bin_len, x_min, L=64):
	enc_hvs = []
	for i in range(len(X_data)):
		# Print percentage completed every 20 iterations
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
Returns whether or not enc_hv is in the hash table represented by hash_table_hv
"""
def cos_sim(hash_table_hv, enc_hv):
	return dot(hash_table_hv, enc_hv) / (norm(hash_table_hv) * norm(enc_hv))


"""
Trains model with X_train and returns the accuracy from testing X_test and y_test
"""
def train(X_train, X_test, y_test, D=500, alg='rp'):
	k = len(X_train[0])

	if alg in ['rp', 'rp-sign']:
		# Create k x D base matrix, around half the values will be 1 and the other half will be -1
		base_matrix = np.random.rand(k, D)
		base_matrix = np.where(base_matrix > 0.5, 1, -1)
		base_matrix = np.array(base_matrix, np.int8)

		# Encode training data using random projection algorithm
		# AKA create a D dimensional hv for each k-mer in X_data
		print('\nEncoding ' + str(len(X_train)) + ' train data')
		data_enc_hvs = encoding_rp(X_train, base_matrix, signed=(alg == 'rp-sign'))

		# Calculate hypervector representing the entire hash table
		hash_table_hv = [sum(column) for column in zip(*data_enc_hvs)]

		# Testing
		print('\nEncoding ' + str(math.floor(len(X_test)/2)) + ' test data')
		test_enc_hvs = encoding_rp(X_test, base_matrix, signed=(alg == 'rp-sign'))
		# Make predictions and calculate model accuracy
		correct = 0
		print('\nCosine similarities')
		for i in range(len(test_enc_hvs)):
			sim = cos_sim(hash_table_hv, test_enc_hvs[i])
			print(f'{sim=}')
			predict = sim > 0.9
			if predict == y_test[i]:
				correct += 1
		test_accuracy = float(correct)/len(test_enc_hvs)
		
		print(f'\n{test_accuracy=}')
