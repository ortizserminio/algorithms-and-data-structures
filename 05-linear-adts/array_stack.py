"""Fixed-capacity stack backed by a Python list (ED practical 1, 2024/25).

The original practical used this stack to simulate a library: returned
books were pushed onto a "returned" stack and later moved to one stack per
genre. That simulation is kept in the repository history (first commit);
this module contains the data structure itself, with the same logic.
"""
from __future__ import annotations

from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class ArrayStack(Generic[T]):
    """LIFO stack stored in a pre-allocated array of ``capacity`` slots.

    ``top_index`` is the number of stored elements, so the top element lives
    at ``elements[top_index - 1]``. Every operation is O(1) time; the stack
    uses O(capacity) space from the start.
    """

    def __init__(self, capacity: int = 100) -> None:
        self.capacity = capacity
        self.elements: list[Optional[T]] = [None] * capacity
        self.top_index = 0

    def is_empty(self) -> bool:
        """Return True if the stack has no elements."""
        return self.top_index == 0

    def push(self, element: T) -> None:
        """Push ``element``; if the stack is full, print a warning and ignore it."""
        if self.top_index >= self.capacity:
            print("The stack is full.")
        else:
            self.elements[self.top_index] = element
            self.top_index += 1

    def pop(self) -> Optional[T]:
        """Remove and return the top element, or None if the stack is empty."""
        if self.is_empty():
            print("The stack is empty. Nothing to pop.")
            return None
        self.top_index -= 1
        return self.elements[self.top_index]

    def peek(self) -> Optional[T]:
        """Return the top element without removing it, or None if empty."""
        if self.is_empty():
            print("The stack is empty.")
            return None
        return self.elements[self.top_index - 1]

    def __len__(self) -> int:
        return self.top_index

    def __str__(self) -> str:
        """Elements from bottom to top, comma separated."""
        if self.is_empty():
            return "The stack is empty."
        return ", ".join(str(e) for e in self.elements[: self.top_index])


if __name__ == "__main__":
    stack: ArrayStack[int] = ArrayStack(capacity=3)
    for isbn in (111111, 222222, 333333, 444444):  # the 4th push overflows
        stack.push(isbn)
    print("Stack:", stack)
    print("Top:", stack.peek())
    print("Popped:", stack.pop(), stack.pop())
    print("Stack:", stack)
