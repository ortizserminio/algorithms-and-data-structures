from abc import ABC, abstractmethod
import random

class IArbol(ABC):
    @abstractmethod
    def esVacio(self):
        pass

    @abstractmethod
    def insertar(self, nodo_insertar):
        pass

    @abstractmethod
    def buscarHumano(self, valor):
        pass

    @abstractmethod
    def eliminar(self, valor):
        pass

    @abstractmethod
    def verRaiz(self):
        pass

    @abstractmethod
    def tam(self):
        pass

    @abstractmethod
    def preorden(self):
        pass

    @abstractmethod
    def inorden(self):
        pass

    @abstractmethod
    def postorden(self):
        pass

class IHumano(ABC):
    @abstractmethod
    def gritar(self):
        pass

class Nodo:
    def __init__(self, humano):
        self.izquierda = None
        self.derecha = None
        self.humano = humano
        self.altura = 1

class Humano(IHumano):
    def __init__(self, id):
        self.id = id
        #self.id = random.randint(10000000, 99999999) # Commenteado para testear, da todo el rato lo mismo en una misma run
        self.nombre = "Antonio"

    def gritar(self):
        pass

class Arbol(IArbol):
    def __init__(self):
        self.raiz = None

    def esVacio(self):
        return self.raiz is None
    
    def insertar(self, nodo_insertar):
        self.raiz = self.insertar_recursivo(nodo_insertar, self.raiz)   

    def buscarHumano(self, valor):
        return self.buscar_recursivo(valor, self.raiz)

    def eliminar(self, valor):
        self.raiz, eliminado = self.eliminar_recursivo(valor, self.raiz)
        return eliminado
    
    def verRaiz(self):
        if self.raiz is None:
            return "No hay raiz"
        else:
            return self.raiz

    def tam(self):
        return self.tam_recursivo(self.raiz)

    def inorden(self):
        return self.inorden_recursivo(self.raiz)

    def preorden(self):
        return self.preorden_recursivo(self.raiz)
    
    def postorden(self):
        return self.postorden_recursivo(self.raiz)

