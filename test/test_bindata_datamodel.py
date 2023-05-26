"""test_bindata_datamodel.py

Test the BinData data model methods.
"""

import itertools
import os.path
import pytest
import sys

# Prepare for relative imports.
ROOTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOTDIR)

from bindata import BinData, Base64String, HexString


EQUALS = [
    BinData(b"Hello, World!"),
    Base64String("SGVsbG8sIFdvcmxkIQ=="),
    HexString("48656C6C6F2C20576F726C6421"),
]

NOT_EQUALS = [
    BinData(b"hello, world!"),
    Base64String("aGVsbG8sIHdvcmxkIQ=="),
    HexString("68656C6C6F2C20776F726C6421"),
]


class TestDataModel(object):
    @pytest.mark.parametrize("lhs, rhs", itertools.product(EQUALS, EQUALS))
    def test_equals(self, lhs: BinData, rhs: object) -> None:
        assert lhs == rhs
        assert rhs == lhs

    @pytest.mark.parametrize("lhs, rhs", itertools.product(EQUALS, NOT_EQUALS))
    def test_not_equals(self, lhs: BinData, rhs: object) -> None:
        assert lhs != rhs
        assert rhs != lhs

    @pytest.mark.parametrize("xor1, xor2, expected", [
        # Basic tests.
        *[("00", f"0{c}", f"0{c}") for c in "0123456789ABCDEF"],
        *[(f"0{c}", "00", f"0{c}") for c in "0123456789ABCDEF"],
        *[(f"0{c}", f"0{c}", "00") for c in "0123456789ABCDEF"],

        # Slightly more interesting.
        ("55", "AA", "FF"),
        ("FF", "03", "FC"),
        ("FF", "C0", "3F"),

        # Challenge 2.
        (
            "1c0111001f010100061a024b53535009181c",
            "686974207468652062756c6c277320657965",
            "746865206b696420646f6e277420706c6179"
        ),
    ])
    def test_xor(self, xor1: str, xor2: str, expected: str) -> None:
        x1 = HexString(xor1)
        x2 = HexString(xor2)
        e = HexString(expected)

        assert x1 ^ x2 == e


