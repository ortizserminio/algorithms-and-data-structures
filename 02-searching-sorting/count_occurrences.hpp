// Counting how many times a value appears in a vector (MPA practical 1).
// Vectors are 1-indexed (positions 1..n, slot 0 unused) to match the
// course pseudocode.
#pragma once

// Returns the number of positions i in 1..n with v[i] == x.
// Every element is inspected exactly once, so best, worst and average case
// are all Theta(n) time, O(1) extra space.
inline int count_occurrences(const float* v, int n, int x) {
    int times = 0;
    for (int i = 1; i <= n; i++) {
        if (v[i] == x) {
            times++;
        }
    }
    return times;
}
