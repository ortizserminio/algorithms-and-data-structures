// Turning recursive functions into iterative ones with an explicit stack.
// Ported from my MPA practical 4; the logic is unchanged.
#pragma once
#include <stack>
#include <utility>

// ---------------------------------------------------------------------------
// Exercise 1: fast exponentiation x^n (n >= 0).
//   n == 0  -> 1
//   n odd   -> x * x^(n-1)
//   n even  -> (x^(n/2))^2
// Every two steps n is at least halved, so time and stack depth are O(log n).
// ---------------------------------------------------------------------------
inline double fast_power_recursive(double x, int n) {
    double r;
    if (n == 0)
        r = 1;
    else {
        if (n % 2 != 0) {  // odd
            r = x * fast_power_recursive(x, n - 1);
        } else {           // even
            r = fast_power_recursive(x, n / 2);
            r = r * r;
        }
    }
    return r;
}

// The function has two different recursive branches, so on the way down we
// push a marker that says which operation to apply on the way up:
// 'I' (odd -> multiply by x) or 'P' (even -> square).
inline double fast_power_iterative(double x, int n) {
    std::stack<char> p;
    double r;

    // Going down: remember the operation for each level.
    while (n != 0) {
        if (n % 2 != 0) {
            p.push('I');
            n = n - 1;
        } else {
            p.push('P');
            n = n / 2;
        }
    }

    r = 1;  // base case

    // Going up: apply the operations in reverse order.
    while (!p.empty()) {
        if (p.top() == 'I')
            r = r * x;
        else
            r = r * r;
        p.pop();
    }
    return r;
}

// ---------------------------------------------------------------------------
// Exercise 2: linear, non-tail recursion.
//   f(x, y) = x + y                           if x <= 4
//           = f(x-4, y/3) + (x-4) * (y/3)     otherwise
// Work remains after the recursive call (adding x*y), so the iterative
// version stores the already-updated (x, y) of each level on a stack.
// Time and extra space O(x).
// ---------------------------------------------------------------------------
inline int exercise2_recursive(int x, int y) {
    if (x <= 4)
        return x + y;
    else {
        x = x - 4;
        y = y / 3;
        return exercise2_recursive(x, y) + x * y;
    }
}

inline int exercise2_iterative(int x, int y) {
    std::stack<std::pair<int, int> > p;
    int res;

    // Going down: update x and y and remember the pending work.
    while (x > 4) {
        x = x - 4;
        y = y / 3;
        p.push(std::make_pair(x, y));
    }

    res = x + y;  // base case

    // Going up: add x*y for every level.
    while (!p.empty()) {
        int xp = p.top().first;
        int yp = p.top().second;
        p.pop();
        res = res + xp * yp;
    }
    return res;
}
