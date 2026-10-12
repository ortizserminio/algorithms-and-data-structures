# -*- coding: utf-8 -*-
"""
Autor: Esterly 

Especificacion formal de la practica : 
    
TAD Humano 

CONJUNTOS 

H  Conjunto de Humanos
N  Conjuntos de enteros
S  Conjuntos de strings
T  Conjuntos de time 
B  Conjuntos de booleanos

SINTAXIS 

CrearHumano      --> H
Gritar        H  --> S

SEMANTICA 

Gritar(CrearHumano()) = f "soy {nombre}"



TAD ColaAbduccion 

CONJUNTOS 

C Conjutos de ColaAbduccion 
H Conjuntos de humanos 
B  Conjuntos de booleanos
N Conjuntos de enteros 
S COnjuntos de strings
M1 Conjuntos de erores "NO hay humanos"
M2 Conjunto de errores "No existe e"

SINTAXIS 

*CrearCola    --> C
CosultarVacia C --> B
*Encolar       HxC --> C
Desencolar   C --> (CxH) u M
Frente       C --> H u M
Tamaño       C --> C
*Concatenar    C x C --> C
EliminarH        C x H --> (C x B) U M
Resto            C --> ?C

SEMANTICA

Para todo h, h1 ∈ H y c1,c2 ∈ C

1. ConsultarVacio(CrearCola()) = true
2. ConsultarVacio(Encolar(c1,h)) = false
3. ConsultarVacio(Concatenar(c1,c2)) =
   Si ConsultarVacio(c1) AND ConsultarVacio(c2) --> true | false

4. Desencolar(CrearCola()) = "No hay humanos"
5. Desencolar(Encolar(c1,h)) = Si ConsultarVacio(c1)
   --> [CrearCola(), h] | [resto(c1), Frente(c1)]

6. Desencolar(Concatenar(c1,c2)) = Si ConsultarVacio(c1)
   --> [resto(c2), Frente(c2)] | [resto(c1), Frente(c1)]

7. Frente(CrearCola()) = "No hay humanos"
8. Frente(Encolar(c1,h)) = Si ConsultarVacio(c1) --> h | Frente(c1)
9. Frente(Concatenar(c1,c2)) = Si ConsultarVacio(c1) --> Frente(c2) | Frente(c1)

10. EliminarH(h,CrearCola()) = "No hay humanos"
11. EliminarH(h1,Encolar(c1,h)) = Si h1 == h [c1,true] | [Encolar(c1,h),false]
12. EliminarH(h,Concatenar(Encolar(c1,h),Encolar(c2,h))) = Concatenar(c1,c2)

"""
from abc import ABC, abstractmethod
import time
import random


# =============================================================================
#  INTERFACES
# =============================================================================

class Humano_Interfaz(ABC):
    
    @abstractmethod
    def gritar(self):
        pass
        
class ColaAbduccion_Interfaz(ABC):

    @abstractmethod
    def CrearCola(cls):
        pass

    @abstractmethod
    def ConsultarVacia(self):
        pass

    @abstractmethod
    def Encolar(self, h):
        pass

    @abstractmethod
    def Desencolar(self):
        pass

    @abstractmethod
    def Frente(self):
        pass

    @abstractmethod
    def Tam(self):
        pass

    @abstractmethod
    def Concatenar(self, c2):
        pass

    @abstractmethod
    def EliminarHumano(self, h):
        pass
    
class PilaGenerica(ABC):
 
    @abstractmethod
    def apilar(self, humano):
        pass
 
    @abstractmethod
    def desapilar(self):
        pass
 
    @abstractmethod
    def mostrarPila(self):
        pass


# =============================================================================
#  HUMANO 
# =============================================================================

class Humano(Humano_Interfaz):

    def __init__(self):
        self.id          = str(random.randint(10000000, 999999999)) + random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.nombre       = "Humano_" + str(random.randint(10, 99))
        self.nivel_miedo  = random.choice(["Bajo", "Medio", "Alto"])
        self.hora_captura = time.time()
        self.apto         = random.choice([True, False])
        self.siguiente    = None

    def gritar(self):
        if self.nivel_miedo == "Bajo":
            print(f"susurra soy {self.nombre}")
        elif self.nivel_miedo == "Medio":
            print(f"Soy {self.nombre}!")
        else:
            print(f"¡¡SOY {self.nombre.upper()}!!")

    def __str__(self):
        hora = time.strftime("%H:%M:%S", time.localtime(self.hora_captura))
        return (f"  ID: {self.id}\n"
                f"  Nombre: {self.nombre}\n"
                f"  Nivel de miedo: {self.nivel_miedo}\n"
                f"  Hora de captura: {hora}\n"
                f"  Apto: {self.apto}")


