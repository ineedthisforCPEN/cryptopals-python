"""test_bindata_conversion.py

Test the BinData conversion methods.
"""

import os.path
import pytest
import sys

from typing import Any

# Prepare for relative imports.
ROOTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOTDIR)

from bindata import BinData, Base64String, HexString


class TestBase64String(object):
    TEST_CASES = [
        # Basic examples, check for correct padding.
        (b"\x00",         "AA=="),
        (b"\x00\x00",     "AAA="),
        (b"\x00\x00\x00", "AAAA"),

        # Test challenge 1.
        (
            b"I'm killing your brain like a poisonous mushroom",
            "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
        ),
    ]

    @pytest.mark.parametrize("binary, base64string", TEST_CASES)
    def test_conversion_from(self, binary: bytes, base64string: str) -> None:
        assert Base64String(base64string)._data == binary

    @pytest.mark.parametrize("binary, base64string", TEST_CASES)
    def test_conversion_to(self, binary: bytes, base64string: str) -> None:
        assert BinData(binary).to_base64() == base64string


class TestHexString(object):
    TEST_CASES = [
        # Basic examples.
        *[(bytes([int(c, 16)]), f"0{c}") for c in "0123456789abcdefABCDEF"],

        # Test challenge 1.
        (
            b"I'm killing your brain like a poisonous mushroom",
            "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
        )
    ]

    @pytest.mark.parametrize("binary, hexstring", TEST_CASES)
    def test_conversion_from(self, binary: bytes, hexstring: str) -> None:
        assert HexString(hexstring.upper())._data == binary
        assert HexString(hexstring.lower())._data == binary

    @pytest.mark.parametrize("binary, hexstring", TEST_CASES)
    def test_conversion_to(self, binary: bytes, hexstring: str) -> None:
        assert BinData(binary).to_hexstring().lower() == hexstring.lower()

