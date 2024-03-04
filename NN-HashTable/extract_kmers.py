# This code extracts all k-mers from a fastq data file and appends them to a list named kmers

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--path', action='store', type=str, help='path to fastq data file', required=True)
parser.add_argument('--k', action='store', type=int, default=501, help='length of a k-mer (should be odd, default is 501)')

inputs = parser.parse_args()
data_file = inputs.path
k = inputs.k

f = open(data_file, 'r')
kmers = []
read = f.readline()
while read != '':
  # Need to read the next line due to the way fastq files are structured
  # For more information, check out this Illumina page:
  #   https://knowledge.illumina.com/software/general/software-general-reference_material-list/000002211
  read = f.readline().strip() # We include a .strip() to ignore the trailing '\n'
  
  # Extract all k-mers of length k from the read and add them to our hash table
  for i in range(len(read) - k + 1):
    kmer = read[i:i+k]
    kmers.append(kmer)
  
  # Need to read in 3 more lines due to the fastq file format
  read = f.readline()
  read = f.readline()
  read = f.readline()

f.close()

for kmer in kmers:
  print(kmer)