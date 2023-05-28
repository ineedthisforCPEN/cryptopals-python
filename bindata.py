"""bindata.py

Implementation of BinData, a binary data storage class. Provides
utilities for various basic cryptography functions and data
conversions.
"""

import itertools
import re
import string


ALPHABET_BASE64 = \
    string.ascii_uppercase + string.ascii_lowercase + string.digits + "+/"
BIT_COUNTS = bytes(bin(x).count("1") for x in range(256))


class BinData(object):
    """Base data object which contains all conversion and data model
    methods.
    """
    def __init__(self, data: bytes) -> None:
        if not isinstance(data, bytes):
            dtype = type(data).__name__
            raise TypeError(f"BinData cannot be initialized with '{dtype}' type")

        self._data = data

    def __repr__(self) -> str:
        return self.to_hexstring()

    def __str__(self) -> str:
        return self._data.decode("ascii")

    ## Data mode - sequence.
    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, key: int|slice) -> "BinData":
        if isinstance(key, int):
            return BinData(bytes([self._data[key]]))
        return BinData(self._data[key])

    ## Data model - comparison.
    def __eq__(self, other: object):
        if isinstance(other, BinData):
            return self._data == other._data
        return False

    def __ne__(self, other: object):
        return not self.__eq__(other)

    ## Data model - numeric operators.
    def __add__(self, other: object) -> "BinData":
        if not isinstance(other, BinData):
            dtype = type(other).__name__
            raise TypeError(f"Unsupported operand type(s) for +: 'BinData' and '{dtype}'")

        return BinData(self._data + other._data)

    def __iadd__(self, other: object) -> "BinData":
        if not isinstance(other, BinData):
            dtype = type(other).__name__
            raise TypeError(f"Unsupported operand type(s) for +: 'BinData' and '{dtype}'")

        self._data += other._data
        return self

    def __xor__(self, other: object) -> "BinData":
        if not isinstance(other, BinData):
            dtype = type(other).__name__
            raise TypeError(f"Unsupported operand type(s) for ^: 'BinData' and '{dtype}'")

        xored = bytes([x ^ y for x, y in zip(self._data, itertools.cycle(other._data))])
        return BinData(xored)

    ## Cryptogaphy methods.
    def hamming_distance(self, other: "BinData") -> int:
        """Calculate the Hamming distance between two chunks of data.
        The two chunks must be the same size (in bytes).

        Parameters:
            other   Other BinData used to calculate Hamming distance

        Returns:
            Returns the Hamming distance between this object and the
            'other' object.
        """
        if len(self._data) != len(other._data):
            raise ValueError("Cannot calculate Hamming distance for BinData objects with different lengths.")

        diff = self ^ other
        return sum(BIT_COUNTS[d] for d in diff._data)

    ## Convertsion methods.
    def to_base64(self) -> str:
        """Convert binary data to its base64 equivalent.

        Returns:
            Returns the equivalent base64 string.
        """
        base64string = ""
        remainder = len(self._data) % 3
        chunks = [self._data[i:i+3] for i in range(0, len(self._data) - remainder, 3)]

        for chunk in chunks:
            raw = int.from_bytes(chunk, "big")

            base64string += ALPHABET_BASE64[(raw & 0xFC0000) >> 18]
            base64string += ALPHABET_BASE64[(raw & 0x03F000) >> 12]
            base64string += ALPHABET_BASE64[(raw & 0x000FC0) >>  6]
            base64string += ALPHABET_BASE64[(raw & 0x00003F) >>  0]

        if remainder == 1:
            raw = int.from_bytes(self._data[-1:], "big")
            base64string += ALPHABET_BASE64[(raw & 0xFC) >> 2]
            base64string += ALPHABET_BASE64[(raw & 0x03) << 4]
        elif remainder == 2:
            raw = int.from_bytes(self._data[-2:], "big")
            base64string += ALPHABET_BASE64[(raw & 0xFC00) >> 10]
            base64string += ALPHABET_BASE64[(raw & 0x03F0) >>  4]
            base64string += ALPHABET_BASE64[(raw & 0x000F) <<  2]
        base64string += "=" * ((3 - remainder) % 3)

        return base64string

    def to_bytes(self) -> bytes:
        """Convert the data to its bytes equivalent.

        Returns:
            Returns the equivalent bytes object.
        """
        return self._data

    def to_hexstring(self) -> str:
        """Convert the data to its hexstring equivalent.

        Returns:
            Returns the equivalent hex string.
        """
        return "".join([f"{i:02X}" for i in self._data])

    def to_string(self, encoding="ascii") -> str:
        """Convert the data to its string equivalent with the
        specified encoding type.

        Parameters:
            encoding    String encoding method (default: ascii)

        Returns:
            Returns the equivalent encoded string.
        """
        return self._data.decode("ascii")


class Base64String(BinData):
    def __init__(self, data: str) -> None:
        if re.match(r"[0-9a-zA-Z+/]+", data) is None:
            raise ValueError("Invlid character(s) in base64 string.")
        if len(data) % 4 != 0:
            raise ValueError("Given base64 string length is not a multiple of 4.")

        binary = b""
        data = data.rstrip("=")
        chunks = [data[i:i+4] for i in range(0, len(data), 4)]

        for chunk in chunks:
            raw = 0
            for c in chunk:
                raw = (raw << 6) | ALPHABET_BASE64.index(c)

            raw >>= (8 - 2*len(chunk))
            binary += raw.to_bytes(len(chunk) - 1, "big")

        super().__init__(binary)


class HexString(BinData):
    def __init__(self, data: str) -> None:
        if re.match(r"[0-9a-fA-F]+", data) is None:
            raise ValueError("Invalid character(s) in hex string")
        if len(data) % 2 != 0:
            raise ValueError("Given hex string length is not a multiple of 2")

        chunks = [data[i:i+2] for i in range(0, len(data), 2)]
        binary = bytes([int(chunk, 16) for chunk in chunks])

        super().__init__(binary)


class String(BinData):
    def __init__(self, data: str, encoding: str = "ascii") -> None:
        super().__init__(data.encode(encoding))

