// Minimal assertion helpers for the C++ tests (no external framework needed).
#pragma once
#include <iostream>

static int g_failures = 0;
static int g_checks = 0;

#define CHECK(cond)                                                        \
    do {                                                                   \
        ++g_checks;                                                        \
        if (!(cond)) {                                                     \
            ++g_failures;                                                  \
            std::cerr << __FILE__ << ":" << __LINE__ << ": CHECK failed: " \
                      << #cond << std::endl;                               \
        }                                                                  \
    } while (0)

#define CHECK_EQ(a, b) CHECK((a) == (b))

inline int report() {
    std::cout << (g_checks - g_failures) << "/" << g_checks << " checks passed"
              << std::endl;
    return g_failures == 0 ? 0 : 1;
}
