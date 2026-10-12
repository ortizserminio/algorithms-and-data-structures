// Interactive demo: reads a natural number and prints it in binary together
// with the recursive call trace.
#include <iostream>
#include "binary.hpp"

int main() {
    int number;
    std::cout << "Enter a natural number (0 included): ";
    std::cin >> number;

    if (number < 0) {
        std::cout << "Error: the number must be >= 0." << std::endl;
        return 1;
    }

    std::cout << "\nBinary:" << std::endl;
    binary(number, std::cout);
    std::cout << std::endl;

    std::cout << "Trace:" << std::endl;
    int calls = 1;
    binary_trace(number, calls, std::cout, std::cout);
    std::cout << std::endl;
    return 0;
}
