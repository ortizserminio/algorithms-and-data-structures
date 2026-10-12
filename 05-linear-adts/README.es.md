# 05 · TADs lineales: pilas, colas y listas

[English](README.md) · **Español**

Lenguaje: **Python 3.10+**. Origen: *Estructuras de Datos*, práctica 1 (2024/25 y 2025/26) y ejercicios del tema 3.

| Archivo | Estructura | Escenario de la asignatura |
|---|---|---|
| [`array_stack.py`](array_stack.py) | Pila de capacidad fija sobre un array | Una biblioteca que clasifica los libros devueltos en una pila por género |
| [`linked_queue.py`](linked_queue.py) | Cola enlazada y pila enlazada | Humanos capturados en cola para ser abducidos y luego clasificados en pilas |
| [`static_list.py`](static_list.py) | Lista contigua, y una lista enlazada guardada dentro de un array | Tema 3: listas en memoria estática |

Las prácticas originales envolvían estas estructuras en menús interactivos y simulaciones con tiempo. Esas partes están en el [primer commit](https://github.com/ortizserminio/algorithms-and-data-structures/commit/26c3ed7) del repositorio; esta carpeta contiene las estructuras de datos en sí.

## Pila sobre array

Un array reservado de antemano más `top_index`, el número de elementos guardados. `push` escribe en `top_index` y lo incrementa; `pop` lo decrementa y lee. Apilar en una pila llena muestra un aviso y no hace nada. Desapilar o consultar la cima de una pila vacía devuelve `None`.

**Complejidad:** todas las operaciones son **O(1)**; el espacio es **O(capacidad)** desde el principio.
**¿Por qué un array?** No hay coste extra por nodo y el acceso aprovecha bien la caché. El precio es un tamaño máximo fijo. La pila enlazada (más abajo) crece sin límite, pero reserva un nodo por elemento.

## Cola enlazada

Una lista simplemente enlazada con punteros a **los dos** extremos: `enqueue` añade detrás de `last` y `dequeue` quita `first`. Guardar `last` es lo que hace que `enqueue` sea O(1); con solo un puntero a la cabeza sería O(n).

| Operación | Tiempo | Nota |
|---|---|---|
| `enqueue`, `dequeue`, `front`, `is_empty` | O(1) | |
| `concatenate(other)` | O(1) | Enlaza `last.next` con `other.first`; `other` queda vacía |
| `remove(value)` | O(n) | Vacía la cola en una auxiliar saltándose la primera coincidencia, y la vuelve a llenar |
| `size` | O(n) | El diseño original no guarda un contador; con uno sería O(1) |

### Especificación formal escrita para la práctica (extracto)

```
TAD ColaAbduccion
SINTAXIS
  CrearCola                    -> C
  ConsultarVacia   C           -> B
  Encolar          H x C       -> C
  Desencolar       C           -> (C x H) U M
  Frente           C           -> H U M
  Concatenar       C x C       -> C
  EliminarH        C x H       -> (C x B) U M
SEMANTICA  (para todo h, h1 en H y c1, c2 en C)
  ConsultarVacia(CrearCola()) = true
  ConsultarVacia(Encolar(c1, h)) = false
  Frente(Encolar(c1, h)) = si ConsultarVacia(c1) -> h | Frente(c1)
  Frente(Concatenar(c1, c2)) = si ConsultarVacia(c1) -> Frente(c2) | Frente(c1)
  EliminarH(h1, Encolar(c1, h)) = si h1 == h -> [c1, true] | [Encolar(c1, h), false]
```

## Listas estáticas

* **`ArrayList`**: `insert(e, pos)` desplaza `elements[pos..size−1]` una posición a la derecha y `delete(pos)` desplaza a la izquierda. El tiempo es **O(n − pos)**; `append` es O(1).
* **`ArrayLinkedList`**: los nodos viven en un array fijo y se enlazan por **índice**, con `−1` en el papel de `None`. Una lista `free` guarda las posiciones sin usar. Así se construyen las estructuras enlazadas cuando no hay memoria dinámica (sistemas embebidos, o formatos de fichero que guardan registros por posición). `insert_last` recorre la lista hasta el final, así que es **O(n)**. Tomar un hueco con `list.pop(0)` también cuesta O(capacidad), como en el original. Con un índice `last` y una pila de huecos libres, las dos cosas serían O(1).

## Ejecutar y probar

```bash
pip install -r requirements-dev.txt
python -m pytest 05-linear-adts
python 05-linear-adts/linked_queue.py    # cada módulo tiene una pequeña demo
```

Hay 23 tests: orden LIFO/FIFO, estructuras vacías y llenas, capacidad 0, concatenar colas vacías, que `last` quede bien después de `remove`, inserción en ambos extremos y posiciones no válidas.
