"""Модуль с реализацией бора и алгоритма Ахо-Корасик."""
from __future__ import annotations

from collections import deque


class Node: # pylint: disable=too-few-public-methods
    """Узел бора."""

    def __init__(self) -> None:
        self.children: dict[str, "Node"] = {}
        self.terminal = False
        self.suff_link: Node | None = None
        self.name: str = ""


class Bor:
    """Бор (префиксное дерево) с суффиксными ссылками."""

    def __init__(self) -> None:
        self.root = Node()

    def add_word(self, word: str) -> None:
        """Добавляет слово в бор."""
        name = ""
        current = self.root
        for symb in word:
            if symb not in current.children:
                current.children[symb] = Node()
            current = current.children[symb]
            name += symb
            current.name = name
        current.terminal = True

    def build_suff_links(self) -> None:
        """Строит суффиксные ссылки."""
        queue: deque[Node] = deque()
        for child in self.root.children.values():
            child.suff_link = self.root
            queue.append(child)

        while queue:
            current = queue.popleft()
            for symb, child in current.children.items():
                link_candidate = current.suff_link
                while link_candidate != self.root and symb not in link_candidate.children:
                    link_candidate = link_candidate.suff_link
                if symb in link_candidate.children:
                    child.suff_link = link_candidate.children[symb]
                else:
                    child.suff_link = self.root
                queue.append(child)

    def search(self, text: str) -> dict[str, tuple[int, ...]]:
        """Ищет все вхождения слов в text."""
        result: dict[str, list[int]] = {}
        current = self.root

        for i, char in enumerate(text):
            while current != self.root and char not in current.children:
                current = current.suff_link
            if char in current.children:
                current = current.children[char]

            temp = current
            while temp != self.root:
                if temp.terminal:
                    start = i - len(temp.name) + 1
                    result.setdefault(temp.name, []).append(start)
                temp = temp.suff_link

        return {word: tuple(idx) for word, idx in result.items()}
