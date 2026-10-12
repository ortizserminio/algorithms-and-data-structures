#include <cstdlib>
#include <vector>
#include "check.hpp"
#include "max_subarray.hpp"

// Independent reference: best sum over all (possibly empty) subarrays using
// prefix sums, O(n^2).
static int reference(const std::vector<int>& v) {  // v is 1-indexed
    int n = (int)v.size() - 1;
    int best = 0;
    for (int i = 1; i <= n; i++) {
        int s = 0;
        for (int j = i; j <= n; j++) {
            s += v[j];
            if (s > best) best = s;
        }
    }
    return best;
}

static int range_sum(const std::vector<int>& v, int i, int j) {
    int s = 0;
    for (int k = i; k <= j; k++) s += v[k];
    return s;
}

int main() {
    int i, j;

    // Classic example: -2 1 -3 4 -1 2 1 -5 4 -> 6 at positions 4..7
    {
        std::vector<int> v = {0, -2, 1, -3, 4, -1, 2, 1, -5, 4};
        int n = 9;
        CHECK_EQ(max_subarray_cubic(v.data(), n, i, j), 6);
        CHECK_EQ(i, 4);
        CHECK_EQ(j, 7);
        CHECK_EQ(max_subarray_linear(v.data(), n, i, j), 6);
        CHECK_EQ(i, 4);
        CHECK_EQ(j, 7);
    }

    // Edge case: empty vector
    {
        std::vector<int> v = {0};
        CHECK_EQ(max_subarray_cubic(v.data(), 0, i, j), 0);
        CHECK_EQ(max_subarray_linear(v.data(), 0, i, j), 0);
    }

    // Edge case: all negative -> empty subarray, sum 0, positions 0..0
    {
        std::vector<int> v = {0, -3, -1, -7};
        CHECK_EQ(max_subarray_cubic(v.data(), 3, i, j), 0);
        CHECK(i == 0 && j == 0);
        CHECK_EQ(max_subarray_linear(v.data(), 3, i, j), 0);
        CHECK(i == 0 && j == 0);
    }

    // Edge case: all positive -> the whole vector
    {
        std::vector<int> v = {0, 2, 3, 1};
        CHECK_EQ(max_subarray_linear(v.data(), 3, i, j), 6);
        CHECK(i == 1 && j == 3);
    }

    // Single element
    {
        std::vector<int> v = {0, 5};
        CHECK_EQ(max_subarray_cubic(v.data(), 1, i, j), 5);
        CHECK_EQ(max_subarray_linear(v.data(), 1, i, j), 5);
    }

    // Random vectors: both match the reference, and the reported positions
    // really add up to the reported sum.
    std::srand(2026);
    for (int trial = 0; trial < 300; trial++) {
        int n = std::rand() % 40;
        std::vector<int> v(n + 1, 0);
        for (int k = 1; k <= n; k++) v[k] = std::rand() % 21 - 10;
        int expected = reference(v);

        int s1 = max_subarray_cubic(v.data(), n, i, j);
        CHECK_EQ(s1, expected);
        if (s1 > 0) CHECK_EQ(range_sum(v, i, j), s1);

        int s2 = max_subarray_linear(v.data(), n, i, j);
        CHECK_EQ(s2, expected);
        if (s2 > 0) CHECK_EQ(range_sum(v, i, j), s2);
    }

    return report();
}
