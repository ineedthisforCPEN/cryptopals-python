"""test_bindata_conversion.py

Test the BinData conversion methods.
"""

import os.path
import pytest
import sys

# Prepare for relative imports.
ROOTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOTDIR)

from bindata import Base64String, HexString


class TestSet1(object):
    def test_challenge1(self) -> None:
        """Convert a hex string into a base64 string."""
        hexstring = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
        base64string = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"

        assert HexString(hexstring).to_base64() == base64string
        assert HexString(hexstring) == Base64String(base64string)

    def test_challenge2(self) -> None:
        """XOR two hex strings together."""
        x1 = HexString("1c0111001f010100061a024b53535009181c")
        x2 = HexString("686974207468652062756c6c277320657965")
        expected = HexString("746865206b696420646f6e277420706c6179")

        assert x1 ^ x2 == expected

