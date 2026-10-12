import random

import pytest

from avl import AVLTree
from bst import BST


# ----------------------------------------------------------------- helpers
def build_bst(keys):
    t = BST()
    for k in keys:
        t.insert(k, f"v{k}")
    return t


def build_avl(keys):
    t = AVLTree()
    for k in keys:
        t.insert(k, f"v{k}")
    return t


def check_avl_invariants(node):
    """Return the height of ``node`` after asserting BST order, stored
    heights and the AVL balance condition on the whole subtree."""
    if node is None:
        return 0
    hl = check_avl_invariants(node.left)
    hr = check_avl_invariants(node.right)
    if node.left:
        assert node.left.key < node.key
    if node.right:
        assert node.right.key > node.key
    assert node.height == 1 + max(hl, hr)
    assert abs(hr - hl) <= 1
    return node.height


# --------------------------------------------------------------------- BST
def test_bst_traversals():
    t = build_bst([50, 30, 70, 20, 40, 60, 80])
    assert t.inorder() == [20, 30, 40, 50, 60, 70, 80]
    assert t.preorder() == [50, 30, 20, 40, 70, 60, 80]
    assert t.postorder() == [20, 40, 30, 60, 80, 70, 50]


def test_bst_empty_tree():
    t = BST()
    assert t.inorder() == [] and t.preorder() == [] and t.postorder() == []
    assert t.search(1) is None
    t.delete(1)  # deleting from an empty tree is a no-op
    assert t.root is None


def test_bst_search():
    t = build_bst([50, 30, 70])
    assert t.search(30).value == "v30"
    assert t.search(31) is None


def test_bst_ignores_duplicates():
    t = build_bst([5, 5, 3, 5])
    assert t.inorder() == [3, 5]


def test_bst_delete_leaf_and_one_child():
    t = build_bst([50, 30, 70, 20, 80])
    t.delete(20)                      # leaf
    assert t.inorder() == [30, 50, 70, 80]
    t.delete(70)                      # one child (80)
    assert t.inorder() == [30, 50, 80]
    t.delete(999)                     # missing key
    assert t.inorder() == [30, 50, 80]


def test_bst_sorted_input_degenerates_to_a_list():
    t = build_bst(range(1, 6))
    node, depth = t.root, 0
    while node:
        depth += 1
        node = node.right
    assert depth == 5  # height n: this is why avl.py exists


# --------------------------------------------------------------------- AVL
def test_avl_sorted_insertions_rotate():
    t = build_avl([10, 20, 30])          # RR case -> single left rotation
    assert t.root.key == 20
    assert t.inorder() == [10, 20, 30]
    assert t.preorder() == [20, 10, 30]
    assert t.postorder() == [10, 30, 20]


@pytest.mark.parametrize("keys, root", [
    ([30, 20, 10], 20),   # LL
    ([10, 20, 30], 20),   # RR
    ([30, 10, 20], 20),   # LR (double rotation)
    ([10, 30, 20], 20),   # RL (double rotation)
])
def test_avl_four_rotation_cases(keys, root):
    t = build_avl(keys)
    assert t.root.key == root
    check_avl_invariants(t.root)


def test_avl_stays_balanced_on_many_insertions():
    t = build_avl(range(1000))           # worst case for a plain BST
    height = check_avl_invariants(t.root)
    assert height <= 15                  # 1.44 * log2(1001) ~ 14.4
    assert t.inorder() == list(range(1000))
    assert t.size() == 1000


def test_avl_random_insertions():
    rng = random.Random(42)
    keys = rng.sample(range(10_000), 500)
    t = build_avl(keys)
    check_avl_invariants(t.root)
    assert t.inorder() == sorted(keys)
    assert all(t.contains(k) for k in keys)
    assert not t.contains(-1)


def test_avl_empty():
    t = AVLTree()
    assert t.is_empty()
    assert t.size() == 0
    assert t.inorder() == []
    assert not t.contains(5)


# ------------------------------------------------- regression tests (fixes)
def test_bst_delete_node_with_two_children():
    t = build_bst([50, 30, 70, 20, 40, 60, 80])
    t.delete(30)                      # two children: successor is 40
    assert t.inorder() == [20, 40, 50, 60, 70, 80]
    assert t.search(40).value == "v40"   # payload moved with the key
    t.delete(50)                      # the root, two children
    assert t.inorder() == [20, 40, 60, 70, 80]
    assert t.root.key == 60 and t.root.value == "v60"


def test_bst_delete_everything_in_random_order():
    rng = random.Random(1)
    keys = rng.sample(range(1000), 200)
    t = build_bst(keys)
    remaining = set(keys)
    for k in rng.sample(keys, len(keys)):
        t.delete(k)
        remaining.discard(k)
        assert t.inorder() == sorted(remaining)
    assert t.root is None
