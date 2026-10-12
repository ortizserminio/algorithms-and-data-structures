//estos son los comentarios 
#include <iostream>
#include <cstdlib>

using namespace std;

//prototipo para que el programa sepa que hay una funcion que va a usar despues 
int Contar(float *V, int n, int x);

/*
que es lo que tenemos que hacer 
lo que hace este algorimot es encontrar un valor X dentro de un vector V de n elementos 
y devuelve el numnero de veces que X esta dentro de V 
función Contar (V:entero[n], x:entero):entero
    i,nveces:entero

    nveces <- 0
    para i<-1 hasta n hacer
        si Vi = x
            nveces <- nveces + 1
        fsi
    fpara
    devolver nveces
ffunción
*/

int main(void)
{
    // 1.1 Pedir por teclado el valor buscar x Y el tamaño n del vector 
    int x;
    int n;

    cout <<  "Intoduce valor a buscar (x):";
    cin >> x;
    cout << "Introduce n.elementos del vector (n): ";
    cin >> n;

    // 1.2 ahora hay que generar tres vectores vpeor, vmejor, vcualquiera 
    //Declaramos 
    float *Vpeor; 
    float *Vmejor;
    float *Vcualquiera;
    //reservamos memoria con el "new"
    Vpeor = new float [n+1];
    Vmejor = new float [n+1];
    Vcualquiera = new float [n+1];
    //ponemos un if por si ha habido algun error 
    if (Vpeor == NULL || Vmejor == NULL || Vcualquiera == NULL)
    {
        cout << "Error al reservar memoria" << endl;
        return -1; // exit(-1);
    }
    
    //1.3 Inicializa cada vector para que representen los casos posibles 
    //Vpeor para inicializar se hace con un for y con el valor de X porque es el Vpeor 
    for (int i = 1; i <= n; i++)
    {
        Vpeor[i] = x;
    }
    //Vmejor para que ninca se cumpla que sea x pues le sumanos 1 o lo multilpicamos por algo 
    for (int i = 1; i <= n; i++)
    {
        Vmejor[i] = x + 1;
    }
    //Vcualquiera el texto dice que la mitad = X y la otra x+1 
    for (int i = 1; i <= n; i++)
    {
        if (i <= n/2)
        {
            Vcualquiera[i] = x; 
        } else{
            Vcualquiera[i] = x + 1;
        }
    }
    
    //Imprime los vectores 
    cout << "Vector vpeor: ";
    cout << endl;

    for (int i=1 ; i<=n ; i++)
        cout << Vpeor[i] << " ";
    cout << endl;
    
    cout << "Vector vpeor: ";
    cout << endl;

    for (int i=1 ; i<=n ; i++)
        cout << Vpeor[i] << " ";
    cout << endl;
    
    cout << "Vector vcualquiera: ";
    cout << endl;

    for (int i=1 ; i<=n ; i++)
        cout << Vcualquiera[i] << " ";
    cout << endl;

    //1.5 Mostrar por pantalla los caso pero y demas 
    cout << "CASO PEOR";
    cout << endl;
    cout << "Numero de veces:";
    cout << n;
    
    cout << endl;
    cout << "CASO MEJOR";
    cout << endl;
    cout << "Numero de veces:";
    cout << Contar(Vmejor, n, x);
    
    cout << endl;
    cout << "CASO CUALQUIERA";
    cout << endl;
    cout << "Numero de veces:";
    cout << Contar(Vcualquiera, n, x);

    cout << endl;
    system("pause"); 
    return 0;
}

// 1.4 Ahora lo importanete que es hacer el contador lo hacemoos por prototipo y luego la
// la funcion porque asi queda el main arriba la opcion b)

int Contar(float *V, int n, int x){
    // Declaracion del contador y inicializacion a 0
    int nveces = 0;

    // Contador 
    for (int i = 1; i <= n; i++){
        if (V[i] == x){
            nveces++;
        }
    }
    return nveces;
}