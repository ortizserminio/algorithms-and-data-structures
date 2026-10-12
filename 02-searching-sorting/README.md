# 02 · Searching and sorting: counting occurrences, insertion sort

Language: **C++14**. Source: *Metodología de la Programación Avanzada*, practicals 1 and 2.

Vectors are **1-indexed** (positions `1..n`, slot `0` unused) to match the course pseudocode. The tests check that slot 0 is never touched.

## Counting occurrences: [`count_occurrences.hpp`](count_occurrences.hpp)

**Problem.** Count how many elements of `v[1..n]` are equal to `x`.

**Approach.** Walk the vector once and increment a counter on every match.

**Complexity analysis (the point of the practical).** The demo builds three input vectors: all elements equal to `x`, none equal, and half equal. For this algorithm the three cases cost the same, because every element must be inspected whatever its value. Best, worst and average case are all **Θ(n)** time with **O(1)** extra space. Searching for the *first* occurrence would be different: there the best case is O(1).

## Insertion sort: [`insertion_sort.hpp`](insertion_sort.hpp)

**Problem.** Sort `v[1..n]` in ascending order, in place.

**Approach.**
1. Treat `v[1..i−1]` as already sorted, starting with `i = 2`.
2. Save `x = v[i]`, then shift every element of the prefix that is *greater* than `x` one position to the right.
3. Drop `x` into the gap and continue with `i + 1`.

**Complexity.**

| Input | Inner-loop shifts | Time |
|---|---|---|
| Already sorted (best) | 0 per element | **Θ(n)** |
| Random (average) | about i/2 per element | **Θ(n²)** |
| Reverse sorted (worst) | i − 1 per element | **Θ(n²)** |

Extra space is **O(1)**. The sort is **stable**, because only strictly greater elements are moved.

**Why insertion sort, and when not?** It is simple, in place, stable and *adaptive*: it is linear on nearly sorted data. That is why real-world sorts such as Timsort and introsort switch to it for small partitions. For large random inputs, an O(n log n) algorithm (merge sort, heap sort, quicksort) is the right choice. The demo times all three cases, and the quadratic growth is easy to see by doubling `n`.

## Run and test

```bash
make test
make demos
./build/02-searching-sorting/count_occurrences_main
./build/02-searching-sorting/insertion_sort_main
```

Tests cover empty and single-element vectors, best, worst and average inputs, duplicates, negative numbers and 200 random vectors checked against `std::sort`.

> A bug in the original practical's `main()` (the best-case vector was never printed) was fixed in its own commit. See the history of `count_occurrences_main.cpp`.
