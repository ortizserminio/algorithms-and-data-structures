// Interactive demo comparing the recursive and iterative versions.
#include <iostream>
#include "recursion_to_iteration.hpp"

int main() {
    std::cout << "=== EXERCISE 1: fast power ===" << std::endl;
    double x;
    int n;
    std::cout << "Enter x: ";
    std::cin >> x;
    std::cout << "Enter n: ";
    std::cin >> n;

    if (n < 0) {
        std::cout << "Error" << std::endl;
    } else {
        std::cout << "Recursive: " << fast_power_recursive(x, n) << std::endl;
        std::cout << "Iterative: " << fast_power_iterative(x, n) << std::endl;
    }

    std::cout << "\n=== EXERCISE 2 ===" << std::endl;
    int a, b;
    std::cout << "Enter x: ";
    std::cin >> a;
    std::cout << "Enter y: ";
    std::cin >> b;
    std::cout << "Recursive: " << exercise2_recursive(a, b) << std::endl;
    std::cout << "Iterative: " << exercise2_iterative(a, b) << std::endl;
    return 0;
}
