# This script manually calculates the memory (bytes) of an HD Bloom Filter given certain variables
# 
# python3 calculate_memory.py

reads = 30
k = 501
D = 25000
kmers_per_hv = 1000
dataset = 'bacillus-SRR26664315.fastq'

f = open(dataset, 'r')
data = f.readline().strip() # Need .strip() to exclude the trailing '\n'

num_hvs = 0
kmers_in_last_hv = kmers_per_hv

read_len = None
for i in range(reads):
  if data == '':
    # We've reached the end of the dataset
    print(f'Calculated memory for {i} reads')
    break
  
  # Extract the read length
  last_equal_index = data.rfind('=')
  read_len = data[last_equal_index + 1:]
  read_len = int(read_len)
  # print(read_len) # sanity check

  # Calculate number of kmers
  kmers = read_len - k + 1
  if kmers < 1:
    raise Exception("Error: k is longer than read length")

  # Update variables
  kmers_in_last_hv += kmers
  if kmers_in_last_hv > kmers_per_hv:
    new_hvs = (int) (kmers_in_last_hv / kmers_per_hv)
    kmers_in_last_hv %= kmers_per_hv
    num_hvs += new_hvs

  for _ in range(4):
    data = f.readline()

f.close()

memory = num_hvs * D * 4 # multiply by 4 because ints are 4 bytes each
# Add the memory it takes to save the encoding scheme (k, D, 4 encodings)
memory += 4 + 4 + 4 * D * 4
print(f'Memory (bytes) = {memory}')