# =============================================================================
#  COLA
# =============================================================================

class ColaAbduccion(ColaAbduccion_Interfaz):

    def __init__(self):
        self.primero = None
        self.ultimo  = None

    def CrearCola(cls):
        return cls()

    def ConsultarVacia(self):
        return self.primero is None

    def Encolar(self, h):
        if self.ConsultarVacia():
            self.primero = h
            self.ultimo  = h
        else:
            self.ultimo.siguiente = h
            self.ultimo = h
        h.siguiente = None

    def Desencolar(self):
        if self.ConsultarVacia():
            print("No hay humanos")
            return None
        humano_salir = self.primero
        self.primero = self.primero.siguiente
        if self.primero is None:
            self.ultimo = None
        humano_salir.siguiente = None
        return humano_salir

    def Frente(self):
        return self.primero

    def Tam(self):
        contador, actual = 0, self.primero
        while actual is not None:
            contador += 1
            actual = actual.siguiente
        return contador

    def Concatenar(self, c2):
        if c2.ConsultarVacia():
            return
        
        if self.ConsultarVacia():
            self.primero = c2.primero
            self.ultimo = c2.ultimo
        else:
            self.ultimo.siguiente = c2.primero
            self.ultimo = c2.ultimo
            
        c2.primero = None
        c2.ultimo = None

    def EliminarHumano(self, h):
        if self.ConsultarVacia():
            print("No hay humanos")
            return None, False
    
        cola_aux = ColaAbduccion()
        encontrado = False
    
        while not self.ConsultarVacia():
            actual = self.Desencolar()
            if actual.id == h.id and not encontrado:
                encontrado = True
            else:
                cola_aux.Encolar(actual)
    
        # Restaurar la cola original con los elementos restantes
        while not cola_aux.ConsultarVacia():
            self.Encolar(cola_aux.Desencolar())
    
        return self, encontrado

    def __str__(self):
        if self.ConsultarVacia():
            return "  (vacia)"
        resultado = ""
        actual = self.primero
        while actual is not None:
            resultado += actual.nombre
            if actual.siguiente is not None:
                resultado += " -> "
            actual = actual.siguiente
        return resultado


# =============================================================================
#  PILA 
# =============================================================================

class Pila(PilaGenerica):

    def __init__(self):
        self.cabeza = None

    def apilar(self, humano):
        humano.siguiente = self.cabeza
        self.cabeza = humano

    def desapilar(self):
        if self.cabeza is None:
            return None
        humano_desapilado = self.cabeza
        self.cabeza = humano_desapilado.siguiente
        humano_desapilado.siguiente = None
        return humano_desapilado

    def mostrarPila(self):
        actual = self.cabeza
        while actual is not None:
            print(actual.nombre, end=" -> ")
            actual = actual.siguiente
        print()


# =============================================================================
#  clasificar_en_pila: lógica de negocio
# =============================================================================

def clasificar_en_pila(humano, p_buenos, p_regulares, p_descartes):
    if humano is None:
        return
    if humano.nivel_miedo == "Bajo":
        p_buenos.apilar(humano)
        print(f"  -> Pila_Buenos: {humano.nombre}")
    elif humano.nivel_miedo == "Medio":
        p_regulares.apilar(humano)
        print(f"  -> Pila_Regulares: {humano.nombre}")
    else:
        p_descartes.apilar(humano)
        print(f"  -> Pila_Descartes: {humano.nombre}")


# =============================================================================
#  SIMULACIÓN
# =============================================================================

