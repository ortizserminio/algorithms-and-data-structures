// Decimal -> binary conversion by recursion, plus a version that prints a
// call trace. Ported from my MPA practical 3.1; the logic is unchanged, but
// output goes to a std::ostream so it can be tested.
#pragma once
#include <ostream>

// Writes the binary representation of n (n >= 0) to out.
//   binary(n) = n                          if n < 2
//             = binary(n div 2), n mod 2   otherwise
// The recursive call comes first, so digits are written most significant
// first. Time O(log n), stack depth O(log n).
inline void binary(int n, std::ostream& out) {
    if (n < 2) {
        out << n;
    } else {
        binary(n / 2, out);
        out << n % 2;
    }
}

// Same algorithm, but before each call it writes a numbered trace line
// "k.- binario_traza(n)" to trace. Digits are written to digits.
inline void binary_trace(int n, int& counter, std::ostream& trace,
                         std::ostream& digits) {
    trace << counter << ".- binario_traza(" << n << ")" << '\n';
    counter++;

    if (n < 2) {
        digits << n;                                  // base case
    } else {
        binary_trace(n / 2, counter, trace, digits);  // recursive call
        digits << n % 2;                              // work after the call
    }
}
