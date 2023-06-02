"""test_bindata_algorithms.py

Test the BinData cryptography algorithms.
"""

import os.path
import pytest
import sys

# Prepare for relative imports.
ROOTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOTDIR)

from algorithms.aes import AesCipher
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


class TestAesAlgorithms(object):
    @pytest.mark.parametrize("plaintext, padded, blocksize", [
        (b"", 4*b"\x04", 4),
        (b"0", b"0\x03\x03\x03", 4),
        (b"01", b"01\x02\x02", 4),
        (b"012", b"012\x01", 4),
        (b"0123", b"0123", 4),
        (b"01234", b"01234\x03\x03\x03", 4),
        (b"012345", b"012345\x02\x02", 4),
        (b"0123456", b"0123456\x01", 4),
        (b"01234567", b"01234567", 4),

        (b"01234567", b"01234567" + 8*b"\x08", 16),
        (b"012345678", b"012345678" + 7*b"\x07", 16),
        (b"0123456789", b"0123456789" + 6*b"\x06", 16),
        (b"0123456789A", b"0123456789A" + 5*b"\x05", 16),
        (b"0123456789AB", b"0123456789AB" + 4*b"\x04", 16),
        (b"0123456789ABC", b"0123456789ABC" + 3*b"\x03", 16),
        (b"0123456789ABCD", b"0123456789ABCD" + 2*b"\x02", 16),
        (b"0123456789ABCDE", b"0123456789ABCDE" + 1*b"\x01", 16),
        (b"0123456789ABCDEF", b"0123456789ABCDEF", 16),

        # Challenge 9.
        (b"YELLOW SUBMARINE", b"YELLOW SUBMARINE\x04\x04\x04\x04", 20),
    ])
    def test_pkcs7_padding(
            self,
            plaintext: bytes,
            padded: bytes,
            blocksize: int
    ) -> None:
        assert AesCipher.pkcs7(plaintext, blocksize) == padded

