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

from bindata import BinData, Base64String, HexString, String


class TestDataModelComparison(object):
    EQUALS = [
        BinData(b"Hello, World!"),
        Base64String("SGVsbG8sIFdvcmxkIQ=="),
        HexString("48656C6C6F2C20576F726C6421"),
        String("Hello, World!"),
    ]

    NOT_EQUALS = [
        BinData(b"hello, world!"),
        Base64String("aGVsbG8sIHdvcmxkIQ=="),
        HexString("68656C6C6F2C20776F726C6421"),
        String("hello, world!"),
    ]

    @pytest.mark.parametrize("lhs, rhs", itertools.product(EQUALS, EQUALS))
    def test_equals(self, lhs: BinData, rhs: object) -> None:
        assert lhs == rhs
        assert rhs == lhs

    @pytest.mark.parametrize("lhs, rhs", itertools.product(EQUALS, NOT_EQUALS))
    def test_not_equals(self, lhs: BinData, rhs: object) -> None:
        assert lhs != rhs
        assert rhs != lhs


class TestDataModelNumeric(object):
    @pytest.mark.parametrize("lhs, rhs, expected", [
        (b"", b"", b""),
        (b"one", b"", b"one"),
        (b"", b"one", b"one"),
        (b"one", b"one", b"oneone"),
        (
            bytes([i for i in range(256)]),
            bytes([i for i in range(256)]),
            2 * bytes([i for i in range(256)])
        )
    ])
    def test_add(self, lhs: bytes, rhs: bytes, expected: bytes) -> None:
        left = BinData(lhs)
        right = BinData(rhs)

        assert left + right == BinData(expected)

    def test_iadd(self) -> None:
        bindata = BinData(b"")
        toadd = String("Hello, world!")

        for i in range(len(toadd)):
            bindata += toadd[i]

            assert bindata[-1] == toadd[i]
            assert bindata == toadd[:i+1]

        assert bindata == toadd

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


class TestDataModelSequence(object):
    def test_getitem(self) -> None:
        original = "Hello, World!"
        bindata = String(original)

        # Test access by index.
        for i in range(len(original)):
            assert bindata[i] == String(original[i])

        # Test access by slice.
        for i in range(2, len(original)):
            assert bindata[0:i] == String(original[0:i])

    @pytest.mark.parametrize("bindata, length", [
        (BinData(b"01234567"), 8),
        (Base64String("01234567"), 6),
        (HexString("01234567"), 4),
        (String("01234567"), 8),
    ])
    def test_len(self, bindata: BinData, length: int) -> None:
        assert len(bindata) == length

