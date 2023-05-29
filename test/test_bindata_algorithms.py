"""test_bindata_algorithms.py

Test the BinData cryptography algorithms.
"""

import os.path
import pytest
import sys

# Prepare for relative imports.
ROOTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOTDIR)

from bindata import HexString


class TestAlgorithms(object):
    @pytest.mark.parametrize("hex1, hex2, distance", [
        ("00", "FF", 8),
        ("0F", "F0", 8),
        ("55", "AA", 8),
        ("FF", "0C", 6),
        ("FF", "03", 6),
        ("FF", "0F", 4),

        # Challenge 6.
        ("7468697320697320612074657374", "776F6B6B6120776F6B6B61212121", 37),
    ])
    def test_hamming_distance(self, hex1: str, hex2: str, distance: int) -> None:
        h1 = HexString(hex1)
        h2 = HexString(hex2)

        assert h1.hamming_distance(h2) == distance
        assert h2.hamming_distance(h1) == distance

    def test_hamming_distance_invalid(self) -> None:
        h1 = HexString("0000")
        h2 = HexString("00")

        with pytest.raises(ValueError):
            _ = h1.hamming_distance(h2)
        with pytest.raises(ValueError):
            _ = h2.hamming_distance(h1)
