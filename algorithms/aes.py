"""aes.py

Implementation of the Advanced Encryption Standard (AES) as defined by NIST in
FIPS-197.
"""


import enum
import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class AesMode(enum.Enum):
    ECB = enum.auto()   # Electronic Code Book mode.
    CBC = enum.auto()   # Cipher Block Chaining mode.
    CFB = enum.auto()   # Cipher FeedBack mode.
    OFB = enum.auto()   # Output FeedBack mode.
    CTR = enum.auto()   # CounTeR mode.


class AesCipher(object):
    def __init__(self, key: bytes, mode: AesMode = AesMode.ECB) -> None:
        iv = os.urandom(16)

        self.mode = {
            AesMode.ECB: modes.ECB(),
            AesMode.CBC: modes.CBC(iv),
            AesMode.CFB: modes.CFB(iv),
            AesMode.OFB: modes.OFB(iv),
            AesMode.CTR: modes.CTR(iv),
        }[mode]
        self.cipher = Cipher(algorithms.AES(key), self.mode)

    def decrypt(self, ciphertext: bytes) -> bytes:
        decryptor = self.cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()

    def encrypt(self, plaintext: bytes) -> bytes:
        encryptor = self.cipher.encryptor()
        return encryptor.update(plaintext) + encryptor.finalize()

