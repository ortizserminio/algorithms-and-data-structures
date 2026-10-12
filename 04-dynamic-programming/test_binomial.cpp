#include <sstream>
#include <string>
#include "check.hpp"
#include "binomial.hpp"

int main() {
    // Known values and edge cases
    CHECK_EQ(binomial_dp(0, 0), 1);
    CHECK_EQ(binomial_dp(1, 0), 1);
    CHECK_EQ(binomial_dp(1, 1), 1);
    CHECK_EQ(binomial_dp(5, 2), 10);
    CHECK_EQ(binomial_dp(10, 5), 252);
    CHECK_EQ(binomial_dp(30, 15), 155117520);
    CHECK_EQ(binomial_recursive(5, 2), 10);
    CHECK_EQ(binomial_recursive(7, 0), 1);
    CHECK_EQ(binomial_recursive(7, 7), 1);

    // Both versions agree and satisfy symmetry C(n,k) = C(n,n-k)
    for (int n = 0; n <= 18; n++) {
        for (int k = 0; k <= n; k++) {
            int dp = binomial_dp(n, k);
            CHECK_EQ(binomial_recursive(n, k), dp);
            CHECK_EQ(binomial_dp(n, n - k), dp);
        }
    }

    // The recursive version makes 2*C(n,k) - 1 calls
    for (int n = 0; n <= 16; n++) {
        for (int k = 0; k <= n; k++) {
            int calls = 0;
            int c = binomial_recursive_counted(n, k, calls);
            CHECK_EQ(calls, 2 * c - 1);
        }
    }

    // Trace format for C(2,1): root plus two indented children
    {
        std::ostringstream out;
        int counter = 1;
        binomial_trace(2, 1, counter, 0, out);
        CHECK_EQ(out.str(), std::string("1.- combinaciones_traza(2,1)\n"
                                        "    2.- combinaciones_traza(1,0)\n"
                                        "    3.- combinaciones_traza(1,1)\n"));
        CHECK_EQ(counter, 4);
    }

    return report();
}
