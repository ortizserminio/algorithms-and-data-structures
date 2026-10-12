from abc import ABC, abstractmethod
import random
import time

# INTERFAZ
class LibroGenerico(ABC):
    @abstractmethod
    def __init__(self,ISBN,titulo,paginas,genero,retraso):
        pass

class PilaGenerica(ABC):
    @abstractmethod
    def __init__(self, capacidad=100):
        self.capacidad = capacidad
        self.elementos = [None] * capacidad
        self.ultimo = 0

    @abstractmethod
    def esta_vacia(self):
        pass

    @abstractmethod
    def apilar(self, e):
        pass

    @abstractmethod
    def desapilar(self):
        pass

    @abstractmethod
    def tope(self):
        pass

    @abstractmethod
    def imprimir(self):
        pass

# IMPLEMENTACIÓN
class Libro(LibroGenerico):
    def __init__(self, ISBN, titulo, paginas, genero, retraso):
        # Inicializa un libro con los atributos proporcionados.
        self.ISBN = ISBN
        self.titulo = titulo
        self.paginas = paginas
        self.genero = genero
        self.retraso = retraso

    @classmethod
    def generar_libro(cls):
        # Método de clase para generar un libro con valores aleatorios.
        ISBN = random.randint(100000, 999999)
        titulo = f"Libro {ISBN}"
        paginas = random.randint(100, 1000)
        genero = random.choice(["Ensayo", "Novela", "Poesía"])
        retraso = random.choice([True, False])
        return cls(ISBN, titulo, paginas, genero, retraso)

class Pila(PilaGenerica):
    def __init__(self, capacidad=100):
        # Inicializa una pila con una capacidad dada.
        self.capacidad = capacidad
        self.elementos = [None] * capacidad
        self.ultimo = 0

    def esta_vacia(self):
        # Devuelve True si la pila está vacía, False en caso contrario.
        return self.ultimo == 0

    def apilar(self, e):
        # Apila un elemento en la pila si no está llena.
        if self.ultimo >= self.capacidad:
            print("La pila está llena.")
        else:
            self.elementos[self.ultimo] = e
            self.ultimo += 1

    def desapilar(self):
        # Desapila un elemento de la pila si no está vacía.
        if self.esta_vacia():
            print("La pila está vacía. No se puede desapilar.")
            return None
        else:
            self.ultimo -= 1
            return self.elementos[self.ultimo]

    def tope(self):
        # Devuelve el elemento en el tope de la pila si no está vacía.
        if self.esta_vacia():
            print("La pila está vacía.")
            return None
        else:
            return self.elementos[self.ultimo - 1]
     
    def imprimir(self):
        # Devuelve una cadena con los ISBN de los libros en la pila.
        if self.esta_vacia():
            return "La pila está vacía."
        else:
            return ", ".join(str(libro.ISBN) for libro in self.elementos[:self.ultimo])

# Simulación
def simulacion():
    # Inicializa las pilas para libros devueltos y para cada género.
    LibrosDevueltos = Pila()
    pila_ensayo = Pila()
    pila_novela = Pila()
    pila_poesia = Pila()

    tiempo_inicial = time.time()
    tiempo_limite = 30  
    
    print("Iniciando simulación...")
    print(f"La biblioteca estará abierta durante {tiempo_limite} segundos.")

    while time.time() - tiempo_inicial < tiempo_limite:
        tiempo_transcurrido = int(time.time() - tiempo_inicial)
        print("________________________________________________________")
        print(f"Tiempo transcurrido: {tiempo_transcurrido}s")

        # Cada 2 segundos, se devuelve un libro
        if tiempo_transcurrido % 2 == 0:
            libro = Libro.generar_libro()
            LibrosDevueltos.apilar(libro)
            print(f"EVENTO: Libro devuelto: {libro.ISBN}")
            print("________________________________________________________")
            print(f"LibrosDevueltos: {LibrosDevueltos.imprimir()}")
            print(f"Pila Ensayo: {pila_ensayo.imprimir()}")
            print(f"Pila Novela: {pila_novela.imprimir()}")
            print(f"Pila Poesía: {pila_poesia.imprimir()}")
    
        # Cada 3 segundos, se ordena un libro
        if tiempo_transcurrido % 3 == 0:
            if not LibrosDevueltos.esta_vacia():
                libro = LibrosDevueltos.desapilar()
                if libro.genero == "Ensayo":
                    pila_ensayo.apilar(libro)
                elif libro.genero == "Novela":
                    pila_novela.apilar(libro)
                elif libro.genero == "Poesía":
                    pila_poesia.apilar(libro)
                print(f"EVENTO: Libro ordenado en la pila {libro.genero}: {libro.ISBN}")
                if libro.retraso:
                    print(f"AVISO: El libro {libro.ISBN} fue devuelto con retraso.")
                    print("________________________________________________________")
                print(f"LibrosDevueltos: {LibrosDevueltos.imprimir()}")
                print(f"Pila Ensayo: {pila_ensayo.imprimir()}")
                print(f"Pila Novela: {pila_novela.imprimir()}")
                print(f"Pila Poesía: {pila_poesia.imprimir()}")

        time.sleep(1)  # Esperar 1 segundo antes de la siguiente iteración

    print("Biblioteca cerrada. Ordenando libros restantes...")
    # Ordenar libros restantes después de cerrar la biblioteca
    while not LibrosDevueltos.esta_vacia() or not pila_ensayo.esta_vacia() or not pila_novela.esta_vacia() or not pila_poesia.esta_vacia():
        if not LibrosDevueltos.esta_vacia():
            libro = LibrosDevueltos.desapilar()
            print(f"EVENTO: El libro {libro.ISBN} ha sido devuelto a su estantería.")
            time.sleep(1)

        pila_random = random.choice([pila_ensayo, pila_novela, pila_poesia])
        if not pila_random.esta_vacia():
            libro = pila_random.desapilar()
            print(f"EVENTO: El libro {libro.ISBN} ha sido devuelto a su estantería.")
            time.sleep(2)

    print("___________________________________________________________")
    print("Simulación finalizada. Todas las pilas han sido ordenadas.")

