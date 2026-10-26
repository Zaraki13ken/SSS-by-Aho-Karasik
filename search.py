"""Модуль поиска подстрок в строке алгоритмом Ахо-Корасик."""
from __future__ import annotations

from typing import Optional, Union

from bor import Bor
from decorators import time_logger

@time_logger
def search(
    string: str,
    sub_string: Union[str, list[str], tuple[str, ...]],
    case_sensitivity: bool = False,
    method: str = "first",
    count: Optional[int] = None,
) -> Optional[Union[tuple[int, ...], dict[str, Optional[tuple[int, ...]]]]]:
    """Ищет все вхождения подстрок в строке алгоритмом Ахо-Корасик."""

    is_single = isinstance(sub_string, str)
    patterns = [sub_string] if is_single else list(sub_string)

    if not case_sensitivity:
        string = string.lower()
        patterns = [w.lower() for w in patterns]

    if not string or not patterns:
        return None

    bor = Bor()
    for word in patterns:
        bor.add_word(word)
    bor.build_suff_links()
    found = bor.search(string)

    flat = []
    for word, indexes in found.items():
        for pos in indexes:
            flat.append((pos, word))

    if not flat:
        return None

    is_reverse = method == "last"
    flat.sort(key=lambda x: x[0], reverse=is_reverse)

    if count is not None:
        flat = flat[:count]

    grouped: dict[str, Optional[tuple[int, ...]]] = {word: None for word in patterns}
    for pos, word in flat:
        if grouped[word] is None:
            grouped[word] = (pos,)
        else:
            grouped[word] = grouped[word] + (pos,)

    if is_single:
        return grouped[patterns[0]]

    if all(v is None for v in grouped.values()):
        return None

    return grouped
