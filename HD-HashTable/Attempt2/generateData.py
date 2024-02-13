# This file generates 500 random 25-mers and writes them to a file named dataTrain.csv. These
# represent the 500 25-mers that exist in our hash table. This file also generates 500 25-mers
# for the testing data and writes them to a file named dataTest.csv. Half of the test data is
# in the hash table and half is not.
# If dataTrain.csv and dataTest.csv already exist, they will be overwritten.

import math
import random
import numpy as np

def generate_kmer(k):
  """
  Generates a k-mer of length k
  """
  DNA_bases = ['A', 'C', 'G', 'T']
  kmer = ''
  for _ in range(k):
    kmer += random.choice(DNA_bases)
  return kmer

def main():
  num_kmers = 500
  k = 25
  kmers_train = set()

  # Generate num_kmers k-mers for the hash table data
  f_train = open('dataTrain.csv', 'w')
  # Generate num_kmers test data. Half will be in the hash table and half will not
  f_test = open('dataTest.csv', 'w')
  includeInTestData = [True] * math.floor(num_kmers/2) + [False] * math.ceil(num_kmers/2)
  np.random.shuffle(includeInTestData)

  for i in range(num_kmers):
    kmer = generate_kmer(k)
    kmers_train.add(kmer)
    f_train.write(kmer + '\n')

    if includeInTestData[i]:
      f_test.write(kmer + ',T\n')

  # Finish generating test data
  for _ in range(math.ceil(num_kmers/2)):
    kmer = generate_kmer(k)
    while kmer in kmers_train:
      # Generate a new k-mer until we get one that's not in the hash tabls
      kmer = generate_kmer(k)
    f_test.write(kmer + ',F\n')
  
  f_train.close()
  f_test.close()

if __name__ == '__main__':
  main()
