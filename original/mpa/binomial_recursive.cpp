#include <iostream>
#include <cstdlib>

using namespace std;

// 1. Funcion original (Actividad 2.2)
int combinaciones(int n, int k) {
    if (k == 0 || k == n) {
        return 1;
    } else {
        return combinaciones(n - 1, k - 1) + combinaciones(n - 1, k);
    }
}

// 2. Funcion con traza e indentacion (Actividad 2.3)
void combinaciones_traza(int n, int k, int &contador, int nivel) {
    // Primero, imprimimos los espacios en blanco segun el nivel de profundidad
    for (int i = 0; i < nivel; i++) {
        cout << "    "; // 4 espacios por nivel
    }

    // Luego imprimimos la linea de la traza
    cout << contador << ".- combinaciones_traza(" << n << "," << k << ")" << endl;
    contador++; // Aumentamos para la siguiente llamada

    // Hacemos la logica recursiva pero sin devolver valores (solo para imprimir traza)
    if (k == 0 || k == n) {
        // Caso base: no hacemos nada mas, la recursividad se detiene aqui
    } else {
        // Caso general: llamamos a las dos ramas sumandole 1 al nivel para que se indenten mas
        combinaciones_traza(n - 1, k - 1, contador, nivel + 1);
        combinaciones_traza(n - 1, k, contador, nivel + 1);
    }
}

// 3. El main que llama a todo
int main() 
{
    int n, k;

    cout << "Introduce total de personas (elementos) (n): ";
    cin >> n;
    cout << "Introduce tamano del grupo de personas(k): ";
    cin >> k;

    if (n < 0 || k < 0 || k > n) {
        cout << "Error: Datos no validos." << endl;
    } else {
        // Resultado normal
        cout << "\nEl numero de grupos es: " << combinaciones(n, k) << endl;

        // La traza (Actividad 2.3)
        cout << "\nLa traza es:" << endl;
        int contador_llamadas = 1;
        // Llamamos a la traza empezando en el nivel 0 de indentacion
        combinaciones_traza(n, k, contador_llamadas, 0);
        
        // Volvemos a imprimir el resultado al final como pide la captura de la practica
        cout << "\nEl numero de grupos es: " << combinaciones(n, k) << endl;
    }

    cout << endl;
    system("pause"); 
    return 0;
} 