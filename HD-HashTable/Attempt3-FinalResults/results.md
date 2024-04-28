## First 30 reads, hash table hypervector for every 500 501-mers

### Attempt to generate model on Minxuan's server

Trying on server
Broadcast message from systemd-journald@zmac (Mon 2024-04-15 00:55:13 PDT):

systemd[1]: Caught <SEGV>, dumped core as pid 16143.


Broadcast message from systemd-journald@zmac (Mon 2024-04-15 00:55:13 PDT):

systemd[1]: Freezing execution.

encoding read 30

real	116m4.225s
user	116m3.413s
sys	0m0.808s

### Generating model
python3 generate_model.py --path bacillus-SRR26664315.fastq --reads 30  1337.63s user 10.27s system 98% cpu 22:41.73 total

### Testing
Correctly identified 158 / 180 501-mers that were in the hash table
Accuracy: 87.78%

Correctly identified 177 / 200 501-mers that were not in the hash table
Accuracy: 88.50%

Total Accuracy: 88.16%
python3 test_model.py --modelPath model.csv --testDataPath data_test.csv  443.70s user 5.18s system 97% cpu 7:39.17 total



## First 40 reads, hash table hypervector for every 500 501-mers

### Generating model
python3 generate_model.py --path bacillus-SRR26664315.fastq --reads 40  1801.06s user 16.12s system 97% cpu 31:12.40 total

### Testing
Correctly identified 168 / 200 501-mers that were in the hash table
Accuracy: 84.00%

Correctly identified 175 / 200 501-mers that were not in the hash table
Accuracy: 87.50%

Total Accuracy: 85.75%
python3 test_model.py --modelPath model.csv --testDataPath data_test.csv  506.10s user 3.14s system 100% cpu 8:29.14 total



## First 50 reads, hash table hypervector for every 500 501-mers

### Generating model
python3 generate_model.py --path bacillus-SRR26664315.fastq --reads 50  2201.16s user 18.89s system 97% cpu 37:58.00 total

### Testing
Correctly identified 171 / 200 501-mers that were in the hash table
Accuracy: 85.50%

Correctly identified 172 / 200 501-mers that were not in the hash table
Accuracy: 86.00%

Total Accuracy: 85.75%
python3 test_model.py --modelPath model.csv --testDataPath data_test.csv  571.88s user 8.79s system 97% cpu 9:53.57 total



## First 100 reads, hash table hypervector for every 500 501-mers

### Generating model
python3 generate_model.py --path bacillus-SRR26664315.fastq --reads 100  4317.61s user 39.01s system 96% cpu 1:15:19.99 total

### Testing
Correctly identified 174 / 200 501-mers that were in the hash table
Accuracy: 87.00%

Correctly identified 144 / 200 501-mers that were not in the hash table
Accuracy: 72.00%

Total Accuracy: 79.50%
python3 test_model.py --modelPath model.csv --testDataPath data_test.csv  782.58s user 12.45s system 85% cpu 15:27.41 total



## First 150 reads, hash table hypervector for every 500 501-mers

### Generating model
python3 generate_model.py --path bacillus-SRR26664315.fastq --reads 150  6222.66s user 40.36s system 87% cpu 1:59:30.53 total

### Testing
Correctly identified 137 / 150 501-mers that were in the hash table
Accuracy: 91.33%

Correctly identified 124 / 200 501-mers that were not in the hash table
Accuracy: 62.00%

Total Accuracy: 74.57%
python3 test_model.py --modelPath model.csv --testDataPath data_test.csv  884.76s user 13.10s system 98% cpu 15:09.51 total



## First 200 reads, hash table hypervector for every 500 501-mers

### Generating model
python3 generate_model.py --path bacillus-SRR26664315.fastq --reads 200  8413.00s user 71.58s system 88% cpu 2:38:59.69 total

3329 lines in model.csv
- 6 = 3323 HVs in hash table

### Testing
Correctly identified 177 / 200 501-mers that were in the hash table
Accuracy: 88.50%

Correctly identified 113 / 200 501-mers that were not in the hash table
Accuracy: 56.50%

Total Accuracy: 72.50%
python3 test_model.py --modelPath model.csv --testDataPath data_test.csv  1154.39s user 33.95s system 98% cpu 20:06.91 total



## First 30 reads, hash table hypervector for every 500 501-mers

### Generating model
python3 generate_model.py --path bacillus-SRR26664315.fastq --reads 30 --k 50  1367.19s user 12.97s system 95% cpu 23:59.95 total

### Testing
Correctly identified 151 / 180 501-mers that were in the hash table
Accuracy: 83.89%

Correctly identified 177 / 200 501-mers that were not in the hash table
Accuracy: 88.50%

Total Accuracy: 86.32%
python3 test_model.py --modelPath model.csv --testDataPath data_test.csv  445.01s user 6.13s system 96% cpu 7:45.57 total



## First 30 reads, hash table hypervector for every 500 1001-mers

### Generating model
python3 generate_model.py --path bacillus-SRR26664315.fastq --reads 30 --k   1308.19s user 10.13s system 97% cpu 22:35.08 total

### Testing
Correctly identified 151 / 180 1001-mers that were in the hash table
Accuracy: 83.89%

Correctly identified 192 / 200 1001-mers that were not in the hash table
Accuracy: 96.00%

Total Accuracy: 90.26%
python3 test_model.py --modelPath model.csv --testDataPath data_test.csv  691.36s user 4.51s system 99% cpu 11:41.41 total



## First 30 reads, hash table hypervector for every 500 2001-mers

### Generating model
python3 generate_model.py --path bacillus-SRR26664315.fastq --reads 30 --k   1180.91s user 10.04s system 98% cpu 20:10.24 total

### Testing
Correctly identified 148 / 180 2001-mers that were in the hash table
Accuracy: 82.22%

Correctly identified 183 / 200 2001-mers that were not in the hash table
Accuracy: 91.50%

Total Accuracy: 87.11%
python3 test_model.py --modelPath model.csv --testDataPath data_test.csv  1195.19s user 7.85s system 99% cpu 20:03.85 total



## First 30 reads, hash table hypervector for every 500 3001-mers

### Generating model
python3 generate_model.py --path bacillus-SRR26664315.fastq --reads 30 --k   1095.05s user 10.68s system 95% cpu 19:18.27 total

### Testing
Correctly identified 154 / 180 3001-mers that were in the hash table
Accuracy: 85.56%

Correctly identified 185 / 200 3001-mers that were not in the hash table
Accuracy: 92.50%

Total Accuracy: 89.21%
python3 test_model.py --modelPath model.csv --testDataPath data_test.csv  1717.16s user 11.37s system 98% cpu 29:06.39 total



## First 30 reads, hash table hypervector for every 500 4001-mers

### Generating model
python3 generate_model.py --path bacillus-SRR26664315.fastq --reads 30 --k   977.93s user 8.60s system 72% cpu 22:48.89 total

### Testing
Correctly identified 152 / 180 4001-mers that were in the hash table
Accuracy: 84.44%

Correctly identified 190 / 200 4001-mers that were not in the hash table
Accuracy: 95.00%

Total Accuracy: 90.00%
python3 test_model.py --modelPath model.csv --testDataPath data_test.csv  2304.55s user 23.34s system 96% cpu 40:08.09 total
