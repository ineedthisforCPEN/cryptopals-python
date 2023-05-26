"""test_bindata_constructors.py

Test the BinData object constructor.
"""

import os.path
import pytest
import sys

from typing import Any

# Prepare for relative imports.
ROOTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOTDIR)

from bindata import BinData, Base64String, HexString


class TestBinData(object):
    @pytest.mark.parametrize("data", [
        0, 0.0, "zero", [0], {0: 0},
    ])
    def test_constructor_invalid(self, data: Any) -> None:
        with pytest.raises(TypeError):
            _ = BinData(data)

    @pytest.mark.parametrize("data", [
        *[bytes([i]) for i in range(0, 256, 16)],
        *[bytes([i, i]) for i in range(0, 256, 16)],
        *[bytes([i, i, i, i]) for i in range(0, 256, 16)],
    ])
    def test_constructor_valid(self, data: bytes) -> None:
        _ = BinData(data)


class TestBase64String(object):
    @pytest.mark.parametrize("data", [
        # Invalid lengths.
        *["0" * i for i in range(1, 33, 4)],
        *["0" * i for i in range(2, 33, 4)],
        *["0" * i for i in range(3, 33, 4)],

        # Invalid characters.
        "ThisIsAllValidSoFar?",
        "No Spaces Allowed!",
    ])
    def test_constructor_invalid(self, data: str) -> None:
        with pytest.raises(ValueError):
            _ = Base64String(data)

    @pytest.mark.parametrize("data", [
        "AA==", "AAA=", "AAAA",
    ])
    def test_constructor_valid(self, data: str) -> None:
        _ = Base64String(data)


class TestHexString(object):
    @pytest.mark.parametrize("data", [
        *["0" * i for i in range(1, 33, 2)],            # Uneven length
        *[f"{c}g" for c in "0123456789abcdefABCDEF"],   # One invalid char
    ])
    def test_constructor_invalid(self, data: str) -> None:
        with pytest.raises(ValueError):
            _ = HexString(data)

    @pytest.mark.parametrize("data", [
        *[2*c for c in "0123456789"],   # Test digits
        *[2*c for c in "abcdef"],       # Test lowercase
        *[2*c for c in "ABCDEF"],       # Test uppercase
        "0123456789abcdef",
        "0123456789ABCDEF",
        "0123456789abcdefABCDEF",
    ])
    def test_constructor_valid(self, data: str) -> None:
        _ = HexString(data)

