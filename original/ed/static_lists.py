# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 17:15:57 2026

@author: ester
"""
 ## Tema 3 implementacion sobre la memoria estatica  
 
"""
tipo NOdo
  x<-- T
  Y<-- T 
  
tipo Lista
elemntos [Max] <-- Nodo 
size <-- int 

CrearLista 
    funcion CREarlista ()<--  Lista 
    
    lista.elemntos <- [NULL; NULL ::::]
    lista.size = 0 
    return lista 

    funcion agregaAlFinal(lista,e)
         Si lista .size >= MAX
             escribir lista llena 
             retornar
             
             lista.elemtos[lista.size] <-- e 
             lista.sicxe <-- lista .size + 1 
             
        funcion agragar_en_posicion(lista, e,pos)
            si pos < 0 o pos>lista.tamañlo Entonces 
                escribit posicion fuera de rango 
                retornar 
            
            si lista.size >= MAX
                escribir lista llena 
                retornar 
            
            Para i <- lista.size hasta pos+1 decrementrar en 1
                lista.elemntos[i] <- lista.elemntos[i-1]
                lista.elemtos[post]<-- e
                lista.size <-- lista.size+1
                
        funcion eliminarElemnto(lista,pos)
            si pos < 0 o pos>lista.tamañlo Entonces 
                escribit posicion fuera de rango 
                retornar 
            
            para i <--pos hasta lista.size
                lista.elemtos`[i]  <- lista.elemtos[i+1]
                
            lista.size <-- lista.elemetos[i+1]
            lista.size [i+1] = Limpiar 
            
"""

##Cuando te pide con un numero fijo capacidad
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 17:15:57 2026

@author: ester
"""

# Tema 3: implementación sobre memoria estática

class Lista:
    def __init__(self, capacidad=100):
        self.capacidad = capacidad
        self.elementos = [None] * capacidad
        self.size = 0

    def agregar_elemento_ultimo(self, e):
        if self.size >= self.capacidad:
            print("Lista llena")
            return

        self.elementos[self.size] = e
        self.size += 1

    def insertar_elemento(self, e, pos):
        if pos < 0 or pos > self.size:
            print("Posicion incorrecta")
            return

        if self.size >= self.capacidad:
            print("No hay hueco")
            return

        i = self.size
        while i > pos:
            self.elementos[i] = self.elementos[i - 1]
            i -= 1

        self.elementos[pos] = e
        self.size += 1

    def eliminar_elemento(self, pos):
        if pos < 0 or pos >= self.size:
            print("Posicion incorrecta")
            return

        i = pos
        while i < self.size - 1:
            self.elementos[i] = self.elementos[i + 1]
            i += 1

        self.size -= 1
        self.elementos[self.size] = None

    def recorrer_lista(self):
        for i in range(self.size):
            print(self.elementos[i], end=" ")
        print()
        
        




mi_lista = Lista(10)

mi_lista.agregar_elemento_ultimo(5)
mi_lista.agregar_elemento_ultimo(8)
mi_lista.agregar_elemento_ultimo(12)

print("Lista inicial:")
mi_lista.recorrer_lista()

mi_lista.insertar_elemento(99, 1)
print("\nDespues de insertar 99 en la posicion 1:")
mi_lista.recorrer_lista()

mi_lista.eliminar_elemento(2)
print("\nDespues de eliminar el elemento de la posicion 2:")
mi_lista.recorrer_lista()



#%%

"""
lista enlazada vectoriales 

tipo Nodo:
    X <-- T
    Siguiente <-- int 
    
tipo Lista :
    vector[MAX] <-- Nodos
    cabeza <-- int 
    ultimo <-- int
    size <-- int 
    listaHuecos[MAX] <-- [0,1,2,3,4,5,6.....,MAx]
    
Operacion InsertarFinale(L,e)
    hueco <--DevolverHueco() ---> lista Huecos[0] 
    
    
    si hueco = -1 
        retornar 0 
    finsi 
    
L.vector[hueco] <-- e 
L.vector[hueco].siguiente <-- -1


    si l.cabeza == -1
        l.cabeza = hueco
    sino 
        actual <- L.cabeza
        mientras L.vector[actual].siguiente != -1
            actual <-- L.vector[actual].siguiente
            
    L.vector[actual].siguiente <-hueco 
    eliminarHueco()

"""
class NodoVector:
    def __init__(self, dato=None, siguiente=-1):
        self.dato = dato
        self.siguiente = siguiente


class ListaVectorEnlazada:
    def __init__(self, capacidad=100):
        self.vector = [NodoVector() for _ in range(capacidad)]
        self.cabeza = -1
        self.libres = list(range(capacidad))

    def DevueleHueco(self):
        return self.libres[0] if self.libres else -1

    def EliminarHueco(self):
        if self.libres:
            self.libres.pop(0)

    def InsertarFinal(self, e):
        hueco = self.DevueleHueco()

        if hueco == -1:
            return 0

        self.vector[hueco].dato = e
        self.vector[hueco].siguiente = -1

        if self.cabeza == -1:
            self.cabeza = hueco
        else:
            actual = self.cabeza
            while self.vector[actual].siguiente != -1:
                actual = self.vector[actual].siguiente

            self.vector[actual].siguiente = hueco

        self.EliminarHueco()
        return 1

    def Mostrar(self):
        actual = self.cabeza
        while actual != -1:
            print(self.vector[actual].dato, end=" -> ")
            actual = self.vector[actual].siguiente
        print("None")

    def MostrarVector(self):
        for i in range(len(self.vector)):
            print(f"Pos {i}: dato={self.vector[i].dato}, siguiente={self.vector[i].siguiente}")
        
        
        
lista = ListaVectorEnlazada(5)

print(lista.InsertarFinal(10))
print(lista.InsertarFinal(20))
print(lista.InsertarFinal(30))

lista.Mostrar()
lista.MostrarVector()


#%%
##Examen 
