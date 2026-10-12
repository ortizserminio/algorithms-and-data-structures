# 01 · Recursion and recursion-to-iteration
n**English** · [Español](README.es.md)

Language: **C++14**. Source: *Metodología de la Programación Avanzada*, practicals 3.1 and 4.

| File | What it does |
|---|---|
| [`binary.hpp`](binary.hpp) | Converts a natural number to binary by recursion; a second version prints the call trace. |
| [`recursion_to_iteration.hpp`](recursion_to_iteration.hpp) | Fast exponentiation and a linear non-tail recursion, each in a recursive version and an iterative one that uses an explicit stack. |
| [`test_recursion.cpp`](test_recursion.cpp) | Tests for both headers. |

## 1. Decimal to binary

**Problem.** Print the binary representation of `n ≥ 0`.

**Approach.**
1. If `n < 2`, the binary digit is `n` itself (base case).
2. Otherwise, first print the binary form of `n div 2`, then print `n mod 2`.

Because the recursive call comes *before* the print, the most significant digit is written first, so no reversing is needed.

**Why recursion here?** The iterative alternative produces the digits in reverse order (least significant first), so it needs a buffer or a stack to print them. The recursion stack does that job for free. With an `int` the depth is at most about 31, so stack overflow is not a concern.

**Complexity.** Each call halves `n`, giving ⌊log₂ n⌋ + 1 calls. Time is **O(log n)** and stack space is **O(log n)**.

`binary_trace` runs the same algorithm and writes a numbered line before every call, e.g. for `n = 10`:

```
1.- binario_traza(10)
2.- binario_traza(5)
3.- binario_traza(2)
4.- binario_traza(1)
1010
```

## 2. Fast exponentiation: recursive → iterative

**Problem.** Compute `xⁿ` for `n ≥ 0`.

**Approach (recursive).** If `n = 0`, return 1. If `n` is odd, return `x · xⁿ⁻¹`. If `n` is even, compute `y = x^(n/2)` and return `y²`.

**Approach (iterative).** The function has *two different* recursive branches, so a plain loop cannot replace it directly. The iterative version simulates the call stack instead:
1. **Going down**, while `n ≠ 0`, push `'I'` and set `n -= 1` if `n` is odd; otherwise push `'P'` and set `n /= 2`.
2. Start from `r = 1`, the base case.
3. **Going up**, pop each marker: `'I'` means `r *= x` and `'P'` means `r = r²`.

**Why this algorithm?** The naive loop `r *= x` repeated `n` times is O(n). Squaring halves the exponent at least every two steps.

**Complexity.** **O(log n)** time, plus **O(log n)** space for either the call stack or the explicit stack.

## 3. Linear non-tail recursion → iterative

`f(x, y) = x + y` if `x ≤ 4`, otherwise `f(x−4, y/3) + (x−4)·(y/3)`.

Work remains *after* the recursive call (adding `x·y`), so this is not tail recursion. The iterative version pushes the already-updated `(x, y)` of every level while going down. On the way up it adds `x·y` for each popped pair. Both versions take **O(x)** time and **O(x)** space.

## Run and test

From the repository root:

```bash
make test                       # builds and runs every C++ test
make demos                      # builds the interactive demos into build/
./build/01-recursion/binary_main
./build/01-recursion/recursion_to_iteration_main
```

The tests check edge cases (`0`, `1`, `n = 0`, negative bases). They also check that the recursive and iterative versions agree over a grid of inputs.
