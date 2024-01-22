# This file generates 500 random 25-mers and writes them to a file named 25mers.txt
# If 25mers.txt already exists, it will be overwritten

import random

"""
Generates a k-mer of length k
"""
def generate_kmer(k):
  DNA_bases = ['A', 'C', 'G', 'T']
  kmer = ''
  for _ in range(k):
    kmer += random.choice(DNA_bases)
  return kmer

def main():
  num_kmers = 500
  k = 25

  f = open('25mers.txt', 'w')
  for _ in range(num_kmers):
    f.write(generate_kmer(k) + '\n')
  f.close()


if __name__ == '__main__':
  main()
