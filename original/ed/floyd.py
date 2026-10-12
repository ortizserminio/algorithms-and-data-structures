# -*- coding: utf-8 -*-
"""
PRÁCTICA 3 - GRAFOS
Algoritmo de Floyd
Caso: optimización de rutas de reparto entre ubicaciones

Notas importantes para la defensa:
- Floyd calcula caminos mínimos entre todos los pares de nodos.
- Soporta pesos negativos, siempre que no existan ciclos negativos.
- Si hay empate entre dos rutas del mismo coste, este código conserva la ruta encontrada primero.
- Warshall es una variante booleana relacionada: indica si existe camino o no entre pares de nodos.
"""

from abc import ABC, abstractmethod

INF = 999999


# ============================================================
# INTERFAZ DEL GRAFO
# ============================================================

class GrafoInterfaz(ABC):
    """Interfaz básica para trabajar con un grafo representado por matriz."""

    @abstractmethod
    def obtener_nodos(self):
        pass

    @abstractmethod
    def obtener_matriz(self):
        pass

    @abstractmethod
    def modificar_conexion(self, origen, destino, coste, bidireccional=False):
        pass

    @abstractmethod
    def borrar_conexion(self, origen, destino, bidireccional=False):
        pass


# ============================================================
# IMPLEMENTACIÓN DEL GRAFO CON MATRIZ DE COSTES
# ============================================================

class GrafoMatrizCostes(GrafoInterfaz):
    def __init__(self, nodos, matriz):
        self.nodos = list(nodos)
        self.matriz = self._copiar_matriz(matriz)
        self._validar_grafo()

    def _copiar_matriz(self, matriz):
        copia = []
        for i in range(len(matriz)):
            fila = []
            for j in range(len(matriz[i])):
                fila.append(matriz[i][j])
            copia.append(fila)
        return copia

    def _validar_grafo(self):
        if len(self.nodos) == 0:
            raise ValueError("El grafo no puede estar vacío.")

        if len(self.matriz) == 0:
            raise ValueError("La matriz de costes no puede estar vacía.")

        if len(self.matriz) != len(self.nodos):
            raise ValueError("El número de filas de la matriz debe coincidir con el número de nodos.")

        for fila in self.matriz:
            if len(fila) != len(self.nodos):
                raise ValueError("La matriz debe ser cuadrada.")

        for i in range(len(self.nodos)):
            if self.matriz[i][i] != 0:
                raise ValueError("La diagonal de la matriz debe tener coste 0.")

    def obtener_nodos(self):
        return list(self.nodos)

    def obtener_matriz(self):
        return self._copiar_matriz(self.matriz)

    def _indice_nodo(self, nodo):
        nodo = nodo.upper()
        if nodo not in self.nodos:
            raise ValueError("El nodo introducido no existe.")
        return self.nodos.index(nodo)

    def modificar_conexion(self, origen, destino, coste, bidireccional=False):
        idx_origen = self._indice_nodo(origen)
        idx_destino = self._indice_nodo(destino)

        if idx_origen == idx_destino and coste != 0:
            raise ValueError("El coste de un nodo hacia sí mismo debe ser 0.")

        self.matriz[idx_origen][idx_destino] = coste

        if bidireccional:
            self.matriz[idx_destino][idx_origen] = coste

    def borrar_conexion(self, origen, destino, bidireccional=False):
        idx_origen = self._indice_nodo(origen)
        idx_destino = self._indice_nodo(destino)

        if idx_origen == idx_destino:
            self.matriz[idx_origen][idx_destino] = 0
        else:
            self.matriz[idx_origen][idx_destino] = INF
            if bidireccional:
                self.matriz[idx_destino][idx_origen] = INF


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def mostrar_matriz(matriz, nodos):
    print("      ", end="")
    for nodo in nodos:
        print(f"{nodo:>8}", end="")
    print()

    for i in range(len(matriz)):
        print(f"{nodos[i]:>6}", end="")
        for j in range(len(matriz[i])):
            if matriz[i][j] == INF:
                print(f"{'INF':>8}", end="")
            else:
                print(f"{matriz[i][j]:>8}", end="")
        print()
    print()


