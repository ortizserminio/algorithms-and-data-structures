#include <iostream>
#include <cstdlib>
#include <ctime>
using namespace std;

// Algoritmo 1
int g1grupal2526_1(int *V, int n, int &imejor, int &jmejor)
{
    int esta_suma, suma_max, i, j, k;

    suma_max = 0;
    imejor = 0;
    jmejor = 0;

    for (i = 1; i <= n; i++) {
        for (j = i; j <= n; j++) {
            esta_suma = 0;
            for (k = i; k <= j; k++) {
                esta_suma = esta_suma + V[k];
            }
            if (esta_suma > suma_max) {
                suma_max = esta_suma;
                imejor = i;
                jmejor = j;
            }
        }
    }
    return suma_max;
}

// Algoritmo 2
int g1grupal2526_2(int *V, int n, int &imejor, int &jmejor)
{
    int esta_suma, suma_max, i, j;

    i = 1;
    esta_suma = 0;
    suma_max = 0;
    imejor = 0;
    jmejor = 0;

    for (j = 1; j <= n; j++) {
        esta_suma = esta_suma + V[j];
        if (esta_suma > suma_max) {
            suma_max = esta_suma;
            imejor = i;
            jmejor = j;
        } else {
            if (esta_suma < 0) {
                i = j + 1;
                esta_suma = 0;
            }
        }
    }
    return suma_max;
}

int main()
{
    int n, semilla, n1, n2, p1, p2;
    int imejor1, jmejor1, imejor2, jmejor2;
    int suma1, suma2;
    clock_t tinicio, tfin;
    double tiempo;

    // Nombres del grupo
    cout << "Esterly Ortiz Serminio" << endl;

    // Pedir datos
    cout << "Semilla inicial para generar numero aleatorios: ";
    cin >> semilla;

    cout << "Dime el tamanio del vector (n): ";
    cin >> n;

    cout << "Dime un valor aleatorio(n1): ";
    cin >> n1;

    cout << "Dime un valor aleatorio(n2): ";
    cin >> n2;

    if (n1 >= n2) {
        cout << "ERROR, n1 debe ser menor que n2" << endl;
        return -1;
    }

    cout << "Introduce la posicion inicial para imprimir el vector: ";
    cin >> p1;
    cout << "Introduce la posicion final para imprimir el vector: ";
    cin >> p2;

    // Crear e inicializar vector
    int *V = new int[n + 1];
    srand(semilla);
    for (int i = 1; i <= n; i++)
        V[i] = n1 + rand() % (n2 - n1 + 1);

    // Imprimir vector entre p1 y p2
    cout << "Vector: ";
    for (int i = p1; i <= p2; i++)
        cout << V[i] << " ";
    cout << endl;

    // --- ALGORITMO 1 ---
    tinicio = clock();
    suma1 = g1grupal2526_1(V, n, imejor1, jmejor1);
    tfin = clock();
    tiempo = (double)(tfin - tinicio) / CLOCKS_PER_SEC * 1000;
    cout << "La suma es: " << suma1 << endl;
    cout << "Las posiciones inicial y final son: " << imejor1 << " y " << jmejor1 << endl;
    cout << "Tiempo: " << tiempo << "ms" << endl;

    // --- ALGORITMO 2 ---
    tinicio = clock();
    suma2 = g1grupal2526_2(V, n, imejor2, jmejor2);
    tfin = clock();
    tiempo = (tfin - tinicio) / CLOCKS_PER_SEC * 1000;
    cout << "La suma es: " << suma2 << endl;
    cout << "Las posiciones inicial y final son: " << imejor2 << " y " << jmejor2 << endl;
    cout << "Tiempo: " << tiempo << "ms" << endl;

    delete[] V;

    system("pause");
    return 0;
}