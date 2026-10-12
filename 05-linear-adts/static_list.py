"""Lists over static (fixed-size) memory (ED, topic 3 exercises, 2025/26).

Two implementations written while studying the course pseudocode:

* ``ArrayList``: a contiguous array; inserting or deleting in the middle
  shifts the following elements.
* ``ArrayLinkedList``: a linked list whose nodes live inside a fixed array,
  linked by indices instead of pointers, with a list of free slots. This is
  how linked structures are built when dynamic allocation is not available.
"""
from __future__ import annotations

from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class ArrayList(Generic[T]):
    """Contiguous list with a fixed capacity.

    append is O(1); insert and delete at position ``pos`` are O(n - pos)
    because the tail has to be shifted. Space O(capacity).
    """

    def __init__(self, capacity: int = 100) -> None:
        self.capacity = capacity
        self.elements: list[Optional[T]] = [None] * capacity
        self.size = 0

    def append(self, element: T) -> None:
        """Add ``element`` at the end (prints a warning if the list is full)."""
        if self.size >= self.capacity:
            print("List full")
            return
        self.elements[self.size] = element
        self.size += 1

    def insert(self, element: T, pos: int) -> None:
        """Insert ``element`` at index ``pos`` (0 <= pos <= size)."""
        if pos < 0 or pos > self.size:
            print("Invalid position")
            return
        if self.size >= self.capacity:
            print("No free space")
            return

        i = self.size
        while i > pos:  # shift the tail one slot to the right
            self.elements[i] = self.elements[i - 1]
            i -= 1

        self.elements[pos] = element
        self.size += 1

    def delete(self, pos: int) -> None:
        """Delete the element at index ``pos`` (0 <= pos < size)."""
        if pos < 0 or pos >= self.size:
            print("Invalid position")
            return

        i = pos
        while i < self.size - 1:  # shift the tail one slot to the left
            self.elements[i] = self.elements[i + 1]
            i += 1

        self.size -= 1
        self.elements[self.size] = None

    def to_list(self) -> list[T]:
        return [e for e in self.elements[: self.size]]  # type: ignore[misc]


class ArrayNode(Generic[T]):
    """A slot of ``ArrayLinkedList``: a value and the index of the next slot."""

    def __init__(self, value: Optional[T] = None, next_index: int = -1) -> None:
        self.value = value
        self.next_index = next_index


class ArrayLinkedList(Generic[T]):
    """Linked list stored in a fixed array; -1 plays the role of ``None``.

    ``free`` holds the indices of unused slots. insert_last walks from the
    head to the last node, so it is O(n); taking a free slot from the front
    of a Python list is also O(capacity) (``list.pop(0)``), as in the
    original code.
    """

    def __init__(self, capacity: int = 100) -> None:
        self.slots: list[ArrayNode[T]] = [ArrayNode() for _ in range(capacity)]
        self.head = -1
        self.free = list(range(capacity))

    def _first_free(self) -> int:
        return self.free[0] if self.free else -1

    def _take_free(self) -> None:
        if self.free:
            self.free.pop(0)

    def insert_last(self, value: T) -> bool:
        """Append ``value``; return False if there is no free slot."""
        slot = self._first_free()
        if slot == -1:
            return False

        self.slots[slot].value = value
        self.slots[slot].next_index = -1

        if self.head == -1:
            self.head = slot
        else:
            current = self.head
            while self.slots[current].next_index != -1:
                current = self.slots[current].next_index
            self.slots[current].next_index = slot

        self._take_free()
        return True

    def to_list(self) -> list[T]:
        values, current = [], self.head
        while current != -1:
            values.append(self.slots[current].value)
            current = self.slots[current].next_index
        return values  # type: ignore[return-value]


if __name__ == "__main__":
    lst: ArrayList[int] = ArrayList(10)
    for x in (5, 8, 12):
        lst.append(x)
    lst.insert(99, 1)
    lst.delete(2)
    print("ArrayList:", lst.to_list())  # [5, 99, 12]

    linked: ArrayLinkedList[int] = ArrayLinkedList(5)
    for x in (10, 20, 30):
        linked.insert_last(x)
    print("ArrayLinkedList:", linked.to_list())
