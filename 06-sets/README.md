# 06 · Sets as bit vectors

**English** · [Español](README.es.md)

Language: **Python 3.10+**. Source: *Estructuras de Datos*, topic 4 ("TAD Conjunto") exercise.

**Problem.** Represent subsets of a small universe `{0, …, size−1}` and implement union, intersection, difference, symmetric difference, membership, insertion and removal.

## Approach

Store the whole set in **one integer**: element `i` is in the set when bit `i` is 1. For example, `{1, 2, 4}` over 8 elements is `0b00010110`.

The course asked for the operations to be written **bit by bit**, as a set of 0/1 flags would be handled in pseudocode. For each position `i`, read `a = (A >> i) & 1` and `b = (B >> i) & 1`, then combine them:

| Operation | Rule for bit `i` |
|---|---|
| Union | `max(a, b)` |
| Intersection | `a · b` |
| Difference A − B | `a and not b` |
| Symmetric difference | `a xor b` |

`add(i)` adds `2^i` only if bit `i` is 0, and `remove(i)` subtracts it only if it is 1, so both are idempotent.

## Complexity, and why a bit vector

| | Bit vector (this) | Hash set (`set`) | Sorted list |
|---|---|---|---|
| Membership / add / remove | **O(1)** | O(1) average | O(log n) / O(n) |
| Union, intersection… | **O(size)** with the bit loop, one machine instruction per word with `\|`, `&`, `^` | O(len A + len B) | O(len A + len B) |
| Space | **size bits** | ~dozens of bytes per element | one slot per element |

Bit vectors win when the universe is small and dense: permissions, flags, chess boards, bloom filters. They lose when the universe is huge and the set sparse (e.g. arbitrary 64-bit ids), where a hash set is the right choice.

## Fixes over the original exercise

The original `Conjuntos.py` could not run. The fix is in a single commit that lists each problem:
1. All methods were indented *inside* `__init__`, so instances had none of them.
2. A typo, `max_elemetos`, raised `AttributeError` in every operation.
3. `contains` and `add` accepted `num == size`, one past the universe. The bounds are now `0 ≤ num < size`.

## Run and test

```bash
python -m pytest 06-sets
python 06-sets/bitset.py
```

The 14 tests compare all four operations with Python's `set` on 200 random pairs, and cover empty and full sets, out-of-universe values, idempotent add, other universe sizes and the identity `A − B = A ∩ (U − B)`.
