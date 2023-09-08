
from typing import Any, Iterable

class Node:
    def __init__(self, value: Any) -> None:
        self.value: Any = value
        self.prev: Node = None
        self.next: Node = None

class SimpleQueue:
    def __init__(self, iterable: Iterable[Any]) -> None:
        for value in iterable:
            self._tail = Node(value)
            try:
                self._tail.next = node
            except UnboundLocalError:
                node = self._tail
                self._head = node
            else:
                self._tail.next = node
                node.prev = self._tail
                node = self._tail

    def __bool__(self) -> bool:
        return self._head is not None

    def append(self, value: Any) -> None:
        new_node = Node(value)
        if not self._head:
            self._head = new_node
            self._tail = new_node
        else:
            new_node.prev = self._tail
            self._tail.next = new_node
            self._tail = new_node

    def popleft(self) -> Any:
        if not self._head:
            raise IndexError("Nothing in the queue!")
        
        value = self._head.value
        if self._head is self._tail:
            self._head = None
            self._tail = None
        else:
            self._head = self._head.next
            self._head.prev = None

        return value