# MAIN
if __name__ == "__main__":
    # Inicializa las pilas para libros devueltos y para cada género.
    LibrosDevueltos = Pila()
    pila_ensayo = Pila()
    pila_novela = Pila()
    pila_poesia = Pila()

    while True:
        print("___________________________________MENU_________________________________")
        print("1. Devolver un libro a la pila de LibrosDevueltos")
        print("2. Ordenar un libro de LibrosDevueltos a su pila de género")
        print("3. Imprimir la pila LibrosDevueltos")
        print("4. Imprimir una de las pilas de género: 1, 2, 3")
        print("5. Ver información sobre el próximo libro a ordenar de LibrosDevueltos")
        print("6. Iniciar la simulación")
        print("7. Salir de la aplicación")

        opcion = int(input("Seleccione una opción: "))
        match opcion:
            case 1:
                # Devuelve un libro a la pila de LibrosDevueltos.
                libro = Libro.generar_libro()
                LibrosDevueltos.apilar(libro)
                print(f"Libro devuelto: ISBN: {libro.ISBN}, Título: {libro.titulo}, Páginas: {libro.paginas}, Género: {libro.genero}, Retraso: {libro.retraso}")

            case 2:
                # Ordena un libro de LibrosDevueltos a su pila de género.
                if LibrosDevueltos.esta_vacia():
                    print("No hay libros en la pila de LibrosDevueltos.")
                else:
                    libro = LibrosDevueltos.desapilar()
                    if libro.genero == "Ensayo":
                        pila_ensayo.apilar(libro)
                    elif libro.genero == "Novela":
                        pila_novela.apilar(libro)
                    elif libro.genero == "Poesía":
                        pila_poesia.apilar(libro)
                    print(f"Libro ordenado en la pila {libro.genero}: ISBN: {libro.ISBN}, Título: {libro.titulo}, Páginas: {libro.paginas}, Género: {libro.genero}, Retraso: {libro.retraso}")

            case 3:
                # Imprime la pila de LibrosDevueltos.
                print("Libros Devueltos:", LibrosDevueltos.imprimir())

            case 4:
                # Imprime una de las pilas de género.
                print("1. Pila Ensayo")
                print("2. Pila Novela")
                print("3. Pila Poesía")
                subopcion = int(input("Seleccione una pila: "))
                
                if subopcion == 1:
                    print("Pila Ensayo:", pila_ensayo.imprimir())
                elif subopcion == 2:
                    print("Pila Novela:", pila_novela.imprimir())
                elif subopcion == 3:
                    print("Pila Poesía:", pila_poesia.imprimir())
                else:
                    print("Opción no válida.")

            case 5:
                # Muestra información sobre el próximo libro a ordenar.
                if LibrosDevueltos.esta_vacia():
                    print("No hay libros en la pila de LibrosDevueltos.")
                else:
                    libro = LibrosDevueltos.tope()
                    print(f"Próximo libro a ordenar: ISBN: {libro.ISBN}, Título: {libro.titulo}, Páginas: {libro.paginas}, Género: {libro.genero}, Retraso: {libro.retraso}")

            case 6:
                # Inicia la simulación.
                print("Iniciando simulación")
                simulacion()

            case 7:
                # Sale de la aplicación.
                break

            case _:
                # Maneja opciones no válidas.
                print("Opción no válida. Intente de nuevo.")