#include <iostream>
#include <stack>
#include <cstdlib>
using namespace std;

// ============================================================
//  ACTIVIDAD 1
// ============================================================

// 1.1 - Version recursiva
double calcular1_rec(double x, int n)
{
    double r;
    if (n == 0)
        r = 1;
    else {
        if (n % 2 != 0) {           // impar(n)
            r = x * calcular1_rec(x, n - 1);
        } else {                    // par(n)
            r = calcular1_rec(x, n / 2);
            r = r * r;
        }
    }
    return r;
}

/*
 * 1.2 - Pseudocodigo iterativo (recursividad multiple -> esquema pila)
 *
 * La funcion tiene dos ramas recursivas distintas:
 *   - Rama impar: r = x * calcular1(x, n-1)        -> multiplica x por el resultado
 *   - Rama par:   r = calcular1(x, n/2); r = r*r   -> eleva al cuadrado el resultado
 *
 * Guardamos en la pila una marca que indica que operacion aplicar
 * al desapilar: 'I' (impar -> multiplicar por x) o 'P' (par -> elevar al cuadrado).
 *
 * funcion calcular1_it(x:real, n:natural U {0}):real
 *   p: pila de caracteres
 *   r: real
 *   mientras n != 0 hacer
 *     si impar(n)
 *       apilar(p, 'I')
 *       n <- n - 1
 *     si no
 *       apilar(p, 'P')
 *       n <- n / 2
 *     fsi
 *   fmientras
 *   r <- 1
 *   mientras NOT vacia(p) hacer
 *     si cima(p) = 'I'
 *       r <- r * x
 *     si no
 *       r <- r * r
 *     fsi
 *     desapilar(p)
 *   fmientras
 *   devolver r
 * ffuncion
 */

// 1.3 - Version iterativa
double calcular1_it(double x, int n)
{
    stack<char> p;
    double r;

    // Fase de bajada: registramos que operacion hacer en cada nivel
    while (n != 0) {
        if (n % 2 != 0) {   // impar
            p.push('I');
            n = n - 1;
        } else {             // par
            p.push('P');
            n = n / 2;
        }
    }

    // Caso base
    r = 1;

    // Fase de subida: aplicamos las operaciones en orden inverso
    while (!p.empty()) {
        if (p.top() == 'I')
            r = r * x;
        else            // 'P'
            r = r * r;
        p.pop();
    }

    return r;
}

// ============================================================
//  ACTIVIDAD 2
// ============================================================

// 2.1 - Version recursiva
int calcular2_rec(int x, int y)
{
    if (x <= 4)
        return x + y;
    else {
        x = x - 4;
        y = y / 3;
        return calcular2_rec(x, y) + x * y;
    }
}

/*
 * 2.2 - Pseudocodigo iterativo (recursividad lineal NO final -> esquema pila)
 *
 * Despues de la llamada recursiva hay trabajo pendiente: sumar x*y.
 * Por tanto guardamos en la pila los valores de x e y de cada nivel
 * para poder calcular x*y al desapilar.
 * Usamos una struct/pair para guardar ambos valores juntos.
 *
 * funcion calcular2_it(x:entero, y:entero):entero
 *   p: pila de pares (entero, entero)
 *   res: entero
 *   mientras x > 4 hacer
 *     x <- x - 4
 *     y <- y / 3
 *     apilar(p, (x, y))       // guardamos los valores YA modificados
 *   fmientras
 *   res <- x + y              // caso base
 *   mientras NOT vacia(p) hacer
 *     (xp, yp) <- cima(p)
 *     desapilar(p)
 *     res <- res + xp * yp
 *   fmientras
 *   devolver res
 * ffuncion
 *
 * Nota: en el recursivo, x e y se modifican ANTES de la llamada y de sumar x*y,
 * por eso guardamos los valores ya modificados.
 */

// 2.3 - Version iterativa
int calcular2_it(int x, int y)
{
    stack< pair<int,int> > p;
    int res;

    // Fase de bajada: modificamos x e y y apilamos para recordar el trabajo pendiente
    while (x > 4) {
        x = x - 4;
        y = y / 3;
        p.push( make_pair(x, y) );
    }

    // Caso base
    res = x + y;

    // Fase de subida: sumamos x*y de cada nivel
    while (!p.empty()) {
        int xp = p.top().first;
        int yp = p.top().second;
        p.pop();
        res = res + xp * yp;
    }

    return res;
}

// ============================================================
//  MAIN
// ============================================================
int main()
{
    // --- Actividad 1 ---
    cout << "=== ACTIVIDAD 1 ===" << endl;
    double x;
    int n;
    cout << "Introduce x: ";
    cin >> x;
    cout << "Introduce n: ";
    cin >> n;

    if (n < 0) {
        cout << "Error" << endl;
    } else {
        cout << "Resultado recursivo:  " << calcular1_rec(x, n) << endl;
        cout << "Resultado iterativo:  " << calcular1_it(x, n)  << endl;
    }

    cout << endl;

    // --- Actividad 2 ---
    cout << "=== ACTIVIDAD 2 ===" << endl;
    int a, b;
    cout << "Introduce x: ";
    cin >> a;
    cout << "Introduce y: ";
    cin >> b;

    cout << "Resultado recursivo:  " << calcular2_rec(a, b) << endl;
    cout << "Resultado iterativo:  " << calcular2_it(a, b)  << endl;

    cout << endl;
    // system("pause");  // descomentar en Windows
    return 0;
}