def simulacion(c1, c2, p_buenos, p_regulares, p_descartes):
    tiempo_inicio  = time.time()
    ultimo_encolar = ultimo_abducir = ultimo_analisis = -1

    # FASE 1
    print("\n=== FASE 1: Capturas y abducciones (30 s) ===")
    while True:
        t = int(time.time() - tiempo_inicio)

        if t >= 30:
            break

        # Cada 2 s: nuevas capturas
        if t % 2 == 0 and t != ultimo_encolar:
            h1 = Humano()
            h2 = Humano()
            c1.Encolar(h1)
            c2.Encolar(h2)
            print(f"\n[t={t}s] Nuevas capturas:")
            print(h1)
            print(h2)
            ultimo_encolar = t

        # Cada 3 s: abduccion y clasificacion en pilas
        if t % 3 == 0 and t != ultimo_abducir:
            print(f"\n[t={t}s] ABDUCCION:")
            for cola, nombre in [(c1, "C1"), (c2, "C2")]:
                abducido = cola.Desencolar()
                if cola.Desencolar():
                    print(f"  Abducido de {nombre}:\n{abducido}")
                    clasificar_en_pila(abducido, p_buenos, p_regulares, p_descartes)
            ultimo_abducir = t

        # Cada 5 s (EXTRA): Pila_Buenos envia un humano a analisis
        if t % 5 == 0 and t != ultimo_analisis and t > 0:
            analizado = p_buenos.desapilar()
            if analizado:
                print(f"\n[t={t}s] EXTRA - {analizado.nombre} enviado a analisis experimental")
            ultimo_analisis = t

        time.sleep(1)

    # FASE 2
    print("\n=== FASE 2: La nave cierra capturas, procesando pilas ===")
    print(f"Cola C1:\n{c1}")
    print(f"Cola C2:\n{c2}")
    print("Pila_Buenos:    ", end=""); p_buenos.mostrarPila()
    print("Pila_Regulares: ", end=""); p_regulares.mostrarPila()
    print("Pila_Descartes: ", end=""); p_descartes.mostrarPila()
 
    while not (p_buenos.cabeza is None and
               p_regulares.cabeza is None and
               p_descartes.cabeza is None):
 
        p_buenos.desapilar()
        p_regulares.desapilar()
        p_descartes.desapilar()
        
        print("____________________________________________________________________")
        print("Buenos:", end=""); p_buenos.mostrarPila()
        print("Regulares:", end=""); p_regulares.mostrarPila()
        print("Descartes:", end=""); p_descartes.mostrarPila()
        time.sleep(1)
 
    print("\n=== Todas las pilas vacias. Mision completada ===")


# =============================================================================
#  MENÚ
#==============================================================================

def menu_interactivo():
    c1 = ColaAbduccion.CrearCola()
    c2 = ColaAbduccion.CrearCola()
    p_buenos    = Pila()
    p_regulares = Pila()
    p_descartes = Pila()

    while True:
        print("\n--- MENU ---")
        print("-- Cola --")
        print("1.  Encolar humano en C1")
        print("2.  Encolar humano en C2")
        print("3.  Frente de una cola")
        print("4.  Desencolar de una cola")
        print("5.  Tamano de una cola")
        print("6.  Cola vacia?")
        print("7.  Concatenar C1 <- C2")
        print("8.  Concatenar C2 <- C1")
        print("9.  Eliminar humano")
        print("10. Mostrar C1 y C2")
        print("11. Gritar")
        print("12. Iniciar simulacion")
        print("0.  Salir")

        opcion = input("Opcion: ")

        match opcion:
            case "1":
                h = Humano()
                c1.Encolar(h)
                print(f"Encolado en C1:\n{h}")

            case "2":
                h = Humano()
                c2.Encolar(h)
                print(f"Encolado en C2:\n{h}")

            case "3":
                if c1.ConsultarVacia():
                    print("C1 vacia")
                else:
                    print("Primero en C1:", c1.Frente().nombre)
                    
                if c2.ConsultarVacia():
                    print("C2 vacia")
                else:
                    print("Primero en C2:", c2.Frente().nombre)

            case "4":
                cual = input("De que cola desencolar (1/2): ")
                cola = 0
                if cual == "1" :
                    cola = c1
                else :
                    cola = c2
                    
                h = cola.Desencolar()
                clasificar_en_pila(h, p_buenos, p_regulares, p_descartes)

            case "5":
                print("Tamano C1:", c1.Tam())
                print("Tamano C2:", c2.Tam())

            case "6":
                print("C1 vacia:\n", c1.ConsultarVacia())
                print("C2 vacia:\n", c2.ConsultarVacia())

            case "7":
                c1.Concatenar(c2)
                print("Ya se han concatenado")

            case "8":
                c2.Concatenar(c1)
                print("Ya se han concatenado")
            
            case "9":
                print("Eliminado de C1:", c1.EliminarHumano(None).nombre)
                print("Eliminado de C2:", c2.EliminarHumano(None).nombre)
            
            case "10":
                print(f"Cola C1:\n {c1}")
                print(f"Cola C2:\n {c2}")
                
            case "11":
                if c1.ConsultarVacia():
                    print("C1 vacia")
                else:
                    c1.Frente().gritar()
                    
                if c2.ConsultarVacia():
                    print("C2 vacia")   
                else:
                    c2.Frente().gritar()
            
            case "12":
                simulacion(c1, c2, p_buenos, p_regulares, p_descartes)

            case "0":
                print("Saliendo...")
                break

            case _:
                print("Opcion invalida")


menu_interactivo()
