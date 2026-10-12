# Algorithms and Data Structures
n**English** · [Español](README.es.md)

[![CI](https://github.com/ortizserminio/algorithms-and-data-structures/actions/workflows/ci.yml/badge.svg)](https://github.com/ortizserminio/algorithms-and-data-structures/actions/workflows/ci.yml)

Algorithms and data structures I implemented during my Computer Engineering degree at Universidad Miguel Hernández (UMH, Spain), in **C++** and **Python**. Each topic folder has its own README with the problem, the approach step by step, why that algorithm was chosen over the alternatives, and a justified Big-O analysis. Every implementation is covered by tests that run in CI.

## Index

| # | Problem | Technique | Time | Space | Lang | Link |
|---|---|---|---|---|---|---|
| 01 | Decimal → binary | Recursion | O(log n) | O(log n) stack | C++ | [01-recursion](01-recursion) |
| 01 | Fast exponentiation xⁿ | Divide and conquer; recursion → iteration with an explicit stack | O(log n) | O(log n) | C++ | [01-recursion](01-recursion) |
| 02 | Count occurrences | Linear scan; best/worst/average-case analysis | Θ(n) | O(1) | C++ | [02-searching-sorting](02-searching-sorting) |
| 02 | Sorting | Insertion sort (stable, adaptive) | Θ(n) best, Θ(n²) worst | O(1) | C++ | [02-searching-sorting](02-searching-sorting) |
| 03 | Maximum subarray sum | Brute force vs single pass (Kadane) | Θ(n³) vs **Θ(n)** | O(1) | C++ | [03-algorithm-analysis](03-algorithm-analysis) |
| 04 | Combinations C(n, k) | Plain recursion vs **dynamic programming** | Θ(C(n,k)) calls vs **Θ(n·k)** | O(n) vs Θ(n·k) | C++ | [04-dynamic-programming](04-dynamic-programming) |
| 05 | Stack | Array with fixed capacity | O(1) per op | O(capacity) | Python | [05-linear-adts](05-linear-adts) |
| 05 | Queue, stack | Singly linked list with head/tail pointers; O(1) concatenation | O(1) per op | O(n) | Python | [05-linear-adts](05-linear-adts) |
| 05 | List over static memory | Contiguous array; index-linked list with free slots | O(n) insert/delete | O(capacity) | Python | [05-linear-adts](05-linear-adts) |
| 06 | Set operations | Bit vector | O(1) membership, O(size) union/∩/− | size bits | Python | [06-sets](06-sets) |
| 07 | Ordered dictionary | Binary search tree | O(h), O(n) worst | O(n) | Python | [07-trees](07-trees) |
| 07 | Ordered dictionary | **AVL tree** (self-balancing, 4 rotation cases) | **O(log n) worst** | O(n) | Python | [07-trees](07-trees) |
| 08 | All-pairs shortest paths | **Floyd-Warshall**, path reconstruction, negative-cycle detection | Θ(n³) | Θ(n²) | Python | [08-graphs](08-graphs) |
| 08 | Reachability | Warshall (transitive closure) | Θ(n³) | Θ(n²) | Python | [08-graphs](08-graphs) |
| 08 | Minimum spanning tree | **Kruskal + Union-Find** (path compression, union by rank) | O(E log E) | O(V + E) | Python | [08-graphs](08-graphs) |

## How it is tested

* **Python:** 77 `pytest` tests. Besides normal and edge cases (empty, full, single element, duplicates, negative values, invalid input), the algorithms are checked against an independent reference on random inputs: Python's `set`, `sorted`, brute-force shortest paths and brute-force MSTs. The AVL tree is checked against its invariants after every insertion and deletion.
* **C++:** 4 test programs with about 2 400 checks, using a minimal `CHECK` macro (`common/check.hpp`) so no external framework is needed. Recursive and iterative versions are compared over grids of inputs, and the O(n³) and O(n) algorithms are compared against an O(n²) reference.
* **CI** ([`.github/workflows/ci.yml`](.github/workflows/ci.yml)) runs on every push: pytest on Python 3.10 and 3.12, and the C++ tests with both g++ and clang++ using `-Werror` and AddressSanitizer/UndefinedBehaviorSanitizer.

## Run it

```bash
# Python (3.10+)
pip install -r requirements-dev.txt
python -m pytest

# C++ (any C++14 compiler + make)
make test     # build and run all C++ tests
make demos    # build the interactive demos into build/
```

Each Python module also runs as a small demo (`python 07-trees/avl.py`), and `08-graphs/floyd.py` opens the interactive route planner from the original practical.

## About this code

* The algorithms are my coursework from *Metodología de la Programación Avanzada* (C++) and *Estructuras de Datos* (Python), 2024–2026. The maximum-subarray exam and the Floyd route planner were team work.
* The unmodified originals are in the first commit, [`26c3ed7`](https://github.com/ortizserminio/algorithms-and-data-structures/commit/26c3ed7) (teammates' names removed for privacy). The history then shows each step separately: restructuring, tests and **every bug fix** with its reason (for example, a BST deletion that crashed on nodes with two children, and an AVL delete method that was never reachable because of a typo).
* The cleanup, tests, CI and documentation were prepared with the help of an AI assistant. I reviewed them, and the algorithms and their logic are my own coursework.

## License

[MIT](LICENSE)
