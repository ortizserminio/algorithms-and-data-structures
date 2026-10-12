# 05 · Linear ADTs: stacks, queues and lists

Language: **Python 3.10+**. Source: *Estructuras de Datos*, practical 1 (2024/25 and 2025/26) and topic 3 exercises.

| File | Structure | Course scenario |
|---|---|---|
| [`array_stack.py`](array_stack.py) | Fixed-capacity stack over an array | A library sorting returned books into one stack per genre |
| [`linked_queue.py`](linked_queue.py) | Linked queue and linked stack | Captured humans queued for abduction, then classified into stacks |
| [`static_list.py`](static_list.py) | Contiguous list, and a linked list stored inside an array | Topic 3: lists over static memory |

The original practicals wrapped these structures in interactive menus and timed simulations. Those are kept in the [first commit](https://github.com/ortizserminio/algorithms-and-data-structures/commit/26c3ed7) of this repository; this folder contains the data structures themselves.

## Array stack

A pre-allocated array plus `top_index`, the number of elements stored. `push` writes at `top_index` and increments it, while `pop` decrements it and reads. Pushing onto a full stack prints a warning and does nothing. Popping or peeking an empty stack returns `None`.

**Complexity:** every operation is **O(1)**; space is **O(capacity)** from the start.
**Why an array?** There is no per-node overhead and access is cache-friendly. The cost is a fixed maximum size. A linked stack (below) grows without limit but allocates one node per element.

## Linked queue

A singly linked list with pointers to **both** ends: `enqueue` appends after `last`, and `dequeue` removes `first`. Keeping `last` is what makes `enqueue` O(1); with only a head pointer it would be O(n).

| Operation | Time | Note |
|---|---|---|
| `enqueue`, `dequeue`, `front`, `is_empty` | O(1) | |
| `concatenate(other)` | O(1) | Links `last.next` to `other.first`; `other` is left empty |
| `remove(value)` | O(n) | Drains into an auxiliary queue skipping the first match, then refills |
| `size` | O(n) | The original design keeps no counter; adding one would make it O(1) |

### Formal specification written for the practical (excerpt)

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
SEMANTICA  (for all h, h1 in H and c1, c2 in C)
  ConsultarVacia(CrearCola()) = true
  ConsultarVacia(Encolar(c1, h)) = false
  Frente(Encolar(c1, h)) = si ConsultarVacia(c1) -> h | Frente(c1)
  Frente(Concatenar(c1, c2)) = si ConsultarVacia(c1) -> Frente(c2) | Frente(c1)
  EliminarH(h1, Encolar(c1, h)) = si h1 == h -> [c1, true] | [Encolar(c1, h), false]
```

## Static lists

* **`ArrayList`**: `insert(e, pos)` shifts `elements[pos..size−1]` one slot to the right, and `delete(pos)` shifts left. Time is **O(n − pos)**; `append` is O(1).
* **`ArrayLinkedList`**: nodes live in a fixed array and link to each other by **index**, with `−1` playing the role of `None`. A `free` list records unused slots. This is how linked structures are built where dynamic allocation is unavailable (embedded systems, or file formats that store records by offset). `insert_last` walks to the tail, so it is **O(n)**. Taking a slot with `list.pop(0)` also costs O(capacity), as in the original. A `last` index and a stack of free slots would make both O(1).

## Run and test

```bash
pip install -r requirements-dev.txt
python -m pytest 05-linear-adts
python 05-linear-adts/linked_queue.py    # each module has a small demo
```

There are 23 tests: LIFO/FIFO order, empty and full structures, capacity 0, concatenating empty queues, `last` updated correctly after `remove`, insertion at both ends, and invalid positions.
