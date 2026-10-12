#include <iostream>
#include <cstdlib>
#include <ctime>

using namespace std;

void Insercion(int *V, int n);
void imprimirVector(int *V, int desde, int hasta);

/*g++ Practica2.cpp -o Practica2.exe Practica2.exe*/
void Insercion(int *V, int n)
{
    int i, j, x;
    for (i = 2; i <= n; i++) {
        x = V[i];
        j = i - 1;
        while (j > 0 && V[j] > x) {
            V[j + 1] = V[j];
            j = j - 1;
        }
        V[j + 1] = x;
    }
}

void imprimirVector(int *V, int desde, int hasta)
{
    for (int i = desde; i <= hasta; i++)
        cout << V[i] << " ";
    cout << endl;
}

int main()
{
    int semilla, tam, ini, fin;
    clock_t tinicio, tfin;
    double tiempo;

    cout << "Semilla inicial para generar numeros aleatorios: ";
    cin >> semilla;

    cout << "Introduce tamano del vector (n): ";
    cin >> tam;

    cout << "Posiciones inicial y final del vector para mostrar" << endl;
    cout << "Inicial: ";
    cin >> ini;
    cout << "Final: ";
    cin >> fin;

    // Reservar memoria para los tres vectores (indices 1..tam)
    int *Vmejor      = new int[tam + 1];
    int *Vcualquiera = new int[tam + 1];
    int *Vpeor       = new int[tam + 1];

    // Caso mejor: vector ya ordenado ascendentemente (1, 2, ..., n)
    for (int i = 1; i <= tam; i++)
        Vmejor[i] = i;

    // Caso cualquiera: vector con numeros aleatorios
    srand(semilla);
    for (int i = 1; i <= tam; i++)
        Vcualquiera[i] = rand();

    // Caso peor: vector ordenado descendentemente (n, n-1, ..., 1)
    for (int i = 1; i <= tam; i++)
        Vpeor[i] = tam - i + 1;

    cout << endl;
    cout << "ALGORITMO DE INSERCION" << endl;

    // --- CASO MEJOR ---
    cout << endl;
    cout << "CASO MEJOR" << endl;
    cout << "----------------" << endl;
    cout << "Vector a ordenar: ";
    imprimirVector(Vmejor, ini, fin);
    tinicio = clock();
    Insercion(Vmejor, tam);
    tfin = clock();
    tiempo = (double)(tfin - tinicio) / CLOCKS_PER_SEC * 1000;
    cout << "Vector ordenado: ";
    imprimirVector(Vmejor, ini, fin);
    cout << "Tiempo de ejecucion (ms): " << tiempo << endl;

    // --- CASO CUALQUIERA ---
    cout << endl;
    cout << "CASO CUALQUIERA" << endl;
    cout << "----------------" << endl;
    cout << "Vector a ordenar: ";
    imprimirVector(Vcualquiera, ini, fin);
    tinicio = clock();
    Insercion(Vcualquiera, tam);
    tfin = clock();
    tiempo = (double)(tfin - tinicio) / CLOCKS_PER_SEC * 1000;
    cout << "Vector ordenado: ";
    imprimirVector(Vcualquiera, ini, fin);
    cout << "Tiempo de ejecucion (ms): " << tiempo << endl;

    // --- CASO PEOR ---
    cout << endl;
    cout << "CASO PEOR" << endl;
    cout << "----------------" << endl;
    cout << "Vector a ordenar: ";
    imprimirVector(Vpeor, ini, fin);
    tinicio = clock();
    Insercion(Vpeor, tam);
    tfin = clock();
    tiempo = (double)(tfin - tinicio) / CLOCKS_PER_SEC * 1000;
    cout << "Vector ordenado: ";
    imprimirVector(Vpeor, ini, fin);
    cout << "Tiempo de ejecucion (ms): " << tiempo << endl;

    delete[] Vmejor;
    delete[] Vcualquiera;
    delete[] Vpeor;

    cout << endl;
    system("pause");
    return 0;
}
