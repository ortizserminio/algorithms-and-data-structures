// 1.1 y 1.2 Implementación del algoritmo recursivo para pasar a binario
#include <iostream>
#include <cstdlib>

using namespace std;

// Prototipo para que el programa sepa que hay una funcion que va a usar despues
void binario(int n);

/*
Pseudocodigo del algoritmo:
procedimiento binario (n:natural)
   si n < 2
      imprimir n
   si no
      binario(n div 2)
      imprimir n mod 2
   fsi
fprocedimiento
*/

// Implementacion de la funcion que hemos declarado arriba
void binario(int n) {
    if (n < 2) {
        cout << n;
    } else {
        binario(n / 2);
        cout << n % 2;
    }
}

void binario_traza(int n, int &contador) {
    // 1º PARTE: ANTES de la recursividad (La Traza)
    cout << contador << ".- binario_traza(" << n << ")" << endl;
    contador++; 

    if (n < 2) {
        // CASO BASE
        cout << n;
    } else {
        // 2º PARTE: LA LLAMADA RECURSIVA
        binario_traza(n / 2, contador);
        
        // 3º PARTE: DESPUÉS de la recursividad (El Resultado)
        cout << n % 2;
    }
}

int main() 
{
    int numero;

    // Pedimos el numero al usuario tal como indica el enunciado
    cout << "Introduce numero natural (incluido el 0): ";
    cin >> numero;

    // Comprobamos si es menor que 0 para mostrar el error
    if (numero < 0) {
        cout << "Error: El numero introducido no es valido. Debe ser mayor o igual a 0." << endl;
    } else {
        cout << "\nEl numero en binario es:" << endl;
        binario(numero);
        cout << endl; 

        cout << "La traza es:" << endl;
        // Inicializamos el contador en 1 para la traza y lo pasamos por referencia
        int contador_llamadas = 1; 
        binario_traza(numero, contador_llamadas);
        cout << endl;
    }

    cout << endl;
    system("pause"); 
    return 0;
}

