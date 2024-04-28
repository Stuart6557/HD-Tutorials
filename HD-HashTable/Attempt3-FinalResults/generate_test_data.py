# This file generates a test dataset of k-mers in the given fastq data and k-mers not in the given data.
# 
# python3 generate_test_data.py --path bacillus-SRR26664315.fastq --reads 30

import random
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--path', action='store', type=str, help='path to fastq data file', required=True)
parser.add_argument('--reads', action='store', type=int, default=30, help='number of reads used to train model')
parser.add_argument('--k', action='store', type=int, default=501, help='length of a k-mer (should be odd, default is 501)')
parser.add_argument('--numPos', action='store', type=int, default=200, help='number of k-mers in the generated test data that are in the hash table (default 200)')
parser.add_argument('--numNeg', action='store', type=int, default=200, help='number of k-mers in the generated test data that are not in the hash table (default 200)')

inputs = parser.parse_args()
data_file = inputs.path
reads = inputs.reads
k = inputs.k
num_pos = inputs.numPos
num_neg = inputs.numNeg

DNA_bases = ['A', 'C', 'G', 'T']

def generate_kmer(k):
  """
  Generates a k-mer of length k
  """
  kmer = ''
  for _ in range(k):
    kmer += random.choice(DNA_bases)
  return kmer

def in_dataset(data_file, reads, kmer):
  """
  Returns whether or not the given k-mer is in the first reads of the given data
  """
  f = open(data_file, "r")
  read = f.readline()
  for _ in range(reads):
    read = f.readline().strip()
    if kmer in read:
      return True
  return False

def main():
  kmer_per_read = int(num_pos / reads)

  f = open(data_file, "r")
  out = open("data_test.csv", "w")

  read = f.readline()

  # First, randomly generate k-mers in the hash table
  for _ in range(reads):
    # Need to read the next line due to the way fastq files are structured
    # For more information, check out this Illumina page:
    #   https://knowledge.illumina.com/software/general/software-general-reference_material-list/000002211
    read = f.readline().strip() # We include a .strip() to ignore the trailing '\n'
    
    kmer_indices = [random.randint(0, len(read) - k + 1) for _ in range(kmer_per_read)]
    for i in kmer_indices:
      out.write(f'{read[i:i+k]},T\n')

    # Need to read in 3 more lines due to the fastq file format
    read = f.readline()
    read = f.readline()
    read = f.readline()

  # Now randomly generate k-mers not in the hash table
  num_neg_generated = 0
  while (num_neg_generated < num_neg):
    kmer = generate_kmer(k)
    if in_dataset(data_file, reads, kmer):
      continue
    out.write(f'{kmer},F\n')
    num_neg_generated += 1
    read = f.readline()
    read = f.readline()
    read = f.readline()

  f.close()
  out.close()
    
if __name__=="__main__":
  main()