def reconstruir_camino(origen, destino, siguiente, nodos):
    if siguiente[origen][destino] is None:
        return None

    camino = [origen]

    while origen != destino:
        origen = siguiente[origen][destino]
        camino.append(origen)

    camino_nombres = []
    for indice in camino:
        camino_nombres.append(nodos[indice])

    return camino_nombres


def detectar_ciclos_negativos(distancias, nodos):
    """
    Después de Floyd, si D[i][i] < 0, existe un ciclo negativo alcanzable desde ese nodo.
    En ese caso no existe camino mínimo real, porque se podría repetir el ciclo y bajar el coste indefinidamente.
    """
    ciclos = []
    for i in range(len(distancias)):
        if distancias[i][i] < 0:
            ciclos.append(nodos[i])
    return ciclos


# ============================================================
# ALGORITMO DE FLOYD
# ============================================================

def floyd(grafo, mostrar_pasos=True, mostrar_matriz_en_cada_paso=False):
    nodos = grafo.obtener_nodos()
    distancias = grafo.obtener_matriz()
    n = len(nodos)

    # Matriz para reconstruir caminos.
    # siguiente[i][j] indica cuál es el siguiente nodo al salir desde i para llegar a j.
    siguiente = []
    for i in range(n):
        fila = []
        for j in range(n):
            if distancias[i][j] != INF and i != j:
                fila.append(j)
            else:
                fila.append(None)
        siguiente.append(fila)

    if mostrar_pasos:
        print("\nMATRIZ INICIAL DE COSTES:")
        mostrar_matriz(distancias, nodos)
        print("Nota: si dos caminos tienen el mismo coste, se conserva el primero encontrado.")
        print("Esto ocurre porque el código actualiza solo cuando el nuevo coste es estrictamente menor.\n")

    # Algoritmo de Floyd.
    # k = nodo intermedio, i = origen, j = destino.
    for k in range(n):
        if mostrar_pasos:
            print(f"--- Paso usando como intermediario el nodo {nodos[k]} ---")

        hubo_cambios = False

        for i in range(n):
            for j in range(n):

                # Evitamos sumar rutas inexistentes.
                if distancias[i][k] != INF and distancias[k][j] != INF:
                    nuevo_coste = distancias[i][k] + distancias[k][j]

                    # PUNTO DE INTERRUPCIÓN RECOMENDADO EN SPYDER:
                    # poner el punto rojo en la siguiente línea.
                    if nuevo_coste < distancias[i][j]:
                        coste_anterior = distancias[i][j]

                        distancias[i][j] = nuevo_coste
                        siguiente[i][j] = siguiente[i][k]
                        hubo_cambios = True

                        if mostrar_pasos:
                            anterior = coste_anterior
                            if anterior == INF:
                                anterior = "INF"

                            print(
                                f"  [!] Mejora: {nodos[i]} -> {nodos[j]} "
                                f"pasando por {nodos[k]} | "
                                f"Antes: {anterior} | "
                                f"Ahora: {nuevo_coste}"
                            )

        if mostrar_pasos and not hubo_cambios:
            print("  No se ha mejorado ningún camino en este paso.")

        if mostrar_pasos and mostrar_matriz_en_cada_paso:
            print("Matriz tras este paso:")
            mostrar_matriz(distancias, nodos)

    ciclos_negativos = detectar_ciclos_negativos(distancias, nodos)

    if len(ciclos_negativos) > 0:
        print("\nATENCIÓN: el grafo contiene ciclo negativo.")
        print("Nodos afectados:", ", ".join(ciclos_negativos))
        print("En este caso no existe una solución válida de caminos mínimos.")

    return distancias, siguiente, ciclos_negativos


