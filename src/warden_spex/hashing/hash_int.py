from hashlib import sha256

import numpy as np
from numpy.typing import NDArray


def hash_int(value: np.int64 | NDArray[np.int64]) -> int:
    """
    Given an array of ints, it returns its _single_ hash.
    """

    # Reduce array to a single int to hash
    v_sum: np.int64 = value if isinstance(value, np.int64) else np.sum(value)

    # Encoding it in a predefined memory layout.
    # "<": Little-endian
    # "u": Unsigned integer
    # "8": 8 bytes (i.e., 64 bits)
    v_mem = np.ascontiguousarray(v_sum.astype("<u8"))

    # Return hash as int in the range expected by rbloom.
    # https://github.com/KenanHanke/rbloom?tab=readme-ov-file#documentation
    v_hash = int.from_bytes(sha256(v_mem.tobytes()).digest()[:16], byteorder="big", signed=True)
    return v_hash
