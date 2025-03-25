from itertools import combinations

import numpy as np
from numpy.typing import NDArray
from scipy.spatial.distance import euclidean

from warden_spex.hashing.hash_int import hash_int


def hash_embedding_m(A: NDArray[np.float64], V: NDArray[np.float64]) -> set[int]:
    """
    HashEmbeddingM:
    Implementation of the SPEX-LSH-M algorithm. Given an array A and a set of vantage points V,
    returns a set of hashes that represent A based on its distance ranking relative to the vantage points.
    """

    # Compute the set of distances D
    D = [euclidean(A, v) for v in V]

    # Generate index pairs (j, k) for unique combinations where j < k
    I = list(combinations(range(len(D)), 2))  # noqa: E741

    # Compute comparisons of all possible inequalities
    C = [(2 * i + (D[j] < D[k])) for i, (j, k) in enumerate(I)]

    # Hash comparisons
    return {hash_int(c) for c in C}


def jaccard_index(X: set[int], Y: set[int]) -> np.float64:
    """
    Compute Jaccard index of sets represented by arrays X and Y.
    """

    intersection = len(X & Y)
    union = len(X | Y)

    return np.float64(intersection / union if union != 0 else 0)