# ============================================================
# VARIANTE DE WARSHALL
# ============================================================

def warshall(grafo):
    """
    Variante booleana relacionada con Floyd.
    No calcula costes: solo indica si existe camino entre cada par de nodos.
    """
    nodos = grafo.obtener_nodos()
    matriz = grafo.obtener_matriz()
    n = len(nodos)

    alcanzable = []
    for i in range(n):
        fila = []
        for j in range(n):
            if i == j or matriz[i][j] != INF:
                fila.append(True)
            else:
                fila.append(False)
        alcanzable.append(fila)

    for k in range(n):
        for i in range(n):
            for j in range(n):
                alcanzable[i][j] = alcanzable[i][j] or (alcanzable[i][k] and alcanzable[k][j])

    return alcanzable


def mostrar_matriz_booleana(matriz, nodos):
    print("      ", end="")
    for nodo in nodos:
        print(f"{nodo:>8}", end="")
    print()

    for i in range(len(matriz)):
        print(f"{nodos[i]:>6}", end="")
        for j in range(len(matriz[i])):
            valor = "SI" if matriz[i][j] else "NO"
            print(f"{valor:>8}", end="")
        print()
    print()


# ============================================================
# GRAFO DE EJEMPLO: RED DE REPARTO
# ============================================================

def crear_grafo_reparto(bidireccional=False):
    nodos = ["A", "B", "C", "D", "E", "F", "G", "H"]

    matriz = [
        [0,   4,   8,   INF, INF, INF, INF, INF],
        [INF, 0,   INF, 5,   INF, INF, INF, 15],
        [INF, INF, 0,   2,   6,   INF, INF, INF],
        [INF, INF, INF, 0,   INF, 7,   INF, INF],
        [INF, INF, INF, INF, 0,   3,   INF, 8],
        [INF, INF, INF, INF, INF, 0,   4,   INF],
        [INF, INF, INF, INF, INF, INF, 0,   2],
        [INF, INF, INF, INF, INF, INF, INF, 0]
    ]

    grafo = GrafoMatrizCostes(nodos, matriz)

    # Si se quiere defender como grafo no dirigido/conexo, activamos rutas de ida y vuelta.
    if bidireccional:
        aristas = [
            ("A", "B", 4),
            ("A", "C", 8),
            ("B", "D", 5),
            ("B", "H", 15),
            ("C", "D", 2),
            ("C", "E", 6),
            ("D", "F", 7),
            ("E", "F", 3),
            ("E", "H", 8),
            ("F", "G", 4),
            ("G", "H", 2)
        ]

        for origen, destino, coste in aristas:
            grafo.modificar_conexion(origen, destino, coste, bidireccional=True)

    return grafo


# ============================================================
# PRUEBAS PARA PREGUNTAS DEL PROFESOR
# ============================================================

def probar_peso_negativo_sin_ciclo_negativo():
    print("\nPrueba: Floyd con peso negativo sin ciclo negativo")
    nodos = ["A", "B", "C"]
    matriz = [
        [0,   2,   10],
        [INF, 0,   -4],
        [INF, INF, 0]
    ]

    grafo = GrafoMatrizCostes(nodos, matriz)
    distancias, siguiente, ciclos = floyd(grafo, mostrar_pasos=True, mostrar_matriz_en_cada_paso=True)

    if len(ciclos) == 0:
        print("Resultado: el peso negativo es válido porque no forma ciclo negativo.")
        print("Camino A -> C:", " -> ".join(reconstruir_camino(0, 2, siguiente, nodos)))
        print("Coste A -> C:", distancias[0][2])


def probar_ciclo_negativo():
    print("\nPrueba: detección de ciclo negativo")
    nodos = ["A", "B", "C"]
    matriz = [
        [0,   2,   INF],
        [INF, 0,   -5],
        [1,   INF, 0]
    ]

    grafo = GrafoMatrizCostes(nodos, matriz)
    floyd(grafo, mostrar_pasos=True, mostrar_matriz_en_cada_paso=True)