#   Helper para programar 
    def insertar_recursivo(self, nodo_insertar, nodo_actual):
        if nodo_actual is None:
            return nodo_insertar
        else:
            if (nodo_insertar.humano.id>nodo_actual.humano.id):
                nodo_actual.derecha = self.insertar_recursivo(nodo_insertar, nodo_actual.derecha)

            elif(nodo_insertar.humano.id < nodo_actual.humano.id):
                    nodo_actual.izquierda = self.insertar_recursivo(nodo_insertar, nodo_actual.izquierda)
            else:
                return "El nodo ya esta insertado"

        self.actualizar_altura(nodo_actual)
        factor = self.calcular_factor_equilibrio(nodo_actual)
        return self.balanceo(factor, nodo_actual)

    def buscar_recursivo(self, valor, nodo_actual):
        if nodo_actual is None:
            return False
        else:
            if nodo_actual.humano.id == valor:
                return True
            else: 
                if valor < nodo_actual.humano.id:
                    return self.buscar_recursivo(valor, nodo_actual.izquierda)
                else:
                    return self.buscar_recursivo(valor, nodo_actual.derecha)

    def elimnar_recursivo(self, valor, nodo_actual):
        #Caso base si el nodo es nulo 
        if nodo_actual is None:
            return None, False
        #Buscar por ID
        if valor > nodo_actual.humano.id:
            nodo_actual.derecha, eliminar  = self.eliminar_recursivo(valor, nodo_actual.derecha)
        elif valor < nodo_actual.humano.id:
            nodo_actual.izquierda, eliminar = self.eliminar_recursivo(valor, nodo_actual.izquierda)

        #Ahora que ya lo hemos encontrado tres casos de eliminacion
        else:
            
            if nodo_actual.izquierda is None and nodo_actual.derecha is None:
                return None, True

            elif nodo_actual.izquierda is None:
                return nodo_actual.derecha,True

            elif nodo_actual.derecha is None:
                return nodo_actual.izquierda, True

            else:
                #Busca el minimo de todo el arobol de la derecha en inorden
                aux = self.minimo_inorden(nodo_actual.derecha)
                # copiamos el minimo en la raiz o el nodo actual
                nodo_actual.humano = aux.humano
                #llamamos a eliminar recursivo para el 25 del subarbol de la derecha 
                nodo_actual.derecha, eliminar = self.eliminar_recursivo(aux.humano.id, nodo_actual.derecha)

        self.actualizar_altura(nodo_actual)
        factor = self.calcular_factor_equilibrio(nodo_actual)
        return self.balanceo(factor, nodo_actual)
        
    def minimo_inorden(self, nodo_actual):
        while nodo_actual.izquierda is not None:
            nodo_actual = nodo_actual.izquierda
        return nodo_actual

    def tam_recursivo(self,nodo):
        if nodo is None:
            return 0
        else:
            return 1 + self.tam_recursivo(nodo.izquierda) + self.tam_recursivo(nodo.derecha)

    def inorden_recursivo(self, nodo):
        if nodo is None:
            return 
        else:
            self.inorden_recursivo(nodo.izquierda)
            print(nodo.humano.id, end=",")
            self.inorden_recursivo(nodo.derecha)

    def preorden_recursivo(self, nodo):
        if nodo is None:
            return 
        else:
            print(nodo.humano.id, end=",")
            self.preorden_recursivo(nodo.izquierda)
            self.preorden_recursivo(nodo.derecha)

    def postorden_recursivo(self, nodo):
        if nodo is None:
            return 
        else:
            self.postorden_recursivo(nodo.izquierda)
            self.postorden_recursivo(nodo.derecha)
            print(nodo.humano.id, end=",")

    def altura(self, nodo):
        if nodo is None:
            return 0
        return nodo.altura


    def actualizar_altura(self, nodo):
        # Importante, puede ser que se le pase un None al max, si ponemos esto: "max(nodo.derecha.altura, nodo.izquierda.altura)"
        # Para eso tenemos la funcion altura, que tambien se podria hacer con 2 checks de si son Nones
        # IMPORTANTE PARA EL EXAMEN BTW
        if nodo is not None:
            nodo.altura = 1 + max(self.altura(nodo.izquierda), self.altura(nodo.derecha))

    def calcular_factor_equilibrio(self, nodo):
        if nodo is None:
            return 0
        return self.altura(nodo.derecha) - self.altura(nodo.izquierda)
        
    def rotacion_derecha(self, P):
        Q = P.izquierda        # guardamos el hijo izquierdo de P
        temporal = Q.derecha   # guardamos el hijo derecho de Q (para no perderlo)

        Q.derecha = P          # Q sube: P pasa a ser hijo derecho de Q
        P.izquierda = temporal # P baja: el antiguo hijo derecho de Q pasa a ser hijo izquierdo de P

        self.actualizar_altura(P)  # P ha cambiado de posición, actualizamos su altura
        self.actualizar_altura(Q)  # Q también ha cambiado, actualizamos su altura

        return Q               # Q es ahora la nueva raíz de este subárbol

    def rotacion_izquierda(self, P):
        Q = P.derecha
        temporal = Q.izquierda

        Q.izquierda = P 
        P.derecha = temporal

        self.actualizar_altura(P)  
        self.actualizar_altura(Q)

        return Q

    def balanceo(self, factor, P):
        if factor > 1:
            Q = P.derecha
            if self.calcular_factor_equilibrio(Q) >= 0:
                return self.rotacion_izquierda(P)  # rotación simple
            else:
                P.derecha = self.rotacion_derecha(Q)  # primero rotamos Q
                return self.rotacion_izquierda(P)     # luego rotamos P
        elif factor < -1:
            Q = P.izquierda
            if self.calcular_factor_equilibrio(Q) <= 0:
                return self.rotacion_derecha(P)
            else:
                P.izquierda = self.rotacion_izquierda(Q) 
                return self.rotacion_derecha(P)

        return P 


ar = Arbol()
ar.insertar(Nodo(Humano(10)))
ar.insertar(Nodo(Humano(20)))
ar.insertar(Nodo(Humano(30)))

 
print(f"Raiz: {ar.verRaiz().humano.id}")  # debe ser 20 por el balanceo AVL
print(f"Tam: {ar.tam()}")                 # debe ser 3
print("Inorden: ")
ar.inorden()   
print("\nPostorden: ")                           
ar.postorden()
print("\nPreorden: ")                           
ar.preorden()