"""
My understanding is that, for example, we just simply flatten the image data into a
1D vector. For the hash table with k-mer's, the naive way is to transform each k-mer
to a k-length vector with a value in the range between 0 and 3. Then, you can encode
these k-length vectors using standard encoding methods (e.g., random projection, id-level
encoding, etc.) to get the encoded HD vectors. 

To represent a hash table, I think the naive way is to add all these encoded HD vectors
together to generate a "hash table" HD vector. In this case, you can search a new k-mer
by comparing the similarity of the new k-mer (after encoding) with the "hash-table" HD
vector. If the similarity is large enough, the k-mer may reside in the hash table. This
will definitely bring some inaccuracies for the hash table search, but what we want to
know further is such inaccuracies will significantly decrease the quality of the final
assembly.
"""
