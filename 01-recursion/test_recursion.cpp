#include <cmath>
#include <sstream>
#include <string>
#include "check.hpp"
#include "binary.hpp"
#include "recursion_to_iteration.hpp"

static std::string to_binary(int n) {
    std::ostringstream out;
    binary(n, out);
    return out.str();
}

int main() {
    // binary: edge cases 0 and 1, powers of two, general values
    CHECK_EQ(to_binary(0), "0");
    CHECK_EQ(to_binary(1), "1");
    CHECK_EQ(to_binary(2), "10");
    CHECK_EQ(to_binary(5), "101");
    CHECK_EQ(to_binary(255), "11111111");
    CHECK_EQ(to_binary(1024), "10000000000");

    // binary_trace: same digits, one numbered trace line per call
    {
        std::ostringstream trace, digits;
        int calls = 1;
        binary_trace(10, calls, trace, digits);
        CHECK_EQ(digits.str(), "1010");
        CHECK_EQ(calls, 5);  // 4 calls (10, 5, 2, 1); counter starts at 1
        CHECK_EQ(trace.str(),
                 std::string("1.- binario_traza(10)\n2.- binario_traza(5)\n"
                             "3.- binario_traza(2)\n4.- binario_traza(1)\n"));
    }

    // fast power: recursive and iterative agree with std::pow
    CHECK_EQ(fast_power_recursive(2, 0), 1.0);
    CHECK_EQ(fast_power_iterative(2, 0), 1.0);
    CHECK_EQ(fast_power_recursive(0, 5), 0.0);
    CHECK_EQ(fast_power_iterative(-2, 3), -8.0);
    // Reference value by repeated multiplication (exact for powers of 3 that
    // fit in a double); std::pow is not exact on every libm.
    double expected = 1;
    for (int n = 0; n <= 20; n++) {
        CHECK_EQ(fast_power_recursive(3, n), expected);
        CHECK_EQ(fast_power_iterative(3, n), expected);
        expected *= 3;
    }
    CHECK(std::fabs(fast_power_iterative(1.5, 7) - 17.0859375) < 1e-9);

    // exercise 2: base case, one level, and agreement over a grid of inputs
    CHECK_EQ(exercise2_recursive(4, 10), 14);
    CHECK_EQ(exercise2_recursive(8, 9), 4 + 3 + 4 * 3);
    for (int x = -3; x <= 40; x++)
        for (int y = 0; y <= 60; y += 7)
            CHECK_EQ(exercise2_recursive(x, y), exercise2_iterative(x, y));

    return report();
}
