"""test_bindata_conversion.py

Test the BinData conversion methods.
"""

import os.path
import pytest
import string
import sys

# Prepare for relative imports.
ROOTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOTDIR)

from bindata import Base64String, HexString, String
from evaluators import evaluate_english
from utils import read_challenge_data, xor_otp_best_guess


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

    def test_challenge3(self) -> None:
        """Decrypt ciphertext that has been encrypted via XOR one
        time pad with key length 1.
        """
        ciphertext = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
        keys = [String(c) for c in string.ascii_letters + string.digits]
        h = HexString(ciphertext)

        key, plaintext = xor_otp_best_guess(h, keys, method="english")

        assert plaintext is not None
        assert plaintext.to_string() == "Cooking MC's like a pound of bacon"
        assert key.to_string() == "X"

    def test_challenge4(self) -> None:
        """One of the 60-character strings provided has been encrypted
        with a single-character XOR. Find it.
        """
        raw = read_challenge_data(4).strip()
        ciphertext = [HexString(line) for line in raw.split("\n")]

        candidates = []
        keys = [String(c) for c in string.ascii_letters + string.digits]

        for c in ciphertext:
            key, plaintext = xor_otp_best_guess(c, keys, method="english")

            if plaintext is None:
                continue

            score = evaluate_english(plaintext)
            candidates.append((score, key, plaintext))

        candidates.sort(key=lambda x: x[0], reverse=True)
        _, key, plaintext = candidates[0]

        assert plaintext.to_string() == "Now that the party is jumping\n"
        assert key.to_string() == "5"

    def test_challenge5(self) -> None:
        """Encrypt the given phrase via XOR one time pad with a longer
        key.
        """
        plaintext = String(
            "Burning 'em, if you ain't quick and nimble\n" + \
            "I go crazy when I hear a cymbal"
        )
        key = String("ICE")
        expected = HexString(
            "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c" + \
            "2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b" + \
            "2027630c692b20283165286326302e27282f"
        )

        assert plaintext ^ key == expected

