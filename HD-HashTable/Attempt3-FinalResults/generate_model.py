# This file extracts all k-mers from the reads in a given fastq file and adds them to a bloom filter.
# It then saves model to model.csv where each line is one element of the bloom filter hypervector.
# 
# python3 generate_model.py --path bacillus-SRR26664315.fastq --reads 30

from HDBloomFilter import HDBloomFilter
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
  parser.add_argument('--reads', action='store', type=int, default=20, help='number of reads used to train model')
  parser.add_argument('--D', action='store', type=int, default=10000, help='number of dimensions in the encoded hypervector (default is 10000)')
  parser.add_argument('--k', action='store', type=int, default=501, help='length of a k-mer (should be odd, default is 501)')
  
  inputs = parser.parse_args()
  data_train_file = inputs.path
  reads = inputs.reads
  D = inputs.D
  k = inputs.k

  # Initialize able
  # Note: k should be odd because this is what LJA requires (see jumbodbg_manual.md)
  bloom_filter = HDBloomFilter(k=k, D=D)
  bloom_filter.print_base_enc_dot_prods()

  # Build the bloom filter
  f = open(data_train_file, 'r')
  read = f.readline()
  for i in range(reads):
    # Need to read the next line due to the way fastq files are structured
    # For more information, check out this Illumina page:
    #   https://knowledge.illumina.com/software/general/software-general-reference_material-list/000002211
    read = f.readline().strip() # We include a .strip() to ignore the trailing '\n'
    print(f'encoding read {i+1}')

    # Extract all k-mers of length k from the read and add them to our bloom filter
    bloom_filter.add_read(read)

    # Need to read in 3 more lines due to the fastq file format
    read = f.readline()
    read = f.readline()
    read = f.readline()

  f.close()

  # Save model
  f = open('model.csv', 'w')
  # First save k and D
  f.write(f'{bloom_filter.k}\n')
  f.write(f'{bloom_filter.D}\n')
  # Now the base encodings
  order_of_bases = ['A', 'C', 'G', 'T']
  for base in order_of_bases:
    for val in bloom_filter.encoding_scheme[base]:
      f.write(f'{val} ')
    f.write('\n')
  # Now save the bloom filter hypervectors
  for bloom_filter_hv in bloom_filter.bloom_filter_hvs:
    for entry in bloom_filter_hv:
      f.write(f'{str(entry)} ')
    f.write('\n')
  f.close()

if __name__ == '__main__':
  main()
