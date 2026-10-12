# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 17:20:18 2026

@author: ester
"""

class Conjunto :
    def __init__(self,bits=8,valor=0):
        self.max_elementos = bits
        self.bits = valor & ((1<<bits)-1) ##desplazar el uno 8 bits a la derecha
        
        def union(self,c2):
            result = 0
            ## El desplazamiento simpre es el mismo
            for i in range(self.max_elemetos):
                a = (self.bits >> i) & 1
                b = (c2.bits >> i) & 1
                ## Lo que cambia son las operaciones
                result += (1 << i) * max(a,b)
                
            return Conjunto(self.max_elementos,result)
        
        def interseccion(self,c2):
            result = 0
            ## El desplazamiento simpre es el mismo
            for i in range(self.max_elemetos):
                a = (self.bits >> i) & 1
                b = (c2.bits >> i) & 1
                ## Lo que cambia son las operaciones en este caso a*b es 1 uno 
                result += (1 << i) * (a*b)
            
            return Conjunto(self.max_elementos, result)
                
        def diferencia(self,c2):
            result = 0
            ## El desplazamiento simpre es el mismo
            for i in range(self.max_elemetos):
                a = (self.bits >> i) & 1
                b = (c2.bits >> i) & 1
                ## Lo que cambia son las operaciones en este caso 
                ## 
                if a and not b:
                    result += (1 << i)
            
            return Conjunto(self.max_elementos, result)
        
        def diferencia_simetrica(self,c2):
            result = 0
            ## El desplazamiento simpre es el mismo
            for i in range(self.max_elemetos):
                a = (self.bits >> i) & 1
                b = (c2.bits >> i) & 1
                ## Lo que cambia son las operaciones en este caso 
                ## 
                if a and not b:
                    result += (1 << i)
                elif b and not a:
                    result += (1 << i)
            
            return Conjunto(self.max_elementos, result)
        
        def pertenecia(self,num):
            if 0 <= num <= self.max_elementos:
                A_desplazado = self.bits >> num
                return A_desplazado % 2 == 1 
            return False 
        
        def __repr__(self):
            return f"{self.bits:0{self.max_elementos}b}"
        
        def sacar_elementos(self):
            elementos = [i for i in range(self.max_elementos) if (self.bits >> i) & 1 ]
            return elementos
                
        def add(self,num):
            if 0 <= num <= self.max_elementos:
                self.bits += (1 << num) * (1 - ((self.bits >> num) & 1 ))
                
        def borrar(self, num):
            if 0 <= num < self.max_elementos:
                self.bits -= (1 << num) * ((self.bits >> num) & 1)
        
        
        
A = Conjunto(8,511)
B = Conjunto(8,16)

print(A.bits)
print(B.bits)