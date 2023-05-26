"""utils.py

Handy functions :)
"""

import requests

from collections.abc import Sequence

from bindata import BinData
from evaluators import evaluate_english


def read_challenge_data(challenge: int) -> str:
    """Download and read any associated data for a given challenge.

    Parameters:
        challenge   Cryptopals challenge number

    Returns:
        Returns the downloaded data as a string.
    """
    url = f"https://cryptopals.com/static/challenge-data/{challenge}.txt"
    res = requests.get(url)

    if res.status_code == 404:
        raise RuntimeError(f"There is no data for challenge {challenge}")
    elif res.status_code != 200:
        raise requests.RequestException(f"Could not read data for challenge {challenge}")

    return res.text


def xor_otp_best_guess(
        ciphertext: BinData,
        keys: Sequence[BinData],
        method: str = "english"
) -> tuple[BinData, BinData|None]:
    """Decrypt the given ciphertext with all available keys and return
    the best guess for the original plaintext along with the key used
    to decrypt the ciphertext. The supported evaluation methods are:

        english     Plaintext looks like English text

    Parameters:
        ciphertext  Ciphertext to decrypt
        keys        List of all possible decryption keys
        method      Evaluation method for the best guess

    Returns:
        Returns the best guess for the decrypted plaintext. Returns
        ("", None) if no valid guesses are found accoring to the
        selected evaluator.
    """
    if method == "english":
        evaluator = evaluate_english
    else:
        raise ValueError(f"Unrecognized evaluation method '{method}'")

    plaintext = [ciphertext ^ k for k in keys]
    scores = [evaluator(p) for p in plaintext]

    best_score = max(scores)
    if best_score < 0:
        return (BinData(b""), None)

    best_guess_index = scores.index(best_score)
    return(keys[best_guess_index], plaintext[best_guess_index])

