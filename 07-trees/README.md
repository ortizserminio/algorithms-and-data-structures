# 07 · Trees: binary search tree and AVL tree
n**English** · [Español](README.es.md)

Language: **Python 3.10+**. Source: *Estructuras de Datos*, practical 2 (2024/25: BST; 2025/26: AVL).

## Binary search tree: [`bst.py`](bst.py)

**Use case in the practical:** a library keeps one BST of books per genre, keyed by a 6-digit id.

**Invariant:** every key in a node's left subtree is smaller than the node's key, and every key in its right subtree is larger.

* **Insert / search:** compare with the current node and recurse left or right.
* **Delete** has three cases:
  1. Leaf: remove it.
  2. One child: replace the node by that child.
  3. Two children: copy the **in-order successor** (the minimum of the right subtree) into the node, then delete the successor from the right subtree. The successor has no left child, so case 1 or 2 applies to it.
* **Traversals:** in-order (yields sorted keys), pre-order and post-order.

**Complexity.** Insert, search and delete are **O(h)**, where `h` is the height. That is O(log n) when the tree is balanced, but **O(n)** when keys arrive in sorted order: the tree degenerates into a linked list, and a test demonstrates it. Traversals are O(n).

## AVL tree: [`avl.py`](avl.py)

An AVL tree fixes the BST's worst case. Every node stores its height, and after each insertion or deletion the nodes on the way back to the root check their **balance factor** `height(right) − height(left)`. If it leaves `[−1, 1]`, one of four rotations restores it:

| Case | Shape | Fix |
|---|---|---|
| RR | right child is right-heavy (or balanced) | single left rotation |
| LL | left child is left-heavy (or balanced) | single right rotation |
| RL | right child is left-heavy | rotate the child right, then the node left |
| LR | left child is right-heavy | rotate the child left, then the node right |

A rotation only re-links three pointers and updates two heights, so it is O(1).

**Complexity.** The height of an AVL tree is at most about 1.44·log₂(n+2). Insert, search and delete are therefore **O(log n) in the worst case**, with O(log n) recursion stack. A test inserts 1 000 *sorted* keys and checks that the height stays ≤ 15. A plain BST would reach height 1 000.

**Why AVL and not another balanced tree?** AVL trees are more strictly balanced than red-black trees, so lookups are slightly faster. The price is more rotations on updates. Red-black trees (used by `std::map` and Java's `TreeMap`) are preferred for write-heavy workloads, and B-trees for data on disk. For an in-memory structure that is read more than written, AVL is a good choice, and it is the one the course covers.

## Fixes over the original practicals

The code was first ported as-is and then fixed in separate commits, each with regression tests:

* **BST:** deleting a node with two children used `actual.id`, but books stored their key in `id_libro`, so it raised `AttributeError`. Even with the right attribute only the key would have been copied, leaving the wrong payload. Now both key and value are copied.
* **AVL:** the delete helper was defined as `elimnar_recursivo` but called as `eliminar_recursivo`, so every deletion crashed. It also returned a bare node where callers expected `(node, deleted)`. Inserting a duplicate key returned a *string*, which was then stored as a child.

## Run and test

```bash
python -m pytest 07-trees
python 07-trees/avl.py
python 07-trees/bst.py
```

There are 19 tests: traversal orders, the four rotation cases, an invariant checker (BST order, stored heights, |balance| ≤ 1) run after every insertion and deletion on random data, deletion of the root, leaves and missing keys, and duplicates.
