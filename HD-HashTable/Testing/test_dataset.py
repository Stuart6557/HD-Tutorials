# THIS IS INCOMPLETE

# This file extracts all k-mers from the reads in a given fastq file and adds them to a hash table.
# It then calculates and prints the accuracy of the constructed hash table.

from HDHashTable import HDHashTable
import argparse
import random

DNA_bases = ['A', 'C', 'G', 'T']

def generate_kmer(k):
  """
  Generates a k-mer of length k
  """
  kmer = ''
  for _ in range(k):
    kmer += random.choice(DNA_bases)
  return kmer

def main():
  # Get data_file, D, and k from command input
  parser = argparse.ArgumentParser()
  parser.add_argument('--path', action='store', type=str, help='path to fastq data file', required=True)
  parser.add_argument('--D', action='store', type=int, default=10000, help='number of dimensions in the encoded hypervector (default is 10000)')
  parser.add_argument('--k', action='store', type=int, default=501, help='length of a k-mer (should be odd, default is 501)')
  
  inputs = parser.parse_args()
  data_file = inputs.path
  D = inputs.D
  k = inputs.k

  # Initialize hash table
  # Note: k should be odd because this is what LJA requires (see jumbodbg_manual.md)
  hash_table = HDHashTable(k=k, D=D)

  data_train = set() # Contains all kmers in the hash table. Need this to generate test set later on
  data_test_pos = [] # Contains a random sample of kmers in the input data
  data_test_neg = [] # Contains kmers not in the input data

  # Build the hash table
  f = open(data_file, 'r')
  num_kmers = 0
  read = f.readline()
  while read != '':
    # Need to read the next line due to the way fastq files are structured
    # For more information, check out this Illumina page:
    #   https://knowledge.illumina.com/software/general/software-general-reference_material-list/000002211
    read = f.readline()[:-1] # We include a [:-1] to ignore the '\n'
    # Extract all k-mers of length k from the read and add them to our hash table
    for i in range(len(read) - k):
      kmer = read[i:i+k]
      hash_table.add(kmer)
      num_kmers += 1
      print(f"{num_kmers} {kmer}")
      # Randomly add around 1/10 of kmers to testing data
      if random.random() < 0.1:
        data_test_pos.append(kmer)
    # Need to read in 3 more lines due to the fastq file format
    read = f.readline()
    read = f.readline()
    read = f.readline()
  f.close()

  # Generate testing set of around 100 random k-mers
  for _ in range(100):
    kmer = generate_kmer(k)
    # In the offchance that a generated k-mer is actually in the hash table, skip
    if kmer in data_train:
      continue
    data_test_neg.append(kmer)

  # Testing
  true_pos = 0
  true_neg = 0
  total_pos = 0
  total_neg = 0
  for kmer in data_test_pos:
    query_result = hash_table.query(kmer)
    total_pos += 1
    if (query_result):
      true_pos += 1
  for kmer in data_test_neg:
    query_result = hash_table.query(kmer)
    total_neg += 1
    if (not query_result):
      true_neg += 1

  # Print results
  print(f'{num_kmers=}')
  print(f'\nCorrectly identified {true_pos} / {total_pos} {k}-mers that were in the hash table')
  print(f'Accuracy: {true_pos / total_pos * 100:.2f}%\n')
  print(f'Correctly identified {true_neg} / {total_neg} {k}-mers that were not in the hash table')
  print(f'Accuracy: {true_neg / total_neg * 100:.2f}%\n')
  print(f'Total Accuracy: {(true_pos + true_neg) / (total_pos + total_neg) * 100:.2f}%')

if __name__ == '__main__':
  main()
