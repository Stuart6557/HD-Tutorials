# python3 inefficientModel.py > inefficient.csv

from inefficientHD import inefficientHD

# Build the model
f = open('model.csv', 'r')
k = int(f.readline().strip()) # Need .strip() to exclude the trailing '\n'
D = int(f.readline().strip())
hash_table = inefficientHD(k=k, D=D)
hash_table.set_A_encoding([int(x) for x in f.readline().strip().split(' ')])
hash_table.set_C_encoding([int(x) for x in f.readline().strip().split(' ')])
hash_table.set_G_encoding([int(x) for x in f.readline().strip().split(' ')])
hash_table.set_T_encoding([int(x) for x in f.readline().strip().split(' ')])
f.close()

f = open('tiny_data.csv', 'r')
kmer = f.readline()[:-1] # We include a [:-1] to ignore the '\n'

while (kmer != ''):
  hash_table.add(kmer)
  kmer = f.readline()[:-1]
f.close()

# print(hash_table.hash_table)

print(hash_table.query('GATAGGCCTATTGATTCGAAGTAAGTACGAAAGGGGTCGGTCAATAGCATAGCTCTTTTTTTTTCTCCTTTCGAAGGAAAGGCCTTCGCATTCCTTAATCTGGTAGGGCCGGACGGCTTTGTTTGCCTAGCTTGGCGAATCGCGCCCCTGACCGTTCTCGCGAAGTCTTTGCAACGGCTGGGAAACCTGTCTACGAAGCTAAGCATATTGCCACGCCGACCATCAAATACAGATATCTGGGCCCCTTCTCAAAGATGGAATGGCCCAGCCCAATAAAGGAAGGTTAACGTACGCGATGCCTTCCATTTGTACGAATCGCGAACATACCACGCACGACCGGACGTAGAGCAAAATTCACTGGCAGACCGAGTCGGGCGCAGGTGCCGGATCCTCAAAGTAAAGTATCCGATCAGCCTAGTGTACCAACCCACGTGGTACGACGGGGCACTCAAAGACCTGGCGAATGAGGGGCCCCACCCCCACCAAGAGCAGCGCTTATGT'))
