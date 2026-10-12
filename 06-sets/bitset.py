"""Set ADT over a small universe {0, ..., size-1} stored as the bits of an int
(ED, topic 4 "TAD Conjunto", 2025/26).

Element ``i`` belongs to the set when bit ``i`` is 1. The operations are
written bit by bit, as in the course, instead of using Python's ``|``, ``&``
and ``^`` on the whole integer: for bit ``i``, ``a = (bits >> i) & 1`` and
``b = (other.bits >> i) & 1``, and only the combining rule changes:

* union:                max(a, b)
* intersection:         a * b
* difference:           a and not b
* symmetric difference: a xor b

Each set operation is O(size); membership, add and remove are O(1).
Space is one integer of ``size`` bits.
"""
from __future__ import annotations


class BitSet:
    """Set of integers in [0, size) represented by the bits of ``bits``."""

    def __init__(self, size: int = 8, value: int = 0) -> None:
        self.size = size
        # Keep only the lowest `size` bits: (1 << size) - 1 is `size` ones.
        self.bits = value & ((1 << size) - 1)

    def union(self, other: BitSet) -> BitSet:
        result = 0
        for i in range(self.size):
            a = (self.bits >> i) & 1
            b = (other.bits >> i) & 1
            result += (1 << i) * max(a, b)
        return BitSet(self.size, result)

    def intersection(self, other: BitSet) -> BitSet:
        result = 0
        for i in range(self.size):
            a = (self.bits >> i) & 1
            b = (other.bits >> i) & 1
            result += (1 << i) * (a * b)
        return BitSet(self.size, result)

    def difference(self, other: BitSet) -> BitSet:
        result = 0
        for i in range(self.size):
            a = (self.bits >> i) & 1
            b = (other.bits >> i) & 1
            if a and not b:
                result += 1 << i
        return BitSet(self.size, result)

    def symmetric_difference(self, other: BitSet) -> BitSet:
        result = 0
        for i in range(self.size):
            a = (self.bits >> i) & 1
            b = (other.bits >> i) & 1
            if a and not b:
                result += 1 << i
            elif b and not a:
                result += 1 << i
        return BitSet(self.size, result)

    def contains(self, num: int) -> bool:
        """True if ``num`` is in the set; out-of-universe values are never in it."""
        if 0 <= num < self.size:
            return (self.bits >> num) % 2 == 1
        return False

    def elements(self) -> list[int]:
        """Members in increasing order."""
        return [i for i in range(self.size) if (self.bits >> i) & 1]

    def add(self, num: int) -> None:
        """Insert ``num`` (ignored if outside [0, size)). Adds 2^num only if absent."""
        if 0 <= num < self.size:
            self.bits += (1 << num) * (1 - ((self.bits >> num) & 1))

    def remove(self, num: int) -> None:
        """Delete ``num`` if present (ignored if outside [0, size))."""
        if 0 <= num < self.size:
            self.bits -= (1 << num) * ((self.bits >> num) & 1)

    def __repr__(self) -> str:
        """Binary string with the highest element on the left, e.g. '00010010'."""
        return f"{self.bits:0{self.size}b}"


if __name__ == "__main__":
    a = BitSet(8, 0b10110)  # {1, 2, 4}
    b = BitSet(8, 0b01100)  # {2, 3}
    print("A =", a, a.elements())
    print("B =", b, b.elements())
    print("A u B   =", a.union(b).elements())
    print("A n B   =", a.intersection(b).elements())
    print("A - B   =", a.difference(b).elements())
    print("A xor B =", a.symmetric_difference(b).elements())
