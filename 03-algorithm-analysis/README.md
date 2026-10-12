# 03 · Algorithm analysis: maximum subarray sum, O(n³) vs O(n)
n**English** · [Español](README.es.md)

Language: **C++14**. Source: *Metodología de la Programación Avanzada* exam (solved in a team).

**Problem.** Given `v[1..n]`, possibly with negative values, find positions `i ≤ j` that maximise `v[i] + … + v[j]`. Convention: the empty subarray is allowed, so the answer is never negative. If every element is negative, both functions return `0` with positions `0..0`.

## Algorithm 1: brute force, [`max_subarray_cubic`](max_subarray.hpp)

1. For every start `i` and every end `j ≥ i`:
2. sum `v[i..j]` from scratch with a third loop, and
3. keep the best sum and its positions.

**Complexity.** The innermost loop runs Σᵢ Σⱼ (j − i + 1) ≈ n³/6 times, so time is **Θ(n³)** and extra space is **O(1)**.

## Algorithm 2: single pass, [`max_subarray_linear`](max_subarray.hpp)

1. Keep `this_sum`, the sum of the current candidate subarray that starts at `i`.
2. Add `v[j]`. If this beats the best so far, record `(i, j)`.
3. If `this_sum` drops below 0, that prefix can only *lower* any subarray that extends it. So discard it: restart with `i = j + 1` and `this_sum = 0`.

This is the idea behind Kadane's algorithm.

**Complexity.** Each element is visited once, so time is **Θ(n)** and extra space is **O(1)**.

## Why the linear algorithm?

An intermediate O(n²) solution exists: fix `i` and extend `j` with a running sum. Divide and conquer gives O(n log n). The single pass is optimal, because any correct algorithm must read every element. It also needs no extra memory. The brute force is still useful as a simple, obviously-correct **reference** for testing.

The demo shows the gap on the same random vector:

| n | O(n³) | O(n) |
|---|---|---|
| 3 000 | ~1.3 s | < 1 ms |
| 5 000 | ~5.4 s | < 1 ms |

(Measured on my laptop with MinGW g++ 6.3 `-O2`. The cubic time grows about 4.2× from 3 000 to 5 000, close to the predicted (5/3)³ ≈ 4.6×.)

## Run and test

```bash
make test
make demos
./build/03-algorithm-analysis/max_subarray_main
```

The tests use the classic example `−2 1 −3 4 −1 2 1 −5 4`, whose answer is 6 at positions 4..7. They cover the empty vector, all-negative and all-positive vectors, and a single element. They also check 300 random vectors against an independent O(n²) reference and verify that the reported positions really add up to the reported sum.

> A bug in the original exam code (the O(n) timing used integer division and always printed 0 ms) was fixed in its own commit.
