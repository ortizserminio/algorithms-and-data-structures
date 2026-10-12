// Number of combinations C(n, k): plain recursion vs. dynamic programming.
// Ported from my MPA practical 3.2 and MPA exam; the logic is unchanged
// (only the C(n, k) table is now freed with RAII instead of new/delete).
#pragma once
#include <ostream>
#include <vector>

// Pascal's rule, top-down:
//   C(n, k) = 1                              if k == 0 or k == n
//           = C(n-1, k-1) + C(n-1, k)        otherwise
// The same subproblems are recomputed many times: the call tree has
// 2*C(n, k) - 1 nodes, which is exponential in n (e.g. Theta(2^n / sqrt(n))
// for k = n/2). Stack depth O(n).
inline int binomial_recursive(int n, int k) {
    if (k == 0 || k == n) {
        return 1;
    } else {
        return binomial_recursive(n - 1, k - 1) + binomial_recursive(n - 1, k);
    }
}

// Same recursion, counting the calls made (calls is incremented once per
// call, so it ends at 2*C(n, k) - 1).
inline int binomial_recursive_counted(int n, int k, int& calls) {
    calls = calls + 1;
    if (k == 0 || k == n) {
        return 1;
    } else {
        return binomial_recursive_counted(n - 1, k - 1, calls) +
               binomial_recursive_counted(n - 1, k, calls);
    }
}

// Same recursion, writing an indented call trace (4 spaces per level).
inline void binomial_trace(int n, int k, int& counter, int level,
                           std::ostream& out) {
    for (int i = 0; i < level; i++) {
        out << "    ";
    }
    out << counter << ".- combinaciones_traza(" << n << "," << k << ")"
        << '\n';
    counter++;

    if (k == 0 || k == n) {
        // base case: nothing else to expand
    } else {
        binomial_trace(n - 1, k - 1, counter, level + 1, out);
        binomial_trace(n - 1, k, counter, level + 1, out);
    }
}

// Bottom-up dynamic programming over the table M[0..n][0..k]:
//   M[i][0] = 1, M[i][i] = 1, M[i][j] = M[i-1][j-1] + M[i-1][j]
// Each cell is computed once from two cells of the previous row:
// Theta(n*k) time and Theta(n*k) space. Requires 0 <= k <= n.
inline int binomial_dp(int n, int k) {
    int i, j;
    std::vector<std::vector<int> > M(n + 1, std::vector<int>(k + 1, 0));

    for (i = 0; i <= n; i++) {
        M[i][0] = 1;
    }
    for (i = 1; i <= k; i++) {
        M[i][i] = 1;
    }
    for (i = 2; i <= n; i++) {
        j = 1;
        while (j < i && j <= k) {
            M[i][j] = M[i - 1][j - 1] + M[i - 1][j];
            j = j + 1;
        }
    }
    return M[n][k];
}
