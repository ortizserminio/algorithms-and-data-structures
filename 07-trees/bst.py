"""Binary search tree (ED practical 2, 2024/25).

In the practical a library kept one BST of books per genre, keyed by a
6-digit book id. Here nodes carry a generic ``key`` and ``value``; the
recursive algorithms are the original ones. Traversals now return lists
instead of printing, so they can be tested.

Complexities, with h = height of the tree (h = O(log n) if the tree is
balanced, but O(n) in the worst case, e.g. keys inserted in sorted order,
because this tree does not rebalance - see avl.py):
insert, search, delete: O(h) time, O(h) recursion stack.
Traversals: O(n) time.
"""
from __future__ import annotations

from typing import Any, Optional


class BSTNode:
    def __init__(self, key: int, value: Any = None) -> None:
        self.key = key
        self.value = value
        self.left: Optional[BSTNode] = None
        self.right: Optional[BSTNode] = None


class BST:
    """Unbalanced binary search tree; duplicate keys are ignored."""

    def __init__(self) -> None:
        self.root: Optional[BSTNode] = None

    # ------------------------------------------------------------ insertion
    def insert(self, key: int, value: Any = None) -> None:
        self.root = self._insert(self.root, BSTNode(key, value))

    def _insert(self, current: Optional[BSTNode], node: BSTNode) -> BSTNode:
        if current is None:
            return node
        if node.key > current.key:
            current.right = self._insert(current.right, node)
        elif node.key < current.key:
            current.left = self._insert(current.left, node)
        return current

    # --------------------------------------------------------------- search
    def search(self, key: int) -> Optional[BSTNode]:
        """Return the node with ``key``, or None."""
        return self._search(self.root, key)

    def _search(self, current: Optional[BSTNode], key: int) -> Optional[BSTNode]:
        if current is None:
            return None
        if current.key == key:
            return current
        if key < current.key:
            return self._search(current.left, key)
        return self._search(current.right, key)

    # ------------------------------------------------------------- deletion
    def delete(self, key: int) -> None:
        self.root = self._delete(self.root, key)

    def _delete(self, current: Optional[BSTNode], key: int) -> Optional[BSTNode]:
        if current is None:
            return None
        if key < current.key:
            current.left = self._delete(current.left, key)
        elif key > current.key:
            current.right = self._delete(current.right, key)
        else:
            # Zero or one child: replace the node by its only child.
            if current.left is None:
                return current.right
            if current.right is None:
                return current.left
            # Two children: copy the in-order successor (minimum of the
            # right subtree) here, then delete it from the right subtree.
            successor = self._min_node(current.right)
            current.key, current.value = successor.key, successor.value
            current.right = self._delete(current.right, successor.key)
        return current

    @staticmethod
    def _min_node(current: BSTNode) -> BSTNode:
        while current.left is not None:
            current = current.left
        return current

    # ----------------------------------------------------------- traversals
    def inorder(self) -> list[int]:
        """Keys in left-root-right order (ascending for a BST)."""
        keys: list[int] = []
        self._inorder(self.root, keys)
        return keys

    def _inorder(self, node: Optional[BSTNode], keys: list[int]) -> None:
        if node:
            self._inorder(node.left, keys)
            keys.append(node.key)
            self._inorder(node.right, keys)

    def preorder(self) -> list[int]:
        """Keys in root-left-right order."""
        keys: list[int] = []
        self._preorder(self.root, keys)
        return keys

    def _preorder(self, node: Optional[BSTNode], keys: list[int]) -> None:
        if node:
            keys.append(node.key)
            self._preorder(node.left, keys)
            self._preorder(node.right, keys)

    def postorder(self) -> list[int]:
        """Keys in left-right-root order."""
        keys: list[int] = []
        self._postorder(self.root, keys)
        return keys

    def _postorder(self, node: Optional[BSTNode], keys: list[int]) -> None:
        if node:
            self._postorder(node.left, keys)
            self._postorder(node.right, keys)
            keys.append(node.key)


if __name__ == "__main__":
    tree = BST()
    for book_id in (500000, 300000, 700000, 200000, 400000, 800000):
        tree.insert(book_id, f"Book {book_id}")
    print("In-order:  ", tree.inorder())
    print("Pre-order: ", tree.preorder())
    print("Post-order:", tree.postorder())
    tree.delete(200000)
    print("After deleting a leaf:", tree.inorder())
