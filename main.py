"""Консольная утилита для поиска подстрок."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from search import search

COLORS = [
    "\033[91m",  # красный
    "\033[92m",  # зеленый
    "\033[93m",  # желтый
    "\033[94m",  # синий
    "\033[95m",  # пурпурный
    "\033[96m",  # голубой
]
RESET = "\033[0m"
MAX_LINES = 10


def highlight( # pylint: disable=too-many-locals
    text: str,
    result: dict[str, tuple[int, ...] | None],
    max_lines: int = MAX_LINES,
) -> str:
    """Раскрашивает найденные подстроки в тексте."""
    lines = text.splitlines(keepends=True)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
    truncated = "".join(lines)
    max_len = len(truncated)

    intervals = []
    for word, idxs in result.items():
        if idxs is None:
            continue
        for start in idxs:
            end = start + len(word)
            if end <= max_len:
                intervals.append((start, end, word))

    if not intervals:
        return truncated

    intervals.sort()

    color_map = {word: COLORS[i % len(COLORS)] for i, word in enumerate(result)}
    pieces = []
    last = 0
    for (s, e, w) in intervals:
        if s < last:
            continue
        pieces.append(truncated[last:s])
        pieces.append(color_map[w] + truncated[s:e] + RESET)
        last = e
    pieces.append(truncated[last:])
    return "".join(pieces)


def main() -> None:
    """Точка входа консольной утилиты."""
    parser = argparse.ArgumentParser(description="Поиск подстрок в строке (Ахо-Корасик)")
    parser.add_argument("--string", type=str, help="Строка для поиска")
    parser.add_argument("--file", type=str, help="Путь до файла")
    parser.add_argument("--substring", nargs="+", required=True, help="Подстроки")
    parser.add_argument("--method", choices=["first", "last"], default="first")
    parser.add_argument("--count", type=int, default=None)
    parser.add_argument("--case", action="store_true", help="Учитывать регистр")
    args = parser.parse_args()

    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    elif args.string:
        text = args.string
    else:
        print("Ошибка: нужно указать --string или --file", file=sys.stderr)
        sys.exit(1)

    result = search(
        string=text,
        sub_string=args.substring,
        case_sensitivity=args.case,
        method=args.method,
        count=args.count,
    )

    if result is None:
        print("Ничего не найдено")
        return

    if isinstance(result, tuple):
        result = {args.substring[0]: result}

    print("Результат:", result)
    print("\nПодсветка:")
    print(highlight(text, result))


if __name__ == "__main__":
    main()
