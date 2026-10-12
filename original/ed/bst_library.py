import random
from abc import ABC, abstractmethod
import time


#Interfaz
class LibroGenerico(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass
#Interfaz para el arbol
class ABBGenerico(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def insertar_recursivo(self, libro):
        pass

    @abstractmethod
    def eliminar_recursivo(self, actual, id_libro):
        pass

    @abstractmethod
    def buscar_recursivo(self, actual, id_libro):
        pass

    @abstractmethod
    def inorder(self, actual):
        pass

    @abstractmethod
    def preorder(self, actual):
        pass

    @abstractmethod
    def postorder(self, actual):
        pass
#implemetacion
class Libro(LibroGenerico):
    
    def __init__(self, id_libro, titulo, paginas, genero, retraso):
        self.id_libro = id_libro
        self.titulo = titulo
        self.paginas = paginas
        self.genero = genero
        self.retraso = retraso
        self.izquierda = None
        self.derecha = None

    @classmethod
    def generar_libro(cls):
        id_libro = random.randint(100000, 999999)
        titulo = f"Libro {id_libro}"
        paginas = random.randint(50, 500)
        genero = random.choice(["ensayo", "novela", "poesia"])
        retraso = random.choice([True, False])
        return cls(id_libro, titulo, paginas, genero, retraso)
    #IA
    def generar_titulo(self):
        palabras = ["El", "misterio", "de", "la", "noche", "oscura", "sol", "luna", "ciudad", "perdida", "secreto", 
                    "antiguo", "libro", "magico", "aventuras", "en", "el", "tiempo", "ultimo", "deseo"]
        return ' '.join(random.sample(palabras, random.randint(2, 5))).capitalize()
    
    def __str__(self):
       return f"ID: {self.id_libro}, Título: {self.titulo}, Páginas: {self.paginas}, Género: {self.genero}, Retraso: {self.retraso}"
   
class Arbol(ABBGenerico):
    def __init__(self, genero): 
        self.raiz = None
        self.genero = genero
        
    def insertar(self, libro):
        self.raiz = self.insertar_recursivo(self.raiz, libro) 
        
    def insertar_recursivo(self, actual, libro):  
        if actual is None:
            return libro 
        else:
            if libro.id_libro > actual.id_libro:
                actual.derecha = self.insertar_recursivo(actual.derecha, libro)  
            elif libro.id_libro < actual.id_libro:
                actual.izquierda = self.insertar_recursivo(actual.izquierda, libro)  
            return actual
            
    # Inorden
    def inorder(self):
        if self.raiz is None:
            print("El Árbol está vacío.")
            return 
        self.inorder_recursivo(self.raiz)
    
    def inorder_recursivo(self, libro_actual):
        if libro_actual:
            self.inorder_recursivo(libro_actual.izquierda)
            print(f"{libro_actual.id_libro}", end=" ")
            self.inorder_recursivo(libro_actual.derecha)
    
    # Preorden
    def preorder(self):
        if self.raiz is None:
            print("El Árbol está vacío.")
            return
        self.preorder_recursivo(self.raiz)
    
    def preorder_recursivo(self, libro_actual):
        if libro_actual:
            print(f"{libro_actual.id_libro}", end=" ")
            self.preorder_recursivo(libro_actual.izquierda)
            self.preorder_recursivo(libro_actual.derecha)
    
    # Postorden
    def postorder(self):
        if self.raiz is None:
            print("El Árbol está vacío.")
            return
        self.postorder_recursivo(self.raiz)
    
    def postorder_recursivo(self, libro_actual):
        if libro_actual:
            self.postorder_recursivo(libro_actual.izquierda)
            self.postorder_recursivo(libro_actual.derecha)
            print(f"{libro_actual.id_libro}", end=" ")

   
    def buscar(self, id_libro): 
        return self.buscar_recursivo(self.raiz, id_libro)
   
    def buscar_recursivo(self, actual, id_libro): 
        if actual is None:
            return None
        if actual.id_libro == id_libro: 
            return actual
        if id_libro < actual.id_libro: 
            return self.buscar_recursivo(actual.izquierda, id_libro)
        return self.buscar_recursivo(actual.derecha, id_libro)
            
    def eliminar(self, id_libro): 
        self.raiz = self.eliminar_recursivo(self.raiz, id_libro)
        
    def eliminar_recursivo(self, actual, id_libro):  
        if actual is None:
            return None
        if id_libro < actual.id_libro: 
            actual.izquierda = self.eliminar_recursivo(actual.izquierda, id_libro)  
        elif id_libro > actual.id_libro:  
            actual.derecha = self.eliminar_recursivo(actual.derecha, id_libro)
        else:
            if actual.izquierda is None:
                return actual.derecha
            if actual.derecha is None:  
                return actual.izquierda 
            else:
                sucesor = self.min_valor_nodo(actual.derecha)  
                actual.id = sucesor.id
                actual.derecha = self.eliminar_recursivo(actual.derecha, sucesor.id)
        return actual  
                
    def min_valor_nodo(self, actual): 
        while actual.izquierda is not None:  
            actual = actual.izquierda
        return actual  
        
    def mostrar_libros(self):
        ids = self.inorden()
        if not ids:
            print(f"ABB {self.genero}: Vacío")
            return
            
        output = f"ABB {self.genero}: " + str(ids[0])
        for id_libro in ids[1:]:
            output += ", " + str(id_libro)
        print(output)
        
def mostrar_recorrido(self,arbol, tipo='inorden'):
        if arbol is None or arbol.raiz is None:
            print("EL arbol esta vacio")
            return
        
        # Obtener la lista de IDs según el recorrido
        if tipo == 'preorden':
            lista_ids = arbol.preorden()
        elif tipo == 'postorden':
            lista_ids = arbol.postorden()
        else:  # Por defecto inorden
            lista_ids = arbol.inorden()
        
        # Mostrar cada libro
        for id_libro in lista_ids:
            libro = arbol.buscar(id_libro)
            if libro:  
                print(f"ID: {libro.id_libro}, Título: {libro.titulo}, Páginas: {libro.paginas}, Retraso: {libro.retraso}")
        
def mostrar_estado_arboles():
    for genero, arbol in arboles.items():
        print(f"\nABB {genero}: ", end="")
        # Esto imprimirá todos los IDs separados por espacios
        arbol.inorder()

        
       
            
#Simulacion

def simulacion():
    abb_num = {
        "ensayo": 1,
        "novela": 2,
        "poesia": 3
    }
    def _ids_inorder(arbol):
        ids = []
        def _rec(nodo):
            if nodo:
                _rec(nodo.izquierda)
                ids.append(nodo.id_libro)
                _rec(nodo.derecha)
        _rec(arbol.raiz)
        return ids
    print("\n--- INICIANDO SIMULACIÓN ---\n")
    tiempo_inicio = time.time()
    while True:
        t = int(time.time() - tiempo_inicio)
        if t >= 60:
            break
        if t > 0 and t % 5 == 0:
            libro = Libro.generar_libro()
            arboles[libro.genero].insertar(libro)
            time.sleep(1)  
        if t > 0 and t % 7 == 0:
            disponibles = [g for g, a in arboles.items() if a.raiz is not None]
            if disponibles:
                genero = random.choice(disponibles)
                arbol = arboles[genero]
                ids = _ids_inorder(arbol)
                id_libro = random.choice(ids)
                libro = arbol.buscar(id_libro)
                if libro.retraso:
                    arbol.eliminar(id_libro)
                    print(
                        f"\nEVENTO: Se detecta retraso en la devolución "
                        f"del libro {id_libro} del ABB{abb_num[genero]}."
                    )
                else:
                    print(
                        f"\nEVENTO: Se devuelve el libro con id {id_libro} "
                        f"al ABB{abb_num[genero]}."
                    )
                mostrar_estado_arboles()  
                time.sleep(1)
        time.sleep(0.1)
    mostrar_estado_arboles()
#Main
arboles = {
    "ensayo": Arbol("ensayo"),
    "novela": Arbol("novela"),
    "poesia": Arbol("poesia")
    }
    
while True:
    print("\n--- MENÚ BIBLIOTECA ---")
    print("1. Insertar un libro")
    print("2. Buscar un libro")
    print("3. Imprimir lista de libros")
    print("4. Borrar un libro")
    print("5. Generar libros aleatorios")
    print("6. Eliminar libros aleatorios")
    print("7. Iniciar simulación")
    print("8. Salir")
    
    opcion = input("Seleccione una opción: ")
    
    match opcion:
        case "1": 
            tipo = input("¿En qué árbol deseas colocar tu libro? (ensayo, novela, poesia): ")
            # Aquí no hacemos conversiones: el usuario debe teclear exactamente A, B o C
            if tipo not in arboles:
                print("El árbol debe ser ensayo, novela o poesia.")
                continue
            
            try:
                id_libro = int(input("Dame el ID del libro (6 dígitos): "))
                if not (100000 <= id_libro <= 999999):
                    print("ID no válido. Tiene que ser de 6 dígitos.")
                    continue
            except ValueError:
                print("El ID debe ser un número de 6 dígitos.")
                continue
        
            libro = Libro.generar_libro()
            libro.id_libro = id_libro
            libro.genero = tipo  
        
            arboles[tipo].insertar(libro)
            print(f"\nLibro insertado en el ABB {tipo}")
            mostrar_estado_arboles()

            
                
        case "2":
            try:
                #pedir el libro que deseas buscar
                id_libro = int(input("Ingrese el ID del libro a buscar: "))
                if 100000 <= id_libro <= 999999:
                    print("El ID del libro es válido :)")
                else:
                    print("ID no válido")
                    continue

                libro_encontrado = None
                arbol_encontrado = None
                
                for nombre_arbol, arbol in arboles.items():
                    resultado = arbol.buscar(id_libro)
                    if resultado:
                        libro_encontrado = resultado
                        arbol_encontrado = nombre_arbol
                        break  
                
                if libro_encontrado:
                    print(f"\nLibro encontrado en el ABB {arbol_encontrado}:")
                    print(libro_encontrado)
                else:
                    print("\nEl libro no fue encontrado en ningún árbol.")
            except ValueError:
                print("Error: El ID debe ser un número entero.")
                
        case "3":
            if all(arbol.raiz is None for arbol in arboles.values()):
                print("No hay libros en la biblioteca.")
                continue
            
                # 2) Pedir tipo de recorrido
            tipo = input("Tipo de recorrido (inorden/preorden/postorden): ")
            if tipo not in ("inorden", "preorden", "postorden"):
                print("Tipo de recorrido no válido. Debe ser exactamente 'inorden', 'preorden' o 'postorden'")
                continue
            
                # 3) Para cada árbol, invocar el método adecuado y mostrar sus IDs
            for genero, arbol in arboles.items():
                # Título
                print(f"ABB {genero.capitalize()}: ", end="")
        
                # Dependiendo de 'tipo', llamamos al método de la instancia:
                if tipo == "inorden":
                    arbol.inorder()    # imprime ids con espacios
                elif tipo == "preorden":
                    arbol.preorder()
                else:  # postorden
                    arbol.postorder()
           
        case "4":
            try:
                # Pedir ID del libro a borrar
                id_libro = int(input("Ingrese el ID del libro a borrar (6 dígitos): "))
                
                # Validar que el ID tenga 6 dígitos
                if 100000 <= id_libro <= 999999:
                    print("El ID del libro es válido :)")
                else:
                    print("ID no válido")
                    continue
                
                libro_encontrado = False
                
                # Buscar y eliminar en cada árbol
                for genero, arbol in arboles.items():
                    libro = arbol.buscar(id_libro)
                    if libro:
                        arbol.eliminar(id_libro)
                        print(f"\nLibro eliminado del ABB {genero}:")
                        print(f"ID: {libro.id_libro}, Título: {libro.titulo}")
                        libro_encontrado = True
                        break  
                
                if not libro_encontrado:
                    print("\nNo se encontró ningún libro con ese ID en la biblioteca")
                    
                # Mostrar estado actual de los árboles
                mostrar_estado_arboles()
                
            except ValueError:
                print("Error: Debes ingresar un número válido de 6 dígitos")
                
        case "5":
            try:
                # Pedir cantidad de libros a generar
                cantidad = int(input("¿Cuántos libros deseas generar? "))
                if cantidad <= 0:
                    print("La cantidad debe ser un número positivo")
                    continue
                
                # Mostrar opciones de género
                print("\nSelecciona el género:")
                print("1. Ensayo")
                print("2. Novela")
                print("3. Poesía")
                
                # Pedir selección de género
                opcion_genero = input("Ingrese el número correspondiente al género (1-3): ")
                
                # Validar opción de género
                if opcion_genero not in ['1', '2', '3']:
                    print("Opción no válida. Debe ser 1, 2 o 3")
                    continue
                
                # Mapear opción a género
                generos = {'1': 'ensayo', '2': 'novela', '3': 'poesia'}
                genero_seleccionado = generos[opcion_genero]
                
                # Generar los libros
                for _ in range(cantidad):
                    libro = Libro.generar_libro()
                    # Forzar el género seleccionado
                    libro.genero = genero_seleccionado
                    arboles[genero_seleccionado].insertar(libro)
                    
                #Mostrar el estado de los arboles 
                mostrar_estado_arboles()
                
            except ValueError:
                print("Error: Debes ingresar un número válido para la cantidad")
        case "6":
            try:
                # Pedir cantidad de libros a eliminar
                cantidad = int(input("¿Cuántos libros aleatorios deseas eliminar? "))
                if cantidad <= 0:
                    print("La cantidad debe ser un número positivo")
                    continue
                
                # Obtener todos los IDs existentes en todos los árboles
                todos_ids = []
                for arbol in arbol.values():
                    todos_ids.extend(arbol.inorden())
                
                # Verificar si hay libros para eliminar
                if not todos_ids:
                    print("No hay libros en la biblioteca para eliminar")
                    continue
                    
                # Asegurarnos de no intentar eliminar más libros de los existentes
                cantidad = min(cantidad, len(todos_ids))
                
                # Seleccionar IDs aleatorios para eliminar
                ids_a_eliminar = random.sample(todos_ids, cantidad)
                
                # Eliminar los libros seleccionados
                eliminados = 0
                for id_libro in ids_a_eliminar:
                    for arbol in arbol.values():
                        libro = arbol.buscar(id_libro)
                        if libro:
                            arbol.eliminar(id_libro)
                            eliminados += 1
                            break  # Pasar al siguiente ID
                
                # Mostrar resultados
                print(f"\nSe eliminaron {eliminados} libros aleatorios:")
                print(", ".join(str(id) for id in ids_a_eliminar))
                
                # Mostrar estado actualizado
                mostrar_estado_arboles()
                
            except ValueError:
                print("Error: Debes ingresar un número válido")
        case "7":
            print ("Ejecutando la simulacion")
            simulacion()
        case "8":
            print("Saliendo del programa...")
            break
        case _:
            print("Opción no válida. Intente nuevamente.")


