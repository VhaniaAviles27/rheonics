from __future__ import annotations
import json
from pathlib import Path
import pandas as pd
from src.constants.p_log_constants import EXPECTED_FIELD_COUNT, FIELDS_PER_PARAMETER, PARAMETERS
from src.utils.log_parser_util import base_row, finalize_row, iter_lines, parse_number, parse_timestamp

def _new_row(path, line_number, raw_line, field_count):
    row = base_row(path, line_number)
    row.update(overall_status=None, pressure=float("nan"),
           field_count=field_count)
    for name in PARAMETERS.values():
        for suffix in FIELDS_PER_PARAMETER:
            row[f"{name}_{suffix}"] = None if suffix.startswith("status") else float("nan")
    return row

def _parse_parameters(fields, row, errors) -> None:
    for parameter_index, name in PARAMETERS.items():
        start = 1 + parameter_index * 4
        for offset, suffix in enumerate(FIELDS_PER_PARAMETER):
            idx = start + offset
            if idx >= len(fields):
                continue
            column, value = f"{name}_{suffix}", fields[idx]
            if suffix.startswith("status"):
                row[column] = value or None
            else:
                row[column] = _measurement(value, column, errors)

def _measurement(value: str, label: str, errors) -> float:
    normalized_value = value.strip().lower()

    if normalized_value in ("", "nan"):
        errors.append(f"missing_measurement:{label}")
        return float("nan")

    try:
        return parse_number(value)
    except ValueError:
        errors.append(f"invalid_numeric_value:{label}={value}")
        return float("nan")

def _parse_tail(fields, row, errors) -> None:
    if len(fields) != EXPECTED_FIELD_COUNT:
        return
    row["overall_status"] = fields[-2] or None
    if fields[-1] == "":
        errors.append("missing_pressure")
    else:
        row["pressure"] = _measurement(fields[-1], "pressure", errors)


def _parse_line(path, line_number, raw_line) -> dict:
    fields = [f.strip() for f in raw_line.strip().split(";")]
    row, errors = _new_row(path, line_number, raw_line, len(fields)), []

    if len(fields) != EXPECTED_FIELD_COUNT:
        errors.append(f"field_count_mismatch:expected_{EXPECTED_FIELD_COUNT}_got_{len(fields)}")

    if fields[0]:
        row["timestamp"], row["timestamp_utc"], ok = parse_timestamp(fields[0])
        if not ok:
            errors.append("invalid_timestamp")
    else:
        errors.append("missing_timestamp")

    _parse_parameters(fields, row, errors)
    _parse_tail(fields, row, errors)
    return finalize_row(row, errors)


def parse_p_log(path: str | Path, *, encoding: str = "utf-8") -> pd.DataFrame:
    source = Path(path)
    return pd.DataFrame(_parse_line(source, n, raw) for n, raw in iter_lines(source, encoding))