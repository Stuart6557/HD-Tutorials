import HashTableHD
import numpy as np
import subprocess

# Generate a new dataset
subprocess.run(['python3', 'generateData.py'])

mapping = {'A': 0, 'C': 1, 'G': 2, 'T': 3}

f = open('dataTrain.csv', 'r')
HT_kmer_vecs = []

kmer = f.readline()
k = len(kmer[:-1]) # We include a [:-1] to ignore the '\n'

while (kmer != ''):
  # Transforms each k-mer to a k-length vector with values between 0 and 3
  kmer_vec = np.array([mapping[char] for char in kmer[:-1]])
  HT_kmer_vecs.append(kmer_vec)
  kmer = f.readline()
f.close()

f = open('dataTest.csv', 'r')
test_kmer_vecs = []
test_labels = []


data = f.readline()
while (data != ''):
  data = data.split(',')
  kmer_vec = np.array([mapping[char] for char in data[0]])
  test_kmer_vecs.append(kmer_vec)
  test_labels.append(data[1].startswith('T'))
  data = f.readline()
f.close()

HashTableHD.train(HT_kmer_vecs, test_kmer_vecs, test_labels)
