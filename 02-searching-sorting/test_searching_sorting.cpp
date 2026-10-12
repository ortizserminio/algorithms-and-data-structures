#include <algorithm>
#include <cstdlib>
#include <vector>
#include "check.hpp"
#include "count_occurrences.hpp"
#include "insertion_sort.hpp"

// Helper: builds a 1-indexed vector (slot 0 is a dummy) from values.
static std::vector<int> one_indexed(const std::vector<int>& values) {
    std::vector<int> v(1, 0);
    v.insert(v.end(), values.begin(), values.end());
    return v;
}

static bool sorts_correctly(std::vector<int> values) {
    std::vector<int> v = one_indexed(values);
    insertion_sort(v.data(), (int)values.size());
    std::sort(values.begin(), values.end());
    return std::equal(values.begin(), values.end(), v.begin() + 1);
}

int main() {
    // count_occurrences
    {
        float empty[1] = {0};
        CHECK_EQ(count_occurrences(empty, 0, 7), 0);           // n = 0

        float all[] = {0, 7, 7, 7, 7};
        CHECK_EQ(count_occurrences(all, 4, 7), 4);             // worst case

        float none[] = {0, 8, 8, 8};
        CHECK_EQ(count_occurrences(none, 3, 7), 0);            // best case

        float half[] = {0, 7, 7, 8, 8};
        CHECK_EQ(count_occurrences(half, 4, 7), 2);            // average case

        float slot0[] = {7, 1, 2};
        CHECK_EQ(count_occurrences(slot0, 2, 7), 0);           // slot 0 ignored

        float negatives[] = {0, -3, 5, -3};
        CHECK_EQ(count_occurrences(negatives, 3, -3), 2);
    }

    // insertion_sort: edge cases
    CHECK(sorts_correctly(std::vector<int>()));                // empty
    CHECK(sorts_correctly(std::vector<int>(1, 42)));           // one element
    CHECK(sorts_correctly({1, 2, 3, 4, 5}));                   // best case
    CHECK(sorts_correctly({5, 4, 3, 2, 1}));                   // worst case
    CHECK(sorts_correctly({3, 1, 3, 2, 1, 3}));                // duplicates
    CHECK(sorts_correctly({0, -5, 12, -5, 7}));                // negatives

    // insertion_sort: slot 0 must never be touched
    {
        std::vector<int> v = {999, 3, 2, 1};
        insertion_sort(v.data(), 3);
        CHECK_EQ(v[0], 999);
    }

    // insertion_sort: random inputs
    std::srand(12345);
    for (int trial = 0; trial < 200; trial++) {
        std::vector<int> values(std::rand() % 50);
        for (size_t i = 0; i < values.size(); i++)
            values[i] = std::rand() % 100 - 50;
        CHECK(sorts_correctly(values));
    }

    return report();
}
