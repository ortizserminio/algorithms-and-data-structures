// Interactive demo: builds the three input vectors studied in the practical
// and counts the occurrences of x in each one.
#include <iostream>
#include "count_occurrences.hpp"

static void print_vector(const float* v, int n) {
    for (int i = 1; i <= n; i++)
        std::cout << v[i] << " ";
    std::cout << std::endl;
}

int main() {
    int x;
    int n;
    std::cout << "Value to search for (x): ";
    std::cin >> x;
    std::cout << "Number of elements (n): ";
    std::cin >> n;

    float* worst = new float[n + 1];
    float* best = new float[n + 1];
    float* any = new float[n + 1];

    // Worst case for the counter: every element equals x.
    for (int i = 1; i <= n; i++)
        worst[i] = x;
    // Best case: no element equals x.
    for (int i = 1; i <= n; i++)
        best[i] = x + 1;
    // Average case: first half equals x, second half does not.
    for (int i = 1; i <= n; i++)
        any[i] = (i <= n / 2) ? x : x + 1;

    std::cout << "Worst-case vector:" << std::endl;
    print_vector(worst, n);
    std::cout << "Worst-case vector:" << std::endl;
    print_vector(worst, n);
    std::cout << "Average-case vector:" << std::endl;
    print_vector(any, n);

    std::cout << "WORST CASE - occurrences: " << n << std::endl;
    std::cout << "BEST CASE - occurrences: " << count_occurrences(best, n, x)
              << std::endl;
    std::cout << "AVERAGE CASE - occurrences: "
              << count_occurrences(any, n, x) << std::endl;

    delete[] worst;
    delete[] best;
    delete[] any;
    return 0;
}
