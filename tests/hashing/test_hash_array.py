import numpy as np

from warden_spex.hashing.hash_array import check_validity, hash_array


def test_hash_array():
    """
    Test: We can assess the similarity of arrays ignoring small differences.
    """
    epsilon = 0.0001
    a1 = np.array([0.0015001, 0.05])
    a2 = np.array([0.0015001 + epsilon, 0.05])
    a3 = np.array([0.0015001 + 1, 0.05])

    h1 = hash_array(a1, epsilon=epsilon)
    h2 = hash_array(a2, epsilon=epsilon)
    h3 = hash_array(a3, epsilon=epsilon)

    assert check_validity(h1, h2) is True
    assert check_validity(h1, h3) is False
