import pytest

from array_stack import ArrayStack
from linked_queue import LinkedQueue, LinkedStack
from static_list import ArrayLinkedList, ArrayList


# ---------------------------------------------------------------- ArrayStack
def test_stack_is_lifo():
    s = ArrayStack()
    for x in (1, 2, 3):
        s.push(x)
    assert len(s) == 3
    assert s.peek() == 3
    assert [s.pop(), s.pop(), s.pop()] == [3, 2, 1]
    assert s.is_empty()


def test_stack_pop_and_peek_on_empty_return_none(capsys):
    s = ArrayStack()
    assert s.pop() is None
    assert s.peek() is None
    assert "empty" in capsys.readouterr().out


def test_stack_overflow_is_ignored(capsys):
    s = ArrayStack(capacity=2)
    s.push("a")
    s.push("b")
    s.push("c")  # ignored
    assert "full" in capsys.readouterr().out
    assert len(s) == 2
    assert s.pop() == "b"


def test_stack_str():
    s = ArrayStack()
    assert str(s) == "The stack is empty."
    s.push(10)
    s.push(20)
    assert str(s) == "10, 20"


def test_stack_capacity_zero():
    s = ArrayStack(capacity=0)
    s.push(1)
    assert s.is_empty()


# --------------------------------------------------------------- LinkedQueue
def make_queue(*values):
    q = LinkedQueue()
    for v in values:
        q.enqueue(v)
    return q


def test_queue_is_fifo():
    q = make_queue(1, 2, 3)
    assert q.front() == 1
    assert q.size() == 3
    assert [q.dequeue(), q.dequeue(), q.dequeue()] == [1, 2, 3]
    assert q.is_empty()
    assert q.last is None  # both pointers reset when the queue empties


def test_queue_dequeue_empty_returns_none():
    q = LinkedQueue()
    assert q.dequeue() is None
    assert q.front() is None
    assert q.size() == 0


def test_queue_reusable_after_emptying():
    q = make_queue("a")
    q.dequeue()
    q.enqueue("b")
    assert q.to_list() == ["b"]


@pytest.mark.parametrize(
    "left, right, expected",
    [
        ((1, 2), (3, 4), [1, 2, 3, 4]),
        ((), (3, 4), [3, 4]),
        ((1, 2), (), [1, 2]),
        ((), (), []),
    ],
)
def test_queue_concatenate(left, right, expected):
    a, b = make_queue(*left), make_queue(*right)
    a.concatenate(b)
    assert a.to_list() == expected
    assert b.is_empty()
    if expected:
        a.enqueue(99)  # `last` must point to the real tail
        assert a.to_list() == expected + [99]


def test_queue_remove_keeps_order_and_only_first_match():
    q = make_queue(1, 2, 3, 2, 4)
    assert q.remove(2) is True
    assert q.to_list() == [1, 3, 2, 4]


def test_queue_remove_missing_and_empty():
    q = make_queue(1, 2)
    assert q.remove(9) is False
    assert q.to_list() == [1, 2]
    assert LinkedQueue().remove(1) is False


def test_queue_remove_last_element_updates_tail():
    q = make_queue(1, 2, 3)
    q.remove(3)
    q.enqueue(4)
    assert q.to_list() == [1, 2, 4]


# --------------------------------------------------------------- LinkedStack
def test_linked_stack():
    s = LinkedStack()
    assert s.pop() is None
    for x in "abc":
        s.push(x)
    assert s.to_list() == ["c", "b", "a"]
    assert s.pop() == "c"
    assert s.to_list() == ["b", "a"]


# ----------------------------------------------------------------- ArrayList
def test_array_list_insert_and_delete():
    lst = ArrayList(10)
    for x in (5, 8, 12):
        lst.append(x)
    lst.insert(99, 1)
    assert lst.to_list() == [5, 99, 8, 12]
    lst.delete(2)
    assert lst.to_list() == [5, 99, 12]


def test_array_list_insert_at_ends():
    lst = ArrayList(5)
    lst.insert("b", 0)
    lst.insert("a", 0)  # front
    lst.insert("c", 2)  # back (pos == size)
    assert lst.to_list() == ["a", "b", "c"]


def test_array_list_invalid_positions_are_ignored(capsys):
    lst = ArrayList(3)
    lst.append(1)
    lst.insert(2, 5)
    lst.insert(2, -1)
    lst.delete(1)
    lst.delete(-1)
    assert lst.to_list() == [1]
    assert "Invalid position" in capsys.readouterr().out


def test_array_list_full(capsys):
    lst = ArrayList(2)
    lst.append(1)
    lst.append(2)
    lst.append(3)
    lst.insert(0, 0)
    assert lst.to_list() == [1, 2]
    out = capsys.readouterr().out
    assert "List full" in out and "No free space" in out


def test_array_list_delete_last_clears_slot():
    lst = ArrayList(3)
    lst.append(1)
    lst.append(2)
    lst.delete(1)
    assert lst.elements[1] is None


# ----------------------------------------------------------- ArrayLinkedList
def test_array_linked_list_insert_until_full():
    lst = ArrayLinkedList(3)
    assert lst.to_list() == []
    assert lst.insert_last(10) and lst.insert_last(20) and lst.insert_last(30)
    assert lst.insert_last(40) is False  # no free slot
    assert lst.to_list() == [10, 20, 30]
    assert lst.free == []


def test_array_linked_list_links_by_index():
    lst = ArrayLinkedList(4)
    lst.insert_last("x")
    lst.insert_last("y")
    assert lst.head == 0
    assert lst.slots[0].next_index == 1
    assert lst.slots[1].next_index == -1
