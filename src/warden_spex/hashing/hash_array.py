import numpy as np
from numpy.typing import NDArray

from warden_spex.hashing.hash_int import hash_int


def first_significant_digit_position(a: NDArray[np.float64]) -> NDArray[np.int64]:
    """
    Computes the position of the first significant digit for each element in the array.
    """
    a = np.abs(a)  # Ensure absolute float and use absolute values
    a[a == 0] = np.nan  # Avoid log10 issues with zero
    d = np.floor(np.log10(a))
    return np.abs(np.nan_to_num(d).astype(np.int64))


def custom_arange(a: np.int64, b: np.int64, step: int = 1) -> NDArray[np.int64]:
    """
    Generates an array from a to b (inclusive) with a given step size.
    """
    if a > b:
        a, b = b, a  # Swap values if needed
    return np.arange(a, b + step, step)  # Ensure upper bound inclusion


def hash_array(a: NDArray[np.float64], epsilon: float = 0.0001) -> list[set[int]]:
    """
    HashArray:
    Discretizes the input array within an epsilon range and hashes it to a 128-bit integer.
    Ensures numerical stability by scaling, flooring, and applying modulo within 64-bit limits.
    """
    # Determine the position of the first significant digit in epsilon
    n = first_significant_digit_position(np.array([epsilon]))

    # Compute lower and upper bounds
    a_bounds = np.column_stack((a - epsilon, a + epsilon)).flatten()

    # Discretize the bounds by scaling and flooring
    a_quant = np.floor(a_bounds * 10**n).astype(int)

    # Generate integer ranges for each bound pair.
    a_ranges = [custom_arange(a_quant[i], a_quant[i + 1]).astype(np.int64) for i in range(0, len(a_quant), 2)]

    # Generate hashes for all integers for each range.
    h = [{hash_int(v) for v in a_range} for a_range in a_ranges]
    return h


def check_validity(h1: list[set[int]], h2: list[set[int]]) -> bool:
    """
    Checks whether there is at least one common hash value between corresponding sets in h1 and h2.
    """
    assert len(h1) == len(h2), "Hash lists must have the same length."
    return all(bool(h1[i] & h2[i]) for i in range(len(h1)))
