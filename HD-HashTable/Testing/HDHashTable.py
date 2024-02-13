# THIS IS INCOMPLETE

# Most of this is copied verbatim from ../Attempt2/HDHashTable
# The difference is that add() now takes in an entire read rather than a single kmer. This allows
# us to take advantage of a significantly more efficient encoding algorithm presented in GenieHD.

from math import ceil, floor
import numpy as np
from numpy import dot
from numpy.linalg import norm

class HDHashTable:
  def __init__(self, k, D):
    """
    Constructor that creates a D-dimensional array to store the contents of the hash table
    Creates an encoding scheme for each of the 4 bases: A, C, G, and T

    Parameters:
      k (int): The length k of a k-mer. All k-mers in the hash table should have the same length
      D (int): The dimension of a hypervector
    """
    # We don't want the dimension to be too small. Otherwise, there's a higher chance that encoded
    # hypervectors will be too similar to each other. Ideally, they should be nearly orthogonal
    if D < 100 * k:
      raise ValueError("Please choose a larger D")

    self.k = k
    self.D = D
    self.hash_table = [0] * D

    # Encoding scheme: each encoding will have half its values be -1 and the other half be 1
    self.encoding_scheme = {}
    A_encoding = [-1] * floor(D/2) + [1] * ceil(D/2)
    np.random.shuffle(A_encoding)
    C_encoding = [-1] * floor(D/2) + [1] * ceil(D/2)
    np.random.shuffle(C_encoding)
    G_encoding = [-1] * floor(D/2) + [1] * ceil(D/2)
    np.random.shuffle(G_encoding)
    T_encoding = [-1] * floor(D/2) + [1] * ceil(D/2)
    np.random.shuffle(T_encoding)
    self.encoding_scheme['A'] = A_encoding
    self.encoding_scheme['C'] = C_encoding
    self.encoding_scheme['G'] = G_encoding
    self.encoding_scheme['T'] = T_encoding

    print("Print dot product between encodings to ensure they're dissimilar enough")
    print(f'A and C: {dot(A_encoding, C_encoding)}')
    print(f'A and G: {dot(A_encoding, G_encoding)}')
    print(f'A and T: {dot(A_encoding, T_encoding)}')
    print(f'C and G: {dot(C_encoding, G_encoding)}')
    print(f'C and T: {dot(C_encoding, T_encoding)}')
    print(f'G and T: {dot(G_encoding, T_encoding)}')
    print()

  def encode(self, kmer):
    """
    Encodes a k-mer into a D-dimensional hypervector
    Follows the algorithm described in the GenieHD paper Minxuan sent:
      https://dl.acm.org/doi/abs/10.5555/3408352.3408378

    Parameters:
      kmer (str): The kmer we want to encode

    Returns:
      D-dimensional hypervector representing the kmer
    """
    if len(kmer) != self.k:
      raise ValueError(f'k-mer must have length {self.k}')
    enc_hv = [1] * self.D
    for i in range(self.k):
      base_enc = self.encoding_scheme[kmer[i]]
      base_enc = np.roll(base_enc, i)
      enc_hv = [a * b for a, b in zip(enc_hv, base_enc)]
    return enc_hv

  def add(self, kmer):
    """
    Adds a new kmer to our hash table. Since there's no way of knowing if it already exists
    in the hash table, we will add it again if it is a duplicate.

    Parameters:
      kmer (str): The k-mer we are adding to the hash table
    """
    if len(kmer) != self.k:
      raise ValueError(f'k-mer must have length {self.k}')
    enc_hv = self.encode(kmer)
    self.hash_table = [sum(x) for x in zip(self.hash_table, enc_hv)]

  def query(self, kmer):
    """
    Returns whether or not the given k-mer is in our hash table

    Parameters:
      kmer (str): The k-mer we are querying

    Returns:
      Whether or not the k-mer exists in the hash table
    """
    enc_hv = self.encode(kmer)
    dot_prod = dot(self.hash_table, enc_hv)
    print(f'dot product for {kmer} is {dot_prod}')
    return dot_prod > self.D / 2
