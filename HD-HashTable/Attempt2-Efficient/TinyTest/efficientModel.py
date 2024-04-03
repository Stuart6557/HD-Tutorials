# python3 efficientModel.py > efficient.csv

from efficientHD import efficientHD

# Build the model
f = open('model.csv', 'r')
k = int(f.readline().strip()) # Need .strip() to exclude the trailing '\n'
D = int(f.readline().strip())
hash_table = efficientHD(k=k, D=D)
hash_table.set_A_encoding([int(x) for x in f.readline().strip().split(' ')])
hash_table.set_C_encoding([int(x) for x in f.readline().strip().split(' ')])
hash_table.set_G_encoding([int(x) for x in f.readline().strip().split(' ')])
hash_table.set_T_encoding([int(x) for x in f.readline().strip().split(' ')])
f.close()

f = open('read.fastq', 'r')
read = f.readline()[:-1] # We include a [:-1] to ignore the '\n'
read = f.readline()[:-1]
hash_table.add(read)
f.close()

# print(hash_table.hash_table_hv)
print(hash_table.query('GATAGGCCTATTGATTCGAAGTAAGTACGAAAGGGGTCGGTCAATAGCATAGCTCTTTTTTTTTCTCCTTTCGAAGGAAAGGCCTTCGCATTCCTTAATCTGGTAGGGCCGGACGGCTTTGTTTGCCTAGCTTGGCGAATCGCGCCCCTGACCGTTCTCGCGAAGTCTTTGCAACGGCTGGGAAACCTGTCTACGAAGCTAAGCATATTGCCACGCCGACCATCAAATACAGATATCTGGGCCCCTTCTCAAAGATGGAATGGCCCAGCCCAATAAAGGAAGGTTAACGTACGCGATGCCTTCCATTTGTACGAATCGCGAACATACCACGCACGACCGGACGTAGAGCAAAATTCACTGGCAGACCGAGTCGGGCGCAGGTGCCGGATCCTCAAAGTAAAGTATCCGATCAGCCTAGTGTACCAACCCACGTGGTACGACGGGGCACTCAAAGACCTGGCGAATGAGGGGCCCCACCCCCACCAAGAGCAGCGCTTATGT'))
