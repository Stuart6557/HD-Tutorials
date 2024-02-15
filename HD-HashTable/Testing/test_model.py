# This file calculates and prints the accuracy of a given HDC model on a given test dataset.

import argparse
from HDHashTable import HDHashTable

parser = argparse.ArgumentParser()
parser.add_argument('--modelPath', action='store', type=str, help='path to model csv file', required=True)
parser.add_argument('--testDataPath', action='store', type=str, help='path to test data csv file', required=True)

inputs = parser.parse_args()
model_path = inputs.modelPath
test_data_path = inputs.testDataPath

# Build the model
set_hash_table_hv = []
f = open(model_path, 'r')
val = f.readline()
while val != '':
  val = int(val[:-1]) # Need [:-1] to exclude the last newline character
  set_hash_table_hv.append(val)
  val = f.readline()
D = len(set_hash_table_hv)
f.close()

# Get the length of a k-mer
f = open(test_data_path, 'r')
kmer = f.readline().split(',')[0]
k = len(kmer)

hash_table = HDHashTable(k=k, D=D)
hash_table.set_hash_table_hv(set_hash_table_hv)

# Testing
true_pos = 0
true_neg = 0
total_pos = 0
total_neg = 0

f.seek(0) # Go back to the top of the file
data = f.readline()
while data != '':
  data = data.split(',')
  kmer = data[0]
  in_hash_table = data[1].startswith('T')
  query_result = hash_table.query(kmer)
  if (in_hash_table):
    total_pos += 1
    if (query_result):
      true_pos += 1
  if (not in_hash_table):
    total_neg += 1
    if (not query_result):
      true_neg += 1
  data = f.readline()

num_kmers = total_pos + total_neg
f.close()

# Print results
print(f'{num_kmers=}')
print(f'\nCorrectly identified {true_pos} / {total_pos} {k}-mers that were in the hash table')
print(f'Accuracy: {true_pos / total_pos * 100:.2f}%\n')
print(f'Correctly identified {true_neg} / {total_neg} {k}-mers that were not in the hash table')
print(f'Accuracy: {true_neg / total_neg * 100:.2f}%\n')
print(f'Total Accuracy: {(true_pos + true_neg) / (total_pos + total_neg) * 100:.2f}%')