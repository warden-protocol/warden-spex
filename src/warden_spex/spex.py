import base64
import logging
from collections.abc import Iterable

import numpy as np
from rbloom import Bloom  # pylint: disable=no-name-in-module

from warden_spex.hashing.hash_int import hash_int
from warden_spex.models import SolverProof

log = logging.getLogger(__name__)


class InvalidValueException(Exception): ...


class Blossom:
    """
    Bloom filter with additional capabilities used by SPEX.
    """

    def __init__(
        self,
        expected_items: int = 1000,
        false_positive_rate: float = 0.01,
    ):
        """
        Create a Bloom filter with a certain number of expected items inserted, and
        an acceptable false positive rate.
        """

        self.inserted_items = 0
        self.expected_items = expected_items

        self.bloom = Bloom(
            expected_items=expected_items,
            false_positive_rate=false_positive_rate,
            hash_func=hash_int,
        )

    def dump(self) -> bytes:
        """
        Serialize Bloom filter to a Base64 sequence of bytes.
        """
        return base64.b64encode(self.bloom.save_bytes())

    def is_hit(self, array: np.ndarray) -> bool:
        """
        Return True if the input `array` is a hit in the Bloom filter.
        """
        return array in self.bloom

    def add(self, array: np.ndarray):
        """
        Add `array` to the Bloom filter.
        """
        if self.inserted_items + 1 > self.expected_items:
            raise InvalidValueException("Bloom filter is full, increase `expected_items`")
        self.inserted_items += 1
        self.bloom.add(array)

    def add_items(self, items: Iterable):
        """
        Add `items` to the Bloom filter.
        """

        for item in items:
            self.add(item)

    @classmethod
    def load(cls, proof: SolverProof):
        """
        Load `proof` Bloom filter.
        """
        blossom = cls()
        blossom.bloom = Bloom.load_bytes(base64.b64decode(proof.bloomFilter), hash_func=hash_int)
        blossom.inserted_items = proof.countItems
        return blossom

    def estimate_false_positive_rate(self):
        """
        Estimate the false positive rate of the current Bloom filter.
        """
        hits = 0
        n = 100000

        rng = np.random.default_rng()
        random_ints = rng.integers(low=1, high=2**32, size=n)
        for i in range(n):
            hits += random_ints[i] in self.bloom

        estimated = hits / n
        return estimated

    def verify_false_positive_rate(self, expected_rate=0.01, tolerance=0.01):
        """
        Decide if the estimated false positive rate is consistent with the expected value.
        """
        estimated = self.estimate_false_positive_rate()
        logging.debug(f"estimated={estimated} expected={expected_rate} tolerance={tolerance}")
        return expected_rate + tolerance >= estimated
