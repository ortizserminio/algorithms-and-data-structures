// Maximum subarray sum: two solutions of very different cost (MPA exam,
// solved in a team). Vectors are 1-indexed (positions 1..n, slot 0 unused)
// to match the course pseudocode; the logic is unchanged.
//
// Convention used by both functions: the empty subarray is allowed, so the
// result is never negative. If every element is negative they return 0 and
// best_i = best_j = 0.
#pragma once

// Brute force: tries every pair (i, j) and sums v[i..j] from scratch.
// Three nested loops -> Theta(n^3) time, O(1) extra space.
inline int max_subarray_cubic(const int* v, int n, int& best_i, int& best_j) {
    int this_sum, max_sum, i, j, k;

    max_sum = 0;
    best_i = 0;
    best_j = 0;

    for (i = 1; i <= n; i++) {
        for (j = i; j <= n; j++) {
            this_sum = 0;
            for (k = i; k <= j; k++) {
                this_sum = this_sum + v[k];
            }
            if (this_sum > max_sum) {
                max_sum = this_sum;
                best_i = i;
                best_j = j;
            }
        }
    }
    return max_sum;
}

// Single pass (Kadane's idea): keep the sum of the current candidate
// subarray starting at i; when it drops below 0 it can never help a later
// subarray, so restart at j + 1.
// One loop -> Theta(n) time, O(1) extra space.
inline int max_subarray_linear(const int* v, int n, int& best_i, int& best_j) {
    int this_sum, max_sum, i, j;

    i = 1;
    this_sum = 0;
    max_sum = 0;
    best_i = 0;
    best_j = 0;

    for (j = 1; j <= n; j++) {
        this_sum = this_sum + v[j];
        if (this_sum > max_sum) {
            max_sum = this_sum;
            best_i = i;
            best_j = j;
        } else {
            if (this_sum < 0) {
                i = j + 1;
                this_sum = 0;
            }
        }
    }
    return max_sum;
}
