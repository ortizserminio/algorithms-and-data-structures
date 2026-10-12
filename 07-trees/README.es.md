# 07 · Árboles: árbol binario de búsqueda y árbol AVL

[English](README.md) · **Español**

Lenguaje: **Python 3.10+**. Origen: *Estructuras de Datos*, práctica 2 (2024/25: ABB; 2025/26: AVL).

## Árbol binario de búsqueda: [`bst.py`](bst.py)

**Caso de uso en la práctica:** una biblioteca mantiene un ABB de libros por género, con un identificador de 6 cifras como clave.

**Invariante:** todas las claves del subárbol izquierdo de un nodo son menores que la suya, y todas las del subárbol derecho, mayores.

* **Insertar / buscar:** se compara con el nodo actual y se baja por la izquierda o por la derecha.
* **Borrar** tiene tres casos:
  1. Hoja: se elimina.
  2. Un hijo: el nodo se sustituye por ese hijo.
  3. Dos hijos: se copia en el nodo el **sucesor en inorden** (el mínimo del subárbol derecho) y después se borra el sucesor del subárbol derecho. El sucesor no tiene hijo izquierdo, así que se le aplica el caso 1 o el 2.
* **Recorridos:** inorden (devuelve las claves ordenadas), preorden y postorden.

**Complejidad.** Insertar, buscar y borrar son **O(h)**, donde `h` es la altura. Eso es O(log n) si el árbol está equilibrado, pero **O(n)** si las claves llegan ordenadas: el árbol degenera en una lista enlazada, y hay un test que lo demuestra. Los recorridos son O(n).

## Árbol AVL: [`avl.py`](avl.py)

Un árbol AVL corrige el peor caso del ABB. Cada nodo guarda su altura, y después de cada inserción o borrado los nodos del camino de vuelta a la raíz comprueban su **factor de equilibrio** `altura(derecho) − altura(izquierdo)`. Si se sale de `[−1, 1]`, una de cuatro rotaciones lo restablece:

| Caso | Forma | Solución |
|---|---|---|
| RR | el hijo derecho está cargado a la derecha (o equilibrado) | rotación simple a la izquierda |
| LL | el hijo izquierdo está cargado a la izquierda (o equilibrado) | rotación simple a la derecha |
| RL | el hijo derecho está cargado a la izquierda | se rota el hijo a la derecha y luego el nodo a la izquierda |
| LR | el hijo izquierdo está cargado a la derecha | se rota el hijo a la izquierda y luego el nodo a la derecha |

Una rotación solo vuelve a enlazar tres punteros y actualiza dos alturas, así que es O(1).

**Complejidad.** La altura de un árbol AVL es como mucho de unos 1,44·log₂(n+2). Por tanto, insertar, buscar y borrar son **O(log n) en el peor caso**, con O(log n) de pila de recursividad. Un test inserta 1 000 claves *ordenadas* y comprueba que la altura se queda en ≤ 15. Un ABB normal llegaría a altura 1 000.

**¿Por qué AVL y no otro árbol equilibrado?** Los AVL están más estrictamente equilibrados que los árboles rojinegros, así que las búsquedas son algo más rápidas. A cambio, las modificaciones hacen más rotaciones. Los rojinegros (los que usan `std::map` y `TreeMap` de Java) se prefieren cuando hay muchas escrituras, y los árboles B para datos en disco. Para una estructura en memoria que se lee más de lo que se escribe, AVL es una buena opción, y es la que se estudia en la asignatura.

## Correcciones sobre las prácticas originales

El código se portó primero tal cual y después se corrigió en commits separados, cada uno con tests de regresión:

* **ABB:** borrar un nodo con dos hijos usaba `actual.id`, pero los libros guardaban su clave en `id_libro`, así que lanzaba `AttributeError`. Incluso con el atributo correcto solo se habría copiado la clave, dejando los datos equivocados. Ahora se copian la clave y el valor.
* **AVL:** el método auxiliar de borrado se definía como `elimnar_recursivo` pero se llamaba como `eliminar_recursivo`, así que todo borrado fallaba. Además devolvía solo el nodo cuando quien llamaba esperaba `(nodo, borrado)`. Insertar una clave repetida devolvía un *texto*, que luego se guardaba como hijo.

## Ejecutar y probar

```bash
python -m pytest 07-trees
python 07-trees/avl.py
python 07-trees/bst.py
```

Hay 19 tests: orden de los recorridos, los cuatro casos de rotación, un comprobador de invariantes (orden de ABB, alturas guardadas, |equilibrio| ≤ 1) que se ejecuta después de cada inserción y cada borrado con datos aleatorios, borrado de la raíz, de hojas y de claves inexistentes, y duplicados.
