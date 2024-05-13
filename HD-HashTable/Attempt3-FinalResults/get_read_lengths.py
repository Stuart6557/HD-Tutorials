# This file writes all read lengths in a given fastq dataset to read_lengths.txt
# No need to use this file. It's just for a quick sanity check
# 
# python3 get_read_lengths.py --path bacillus-SRR26664315.fastq

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--path', action='store', type=str, help='path to fastq data file', required=True)

inputs = parser.parse_args()
dataset = inputs.path

data = open(dataset, 'r')
out = open('read_lengths.txt', 'w')

read_len = data.readline().strip() # Need .strip() to exclude the trailing '\n'
while read_len != '':
  # Extract the read length
  last_equal_index = read_len.rfind('=')
  read_len = read_len[last_equal_index + 1:]
  read_len = int(read_len)

  out.write(f'{read_len}\n')
  for _ in range(4):
    read_len = data.readline().strip()

data.close()
out.close()