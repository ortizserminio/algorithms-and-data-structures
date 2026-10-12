// Interactive demo: computes C(n, k) with dynamic programming and with plain
// recursion, prints the number of recursive calls and, for small inputs,
// the indented call trace.
#include <iostream>
#include "binomial.hpp"

int main() {
    int n, k;
    std::cout << "Total number of elements (n): ";
    std::cin >> n;
    std::cout << "Group size (k): ";
    std::cin >> k;

    if (n < 0 || k < 0 || k > n) {
        std::cout << "Error: invalid input (need 0 <= k <= n)." << std::endl;
        return 1;
    }

    std::cout << "\nDynamic programming: " << binomial_dp(n, k) << std::endl;

    int calls = 0;
    int result = binomial_recursive_counted(n, k, calls);
    std::cout << "Recursive:           " << result << std::endl;
    std::cout << "Recursive calls:     " << calls << std::endl;

    if (n <= 6) {
        std::cout << "\nCall trace:" << std::endl;
        int counter = 1;
        binomial_trace(n, k, counter, 0, std::cout);
    }
    return 0;
}
