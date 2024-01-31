import subprocess
from HDHashTable import HDHashTable

# Generate a new dataset
subprocess.run(['python3', 'generateData.py'])

# Build the hash table
f = open('dataTrain.csv', 'r')
kmer = f.readline()[:-1] # We include a [:-1] to ignore the '\n'
k = len(kmer)
hash_table = HDHashTable(k=k, D=10000)
while (kmer != ''):
  hash_table.add(kmer)
  kmer = f.readline()[:-1]
f.close()

# Testing
true_pos = 0
true_neg = 0
total_pos = 0
total_neg = 0

f = open('dataTest.csv')
data = f.readline()
while (data != ''):
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
f.close()

# Printing results
print(f'\nCorrectly identified {true_pos} / {total_pos} {k}-mers that were in the hash table')
print(f'Accuracy: {true_pos / total_pos * 100:.2f}%\n')
print(f'Correctly identified {true_neg} / {total_neg} {k}-mers that were not in the hash table')
print(f'Accuracy: {true_neg / total_neg * 100:.2f}%\n')
print(f'Total Accuracy: {(true_pos + true_neg) / (total_pos + total_neg) * 100:.2f}%')
