import itertools
import random

import pytest

from bitset import BitSet


def from_set(values, size=8):
    s = BitSet(size)
    for v in values:
        s.add(v)
    return s


def test_constructor_masks_to_size():
    # 511 = 0b1_1111_1111 has 9 bits; an 8-element universe keeps 8 of them
    assert BitSet(8, 511).bits == 255
    assert BitSet(8, 16).elements() == [4]
    assert BitSet(8).elements() == []


@pytest.mark.parametrize("op, py_op", [
    ("union", set.union),
    ("intersection", set.intersection),
    ("difference", set.difference),
    ("symmetric_difference", set.symmetric_difference),
])
def test_operations_match_python_sets(op, py_op):
    rng = random.Random(7)
    for _ in range(200):
        a = set(rng.sample(range(8), rng.randint(0, 8)))
        b = set(rng.sample(range(8), rng.randint(0, 8)))
        result = getattr(from_set(a), op)(from_set(b))
        assert result.elements() == sorted(py_op(a, b))
        assert result.size == 8


def test_operations_with_empty_and_full_sets():
    empty, full = BitSet(8, 0), BitSet(8, 255)
    assert empty.union(full).elements() == list(range(8))
    assert empty.intersection(full).elements() == []
    assert full.difference(full).elements() == []
    assert full.symmetric_difference(empty).elements() == list(range(8))


def test_add_is_idempotent_and_remove_absent_is_noop():
    s = BitSet(8)
    s.add(3)
    s.add(3)
    assert s.bits == 0b1000
    s.remove(5)
    assert s.bits == 0b1000
    s.remove(3)
    assert s.bits == 0


@pytest.mark.parametrize("value", [-1, 8, 100])
def test_out_of_universe_values_are_ignored(value):
    s = BitSet(8)
    s.add(value)
    assert s.bits == 0
    assert not s.contains(value)
    s.remove(value)
    assert s.bits == 0


def test_contains_and_boundaries():
    s = from_set({0, 7})
    assert s.contains(0) and s.contains(7)
    assert not any(s.contains(i) for i in range(1, 7))


def test_repr_is_zero_padded_binary():
    assert repr(BitSet(8, 0b10010)) == "00010010"
    assert repr(BitSet(4, 0)) == "0000"


def test_other_universe_sizes():
    s = BitSet(16)
    for i in range(0, 16, 3):
        s.add(i)
    assert s.elements() == [0, 3, 6, 9, 12, 15]
    assert all(BitSet(1, v).elements() == ([0] if v & 1 else []) for v in range(4))


def test_de_morgan_style_identity():
    # A - B == A n (U - B)
    universe = BitSet(8, 255)
    for a_bits, b_bits in itertools.product([0, 0b1011, 0b11110000, 255], repeat=2):
        a, b = BitSet(8, a_bits), BitSet(8, b_bits)
        assert a.difference(b).bits == a.intersection(universe.difference(b)).bits
