import numpy as np

from warden_spex.hashing.hash_int import hash_int


def test_hash_int():
    """
    Test: We can hash an int value.
    """

    h = hash_int(np.array([123], dtype=np.int64))
    assert h == 105266548169393929222442971458088679220
