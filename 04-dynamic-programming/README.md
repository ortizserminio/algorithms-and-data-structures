# 04 · Dynamic programming: number of combinations C(n, k)

Language: **C++14**. Source: *Metodología de la Programación Avanzada*, practical 3.2 and exam.

**Problem.** Count the ways to choose `k` elements out of `n`, for `0 ≤ k ≤ n`.

## Plain recursion: `binomial_recursive`

Pascal's rule: `C(n, k) = 1` if `k = 0` or `k = n`, otherwise `C(n−1, k−1) + C(n−1, k)`.

It is short and obviously correct, but it recomputes the same subproblems again and again. `C(n−2, k−1)` alone is reached from two different parents. Every leaf of the call tree returns 1, so there are exactly `C(n, k)` leaves and **`2·C(n, k) − 1` calls** in total. The tests verify this count for every `n ≤ 16`. For `k = n/2` that is **Θ(2ⁿ/√n)**, exponential in `n`. Stack depth is O(n).

`binomial_trace` prints the indented call tree, which makes the repeated work visible. For `C(4, 2)`, `combinaciones_traza(2,1)` appears twice.

## Dynamic programming: `binomial_dp`

1. Build a table `M[0..n][0..k]`.
2. Fill the borders: `M[i][0] = 1` and `M[i][i] = 1`.
3. Row by row, for `i = 2..n`, set `M[i][j] = M[i−1][j−1] + M[i−1][j]` for `1 ≤ j < i` and `j ≤ k`.
4. The answer is `M[n][k]`.

Each cell is computed **once**, from two cells of the previous row, so time is **Θ(n·k)** and space is **Θ(n·k)**.

## Why DP, and possible improvements

The problem has both ingredients DP needs: **optimal substructure** (the answer is built from answers to smaller instances) and **overlapping subproblems** (the recursion repeats them). The DP table replaces exponential time with polynomial time.

Improvements I did not need for the exercise:
- Each row only uses the previous one, so space can drop to **O(k)** by keeping a single row and filling it right to left.
- `C(n, k) = n! / (k!(n−k)!)` can be computed in O(k) multiplications with the multiplicative formula, but intermediate values overflow `int` quickly.

With 32-bit `int`, results overflow beyond about `C(33, 16)`. The tests stay below that.

## Run and test

```bash
make test
make demos
./build/04-dynamic-programming/binomial_main     # prints the trace when n <= 6
```

Tests check known values (`C(0,0)`, `C(10,5) = 252`, `C(30,15) = 155117520`). They also check that recursion and DP agree for all `n ≤ 18`, the symmetry `C(n,k) = C(n,n−k)`, the call-count formula and the trace format.
