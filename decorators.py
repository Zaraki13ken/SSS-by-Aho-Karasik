"""Декоратор."""
import functools
import time


def time_logger(func):
    """Декоратор, логирующий время выполнения функции."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[TIME] {func.__name__} выполнено за {elapsed:.6f} сек.")
        return result
    return wrapper
