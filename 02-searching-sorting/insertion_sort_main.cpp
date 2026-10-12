// Interactive demo: times insertion sort on its best, average and worst
// case inputs of size n.
#include <cstdlib>
#include <ctime>
#include <iostream>
#include "insertion_sort.hpp"

static void print_range(const int* v, int from, int to) {
    for (int i = from; i <= to; i++)
        std::cout << v[i] << " ";
    std::cout << std::endl;
}

static void run_case(const char* name, int* v, int n, int from, int to) {
    std::cout << "\n" << name << "\n----------------" << std::endl;
    std::cout << "Input:  ";
    print_range(v, from, to);
    clock_t start = clock();
    insertion_sort(v, n);
    clock_t end = clock();
    double ms = (double)(end - start) / CLOCKS_PER_SEC * 1000;
    std::cout << "Sorted: ";
    print_range(v, from, to);
    std::cout << "Time (ms): " << ms << std::endl;
}

int main() {
    int seed, n, from, to;
    std::cout << "Random seed: ";
    std::cin >> seed;
    std::cout << "Vector size (n): ";
    std::cin >> n;
    std::cout << "First and last positions to print: ";
    std::cin >> from >> to;

    int* best = new int[n + 1];
    int* any = new int[n + 1];
    int* worst = new int[n + 1];

    for (int i = 1; i <= n; i++) best[i] = i;           // already sorted
    std::srand(seed);
    for (int i = 1; i <= n; i++) any[i] = std::rand();  // random
    for (int i = 1; i <= n; i++) worst[i] = n - i + 1;  // reverse sorted

    std::cout << "\nINSERTION SORT" << std::endl;
    run_case("BEST CASE", best, n, from, to);
    run_case("AVERAGE CASE", any, n, from, to);
    run_case("WORST CASE", worst, n, from, to);

    delete[] best;
    delete[] any;
    delete[] worst;
    return 0;
}
