from functools import partial

import pandas as pd


def is_positive(series) -> None:
    for index, item in series.items():
        if item <= 0:
            raise ValueError(
                f"Illegal value at index {index} in column '{series.name}': {item}"
            )


def is_in_range(min_value: int, max_value: int) -> None:
    return partial(_is_in_range_inner, min_value=min_value, max_value=max_value)


def _is_in_range_inner(item, min_value: int, max_value: int) -> None:
    if (item < min_value) or (item > max_value):
        raise ValueError("Illegal value")
