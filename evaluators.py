"""evaluators.py

Utilities used for evaluating the validity of BinData given some criteria.
All evaluators should return a score (float). The higher the score, the more
likely the provided BinData will match the criteria expected of a given
evaluator. Negative scores should be interpreted as completely invalid and can
be ignored.
"""

import string

from collections import Counter, defaultdict
from collections.abc import Sequence

from bindata import BinData


def __fibonacci_distribution(iterable: Sequence[object]) -> defaultdict[object, float]:
    """Creates a "Fibonacci" distribution for a given iterable. The
    distribution assigns a value to each element, and each element is
    a reversed, normalized Fibonnaci sequenc of the same length as the
    given iterable.

    Parameters:
        iterable    The iterable for which to assign values

    Returns:
        Returns a dictionary where each entry is given a value that
        falls along a normalized Fibonacci sequence.
    """
    if len(iterable) == 0:
        return defaultdict(lambda: 0)
    if len(iterable) == 1:
        return defaultdict(lambda: 0, {iterable[0]: 1.0})

    values = [0, 1]
    for i in range(len(iterable)):
        values.append(values[i-1] + values[i-2])
    values = values[::-1]

    mapping = {iterable[i]: values[i] for i in range(len(iterable))}
    return defaultdict(lambda: 0, mapping)


def evaluate_english(plaintext: BinData) -> float:
    """Evaluate the given plaintext as English text.

    Parameters:
        plaintext   The plaintext to evaluate

    Returns:
        Returns an evaluation score.
    """
    try:
        decoded = str(plaintext)
    except:
        return -1.0

    if any([c not in string.printable for c in decoded]):
        return -1.0

    c_single = Counter(decoded)
    c_double = Counter([decoded[i:i+2] for i in range(len(decoded)-1)])

    c_lower = sum([c_single[c] for c in string.ascii_lowercase])
    c_upper = sum([c_single[c] for c in string.ascii_uppercase])

    SCORE_SINGLE = __fibonacci_distribution("ETAOIN SHRDLU")
    SCORE_DOUBLE = __fibonacci_distribution([
        "LL", "EE", "SS", "OO", "TT", "FF", "RR", "NN", "PP", "CC"
    ])
    SCORE_PAIR = __fibonacci_distribution([
        "TH", "HE", "AN", "RE", "ER", "IN", "ON", "AT", "ND", "ST",
        "ES", "EN", "OF", "TE",
    ])

    score = 0.0
    for letter in c_single:
        score += SCORE_SINGLE[letter.upper()] * c_single[letter]
    for pair in c_double:
        score += SCORE_DOUBLE[pair.upper()] * c_double[pair]
        score += SCORE_PAIR[pair.upper()] * c_double[pair]
    score *= c_lower / max(c_upper, 1)

    return score

