"""Linked queue and linked stack (ED practical 1, 2025/26).

In the original practical the queue held "captured humans" waiting to be
abducted by a spaceship, and abducted humans were classified into three
stacks. The nodes were the ``Humano`` objects themselves (each had a
``siguiente`` pointer). Here the same algorithms work on generic values
wrapped in a small ``Node`` class. The formal specification of the queue
ADT written for the practical is reproduced in this folder's README.
"""
from __future__ import annotations

from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class Node(Generic[T]):
    """Singly linked node."""

    def __init__(self, value: T) -> None:
        self.value = value
        self.next: Optional[Node[T]] = None


class LinkedQueue(Generic[T]):
    """FIFO queue with pointers to the first and last node.

    enqueue, dequeue, front and is_empty are O(1); size is O(n) because the
    original design does not store a counter; concatenate is O(1) because it
    links the two lists; remove is O(n).
    """

    def __init__(self) -> None:
        self.first: Optional[Node[T]] = None
        self.last: Optional[Node[T]] = None

    def is_empty(self) -> bool:
        return self.first is None

    def enqueue(self, value: T) -> None:
        """Add ``value`` at the back of the queue."""
        node = Node(value)
        if self.is_empty():
            self.first = node
            self.last = node
        else:
            assert self.last is not None
            self.last.next = node
            self.last = node

    def dequeue(self) -> Optional[T]:
        """Remove and return the front value, or None if the queue is empty."""
        if self.first is None:
            print("The queue is empty")
            return None
        leaving = self.first
        self.first = leaving.next
        if self.first is None:
            self.last = None
        leaving.next = None
        return leaving.value

    def front(self) -> Optional[T]:
        """Return the front value without removing it (None if empty)."""
        return None if self.first is None else self.first.value

    def size(self) -> int:
        """Count the nodes by walking the list: O(n)."""
        count, current = 0, self.first
        while current is not None:
            count += 1
            current = current.next
        return count

    def concatenate(self, other: LinkedQueue[T]) -> None:
        """Append all of ``other`` to the back of this queue in O(1).

        ``other`` is left empty, since its nodes now belong to this queue.
        """
        if other.is_empty():
            return
        if self.is_empty():
            self.first = other.first
            self.last = other.last
        else:
            assert self.last is not None
            self.last.next = other.first
            self.last = other.last
        other.first = None
        other.last = None

    def remove(self, value: T) -> bool:
        """Remove the first occurrence of ``value`` and keep the order of the rest.

        As in the original, the queue is emptied into an auxiliary queue,
        skipping the first match, and then refilled. Returns True if a value
        was removed. O(n) time, O(n) auxiliary space.
        """
        if self.is_empty():
            print("The queue is empty")
            return False

        aux: LinkedQueue[T] = LinkedQueue()
        found = False
        while not self.is_empty():
            current = self.dequeue()
            if current == value and not found:
                found = True
            else:
                aux.enqueue(current)  # type: ignore[arg-type]

        while not aux.is_empty():
            self.enqueue(aux.dequeue())  # type: ignore[arg-type]
        return found

    def to_list(self) -> list[T]:
        """Values from front to back."""
        values, current = [], self.first
        while current is not None:
            values.append(current.value)
            current = current.next
        return values

    def __str__(self) -> str:
        return " -> ".join(str(v) for v in self.to_list()) or "(empty)"


class LinkedStack(Generic[T]):
    """LIFO stack as a singly linked list; push and pop are O(1)."""

    def __init__(self) -> None:
        self.head: Optional[Node[T]] = None

    def is_empty(self) -> bool:
        return self.head is None

    def push(self, value: T) -> None:
        node = Node(value)
        node.next = self.head
        self.head = node

    def pop(self) -> Optional[T]:
        """Remove and return the top value, or None if the stack is empty."""
        if self.head is None:
            return None
        popped = self.head
        self.head = popped.next
        popped.next = None
        return popped.value

    def to_list(self) -> list[T]:
        """Values from top to bottom."""
        values, current = [], self.head
        while current is not None:
            values.append(current.value)
            current = current.next
        return values


if __name__ == "__main__":
    c1: LinkedQueue[str] = LinkedQueue()
    c2: LinkedQueue[str] = LinkedQueue()
    for name in ("h1", "h2", "h3"):
        c1.enqueue(name)
    c2.enqueue("h4")
    c1.concatenate(c2)
    print("C1:", c1, "| C2:", c2)
    c1.remove("h2")
    print("After removing h2:", c1, "| size:", c1.size())
    stack: LinkedStack[str] = LinkedStack()
    while not c1.is_empty():
        stack.push(c1.dequeue())  # type: ignore[arg-type]
    print("Stack (top first):", stack.to_list())
