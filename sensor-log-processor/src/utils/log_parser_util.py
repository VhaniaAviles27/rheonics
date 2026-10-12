from __future__ import annotations
import math
from pathlib import Path
from typing import Any, Iterator
import pandas as pd

def parse_number(value: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"not a finite number: {value!r}")
    return number

def parse_timestamp(text: str) -> tuple[int | None, Any, bool]:
    try:
        seconds = int(text)
    except ValueError:
        return None, pd.NaT, False
    try:
        return seconds, pd.to_datetime(seconds, unit="s", utc=True), True
    except (ValueError, OverflowError, pd.errors.OutOfBoundsDatetime):
        return seconds, pd.NaT, False

def iter_lines(path: Path, encoding: str) -> Iterator[tuple[int, str]]:
    with path.open("r", encoding=encoding, errors="replace") as file:
        for line_number, raw_line in enumerate(file, start=1):
            if raw_line.strip():
                yield line_number, raw_line

def base_row(path: Path, line_number: int) -> dict[str, Any]:
    return {
        "source_file": path.name,
        "line_number": line_number,
        "timestamp": None,
        "timestamp_utc": pd.NaT,
    }

def finalize_row(row: dict[str, Any], errors: list[str]) -> dict[str, Any]:
    row["description_error"] = "; ".join(errors)
    row["is_valid"] = not errors
    return row
