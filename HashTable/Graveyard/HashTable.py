"""
Then, you can encode these k-length vectors using standard encoding methods (e.g.,
random projection, id-level encoding, etc.) to get the encoded HD vectors. 

To represent a hash table, I think the naive way is to add all these encoded HD vectors
together to generate a "hash table" HD vector. In this case, you can search a new k-mer
by comparing the similarity of the new k-mer (after encoding) with the "hash-table" HD
vector. If the similarity is large enough, the k-mer may reside in the hash table. This
will definitely bring some inaccuracies for the hash table search, but what we want to
know further is such inaccuracies will significantly decrease the quality of the final
assembly.
"""
import HashTableHD
import numpy as np

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

f = open('dataTest.csv')
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
