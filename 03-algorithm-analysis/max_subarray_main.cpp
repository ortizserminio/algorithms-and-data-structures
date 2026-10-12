// Interactive demo: fills a vector with random values in [n1, n2] and times
// both maximum-subarray algorithms on it.
#include <cstdlib>
#include <ctime>
#include <iostream>
#include "max_subarray.hpp"

int main() {
    int n, seed, n1, n2, p1, p2;
    int i1, j1, i2, j2;
    int sum1, sum2;
    clock_t start, end;
    double ms;

    std::cout << "Random seed: ";
    std::cin >> seed;
    std::cout << "Vector size (n): ";
    std::cin >> n;
    std::cout << "Minimum random value (n1): ";
    std::cin >> n1;
    std::cout << "Maximum random value (n2): ";
    std::cin >> n2;

    if (n1 >= n2) {
        std::cout << "ERROR, n1 must be smaller than n2" << std::endl;
        return 1;
    }

    std::cout << "First position to print: ";
    std::cin >> p1;
    std::cout << "Last position to print: ";
    std::cin >> p2;

    int* v = new int[n + 1];
    std::srand(seed);
    for (int i = 1; i <= n; i++)
        v[i] = n1 + std::rand() % (n2 - n1 + 1);

    std::cout << "Vector: ";
    for (int i = p1; i <= p2; i++)
        std::cout << v[i] << " ";
    std::cout << std::endl;

    // --- Algorithm 1: O(n^3) ---
    start = clock();
    sum1 = max_subarray_cubic(v, n, i1, j1);
    end = clock();
    ms = (double)(end - start) / CLOCKS_PER_SEC * 1000;
    std::cout << "O(n^3) sum: " << sum1 << "  positions: " << i1 << " .. "
              << j1 << "  time: " << ms << " ms" << std::endl;

    // --- Algorithm 2: O(n) ---
    start = clock();
    sum2 = max_subarray_linear(v, n, i2, j2);
    end = clock();
    ms = (double)(end - start) / CLOCKS_PER_SEC * 1000;
    std::cout << "O(n)   sum: " << sum2 << "  positions: " << i2 << " .. "
              << j2 << "  time: " << ms << " ms" << std::endl;

    delete[] v;
    return 0;
}
