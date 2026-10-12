#include <iostream>
using namespace std;

// =====================================================================
//  Funcion combinaciones (version ITERATIVA con programacion dinamica)
//  Pseudocodigo (Tema 5, Ejemplo: Numero de combinaciones):
//
//  funcion combinaciones(n:natural, k:natural U {0}):natural
//      i:natural U {0}  j:natural  M:natural[n+1,k+1]
//      para i<-0 hasta n hacer
//          M[i,0] <- 1
//      fpara
//      para i<-1 hasta k hacer
//          M[i,i] <- 1
//      fpara
//      para i<-2 hasta n hacer
//          j <- 1
//          mientras j < i y j <= k hacer
//              M[i,j] <- M[i-1,j-1] + M[i-1,j]
//              j <- j + 1
//          fmientras
//      fpara
//      devolver M[n,k]
//  ffuncion
// =====================================================================
int combinaciones(int n, int k) {
    int i, j;

    // Reserva de memoria dinamica para la matriz M de [n+1][k+1].
    int **M = new int*[n + 1];
    for (i = 0; i <= n; i++) {
        M[i] = new int[k + 1];
    }

    // para i<-0 hasta n hacer: M[i,0] <- 1
    for (i = 0; i <= n; i++) {
        M[i][0] = 1;
    }

    // para i<-1 hasta k hacer: M[i,i] <- 1
    for (i = 1; i <= k; i++) {
        M[i][i] = 1;
    }

    // para i<-2 hasta n hacer
    for (i = 2; i <= n; i++) {
        j = 1;
        while (j < i && j <= k) {
            M[i][j] = M[i - 1][j - 1] + M[i - 1][j];
            j = j + 1;
        }
    }

    int resultado = M[n][k];

    // Liberar la memoria dinamica.
    for (i = 0; i <= n; i++) {
        delete[] M[i];
    }
    delete[] M;

    return resultado;
}

// =====================================================================
//  Funcion combinaciones2 (version RECURSIVA)
//  Pseudocodigo (Tema 5, Definicion recursiva):
//
//  funcion combinaciones2(n:natural, k:natural U {0}):natural
//      si k = 0 o k = n
//          devolver 1
//      si no
//          devolver combinaciones2(n-1,k-1) + combinaciones2(n-1,k)
//      fsi
//  ffuncion
//
//  numLlamadas se pasa por referencia (&) para contar el numero total
//  de llamadas que se realizan a la funcion.
// =====================================================================
int combinaciones2(int n, int k, int &numLlamadas) {
    numLlamadas = numLlamadas + 1;   // se cuenta esta llamada
    if (k == 0 || k == n) {
        return 1;
    } else {
        return combinaciones2(n - 1, k - 1, numLlamadas)
             + combinaciones2(n - 1, k, numLlamadas);
    }
}

int main() {
    int n, k;

    // Mostrar nombre y apellidos.
    cout << "Esterly Ortiz Serminio" << endl << endl;

    // Pedir por teclado los valores n y k (no se validan).
    cout << "Introduce n: ";
    cin >> n;
    cout << "Introduce k: ";
    cin >> k;

    // Llamada a la funcion combinaciones (iterativa) e impresion del resultado.
    cout << endl << "Resultado (combinaciones): " << combinaciones(n, k) << endl;

    // Llamada a la funcion combinaciones2 (recursiva) con los mismos valores.
    int numLlamadas = 0;
    int resultado2 = combinaciones2(n, k, numLlamadas);
    cout << "Resultado (combinaciones2): " << resultado2 << endl;
    cout << "Numero total de llamadas a combinaciones2: " << numLlamadas << endl;

    system("pause");
    return 0;
}