# ============================================================
# MENÚ PRINCIPAL
# ============================================================

def menu():
    # Cambiad a True si queréis usar un grafo de reparto bidireccional.
    # Para mantener la misma matriz de la presentación actual, se deja False.
    grafo = crear_grafo_reparto(bidireccional=False)

    while True:
        print("\n" + "=" * 54)
        print(" MENÚ DEL GESTOR DE RUTAS - ALGORITMO DE FLOYD")
        print("=" * 54)
        print("1. Ver matriz inicial actual")
        print("2. Modificar, añadir o borrar una conexión")
        print("3. Calcular camino mínimo con Floyd")
        print("4. Ver alcanzabilidad con Warshall")
        print("5. Probar peso negativo sin ciclo negativo")
        print("6. Probar detección de ciclo negativo")
        print("7. Salir")

        opcion = input("\nElige una opción (1-7): ")

        if opcion == "1":
            print("\n--- MATRIZ ACTUAL ---")
            mostrar_matriz(grafo.obtener_matriz(), grafo.obtener_nodos())

        elif opcion == "2":
            nodos = grafo.obtener_nodos()
            print(f"\nNodos disponibles: {', '.join(nodos)}")
            origen = input("Nodo de origen: ").upper()
            destino = input("Nodo de destino: ").upper()
            coste = input("Nuevo coste, o INF para borrar conexión: ").upper()
            bidi = input("¿Aplicar también en sentido contrario? (S/N): ").upper() == "S"

            try:
                if coste == "INF":
                    grafo.borrar_conexion(origen, destino, bidireccional=bidi)
                    print("Conexión borrada correctamente.")
                else:
                    coste_num = int(coste)
                    grafo.modificar_conexion(origen, destino, coste_num, bidireccional=bidi)
                    print("Conexión actualizada correctamente.")
            except ValueError as error:
                print("Error:", error)

        elif opcion == "3":
            nodos = grafo.obtener_nodos()
            print(f"\nNodos disponibles: {', '.join(nodos)}")
            origen = input("¿Desde dónde sales?: ").upper()
            destino = input("¿A dónde vas?: ").upper()
            ver_matrices = input("¿Mostrar matriz tras cada paso? (S/N): ").upper() == "S"

            try:
                idx_origen = nodos.index(origen)
                idx_destino = nodos.index(destino)

                print("\n" + "*" * 54)
                print(" INICIANDO ALGORITMO DE FLOYD")
                print("*" * 54)

                distancias, siguiente, ciclos = floyd(
                    grafo,
                    mostrar_pasos=True,
                    mostrar_matriz_en_cada_paso=ver_matrices
                )

                if len(ciclos) == 0:
                    camino = reconstruir_camino(idx_origen, idx_destino, siguiente, nodos)

                    print("\n" + "*" * 54)
                    print(" RESULTADO FINAL DE LA CONSULTA")
                    print("*" * 54)

                    if camino is None:
                        print(f"No existe camino desde {origen} hasta {destino}.")
                    else:
                        print(f"Ruta óptima: {' -> '.join(camino)}")
                        print(f"Coste total: {distancias[idx_origen][idx_destino]} minutos")

            except ValueError:
                print("Error: los nodos introducidos no existen.")

        elif opcion == "4":
            print("\n--- WARSHALL: EXISTENCIA DE CAMINOS ---")
            print("SI significa que existe algún camino entre esos dos nodos.")
            alcanzable = warshall(grafo)
            mostrar_matriz_booleana(alcanzable, grafo.obtener_nodos())

        elif opcion == "5":
            probar_peso_negativo_sin_ciclo_negativo()

        elif opcion == "6":
            probar_ciclo_negativo()

        elif opcion == "7":
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Inténtalo de nuevo.")


if __name__ == "__main__":
    menu()
