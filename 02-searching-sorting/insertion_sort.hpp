// Insertion sort (MPA practical 2). Vectors are 1-indexed (positions 1..n,
// slot 0 unused) to match the course pseudocode; the logic is unchanged.
#pragma once

// Sorts v[1..n] in ascending order, in place.
// For each i, v[i] is moved left past every larger element of the already
// sorted prefix v[1..i-1].
//   best case  (already sorted):  Theta(n)   - the inner loop never runs
//   worst case (reverse sorted):  Theta(n^2) - i-1 shifts for each i
//   average case (random):        Theta(n^2)
// Extra space O(1). The sort is stable (only strictly greater elements move).
inline void insertion_sort(int* v, int n) {
    int i, j, x;
    for (i = 2; i <= n; i++) {
        x = v[i];
        j = i - 1;
        while (j > 0 && v[j] > x) {
            v[j + 1] = v[j];
            j = j - 1;
        }
        v[j + 1] = x;
    }
}
