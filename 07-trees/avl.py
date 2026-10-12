"""AVL tree: a self-balancing binary search tree (ED practical 2, 2025/26).

Every node stores its height. After each insertion or deletion the balance
factor ``height(right) - height(left)`` of the nodes on the path back to the
root is recomputed and, when it leaves [-1, 1], one or two rotations restore
it. This keeps the height at O(log n), so insert, search and delete are
O(log n) in the worst case (a plain BST degrades to O(n)).

In the practical the keys were the ids of "humans"; here nodes carry a
generic ``key`` and ``value``. Traversals now return lists instead of
printing, so they can be tested.
"""
from __future__ import annotations

from typing import Any, Optional


class AVLNode:
    def __init__(self, key: int, value: Any = None) -> None:
        self.key = key
        self.value = value
        self.left: Optional[AVLNode] = None
        self.right: Optional[AVLNode] = None
        self.height = 1


class AVLTree:
    def __init__(self) -> None:
        self.root: Optional[AVLNode] = None

    # ------------------------------------------------------------ public API
    def is_empty(self) -> bool:
        return self.root is None

    def insert(self, key: int, value: Any = None) -> None:
        self.root = self._insert(AVLNode(key, value), self.root)

    def contains(self, key: int) -> bool:
        return self._contains(key, self.root)

    def delete(self, key: int) -> bool:
        """Delete ``key``; return True if it was in the tree."""
        self.root, deleted = self._delete(key, self.root)
        return deleted

    def size(self) -> int:
        return self._size(self.root)

    def inorder(self) -> list[int]:
        keys: list[int] = []
        self._inorder(self.root, keys)
        return keys

    def preorder(self) -> list[int]:
        keys: list[int] = []
        self._preorder(self.root, keys)
        return keys

    def postorder(self) -> list[int]:
        keys: list[int] = []
        self._postorder(self.root, keys)
        return keys

    # ------------------------------------------------------- recursive helpers
    def _insert(self, node: AVLNode, current: Optional[AVLNode]) -> AVLNode:
        if current is None:
            return node
        if node.key > current.key:
            current.right = self._insert(node, current.right)
        elif node.key < current.key:
            current.left = self._insert(node, current.left)
        else:
            return current  # duplicate key: the tree is unchanged

        self._update_height(current)
        return self._rebalance(self._balance_factor(current), current)

    def _contains(self, key: int, current: Optional[AVLNode]) -> bool:
        if current is None:
            return False
        if current.key == key:
            return True
        if key < current.key:
            return self._contains(key, current.left)
        return self._contains(key, current.right)

    def _delete(
        self, key: int, current: Optional[AVLNode]
    ) -> tuple[Optional[AVLNode], bool]:
        """Delete ``key`` from the subtree; return (new subtree root, deleted)."""
        if current is None:
            return None, False
        if key > current.key:
            current.right, deleted = self._delete(key, current.right)
        elif key < current.key:
            current.left, deleted = self._delete(key, current.left)
        else:
            # Three cases: leaf, one child, two children.
            if current.left is None and current.right is None:
                return None, True
            elif current.left is None:
                return current.right, True
            elif current.right is None:
                return current.left, True
            else:
                # Copy the in-order successor here and delete it on the right.
                successor = self._min_node(current.right)
                current.key, current.value = successor.key, successor.value
                current.right, deleted = self._delete(successor.key, current.right)

        self._update_height(current)
        return self._rebalance(self._balance_factor(current), current), deleted

    @staticmethod
    def _min_node(current: AVLNode) -> AVLNode:
        while current.left is not None:
            current = current.left
        return current

    def _size(self, node: Optional[AVLNode]) -> int:
        if node is None:
            return 0
        return 1 + self._size(node.left) + self._size(node.right)

    def _inorder(self, node: Optional[AVLNode], keys: list[int]) -> None:
        if node is not None:
            self._inorder(node.left, keys)
            keys.append(node.key)
            self._inorder(node.right, keys)

    def _preorder(self, node: Optional[AVLNode], keys: list[int]) -> None:
        if node is not None:
            keys.append(node.key)
            self._preorder(node.left, keys)
            self._preorder(node.right, keys)

    def _postorder(self, node: Optional[AVLNode], keys: list[int]) -> None:
        if node is not None:
            self._postorder(node.left, keys)
            self._postorder(node.right, keys)
            keys.append(node.key)

    # --------------------------------------------------------------- balancing
    @staticmethod
    def _height(node: Optional[AVLNode]) -> int:
        return 0 if node is None else node.height

    def _update_height(self, node: Optional[AVLNode]) -> None:
        # _height() handles None children, so max() never sees None.
        if node is not None:
            node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node: Optional[AVLNode]) -> int:
        if node is None:
            return 0
        return self._height(node.right) - self._height(node.left)

    def _rotate_right(self, p: AVLNode) -> AVLNode:
        q = p.left
        assert q is not None
        moved = q.right       # keep Q's right subtree so it is not lost
        q.right = p           # Q goes up, P becomes its right child
        p.left = moved        # Q's old right subtree becomes P's left
        self._update_height(p)  # P is now lower: update it first
        self._update_height(q)
        return q              # Q is the new root of this subtree

    def _rotate_left(self, p: AVLNode) -> AVLNode:
        q = p.right
        assert q is not None
        moved = q.left
        q.left = p
        p.right = moved
        self._update_height(p)
        self._update_height(q)
        return q

    def _rebalance(self, factor: int, p: AVLNode) -> AVLNode:
        if factor > 1:  # right-heavy
            q = p.right
            if self._balance_factor(q) >= 0:
                return self._rotate_left(p)            # RR: single rotation
            p.right = self._rotate_right(q)            # RL: double rotation
            return self._rotate_left(p)
        if factor < -1:  # left-heavy
            q = p.left
            if self._balance_factor(q) <= 0:
                return self._rotate_right(p)           # LL: single rotation
            p.left = self._rotate_left(q)              # LR: double rotation
            return self._rotate_right(p)
        return p


if __name__ == "__main__":
    tree = AVLTree()
    for key in (10, 20, 30):  # sorted input: a plain BST would be a list
        tree.insert(key)
    print("Root:", tree.root.key if tree.root else None)  # 20 after rotating
    print("Size:", tree.size())
    print("In-order:  ", tree.inorder())
    print("Pre-order: ", tree.preorder())
    print("Post-order:", tree.postorder())
