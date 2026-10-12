from __future__ import annotations
from pathlib import Path
import pandas as pd
from src.constants.a_log_constants import HEADER_RE, KNOWN_TAGS, TAG_DEFINITIONS, TIMESTAMP_RE
from src.utils.log_parser_util import base_row, finalize_row, iter_lines, parse_number, parse_timestamp

def _new_row(path, line_number, raw_line):
    row = base_row(path, line_number)
    row.update(
        sensor_serial=None,
        firmware_version=None,
        electronics_serial=None,
    )
    return row

def _parse_header(body: str, row, errors) -> str:
    match = HEADER_RE.match(body)
    if not match:
        errors.append("missing_or_malformed_identification_header")
        return ""
    parts = match.group("header").split()
    if len(parts) < 3:
        errors.append("incomplete_identification_header")
    else:
        row["sensor_serial"], row["firmware_version"], row["electronics_serial"] = parts[:3]
        if len(parts) > 3:
            errors.append("extra_identification_header_fields")
    return match.group("measurements")

def _parse_measurements(text: str, row, errors) -> None:
    tokens = text.split()
    i = 0
    while i < len(tokens):
        tag = tokens[i]

        if tag not in KNOWN_TAGS:
            if i + 1 < len(tokens):
                errors.append(f"unknown_tag:{tag}")
                i += 2
            else:
                i += 1
            continue

        if i + 1 >= len(tokens):
            errors.append(f"missing_value_for_tag:{tag}")
            i += 1
            continue

        value = tokens[i + 1]

        if value in KNOWN_TAGS:
            errors.append(f"missing_value_for_tag:{tag}")
            i += 1
            continue

        _assign_tag(row, tag, value, errors)
        i += 2


def _assign_tag(row, tag, value, errors) -> None:
    definition = TAG_DEFINITIONS[tag]
    column = definition["name"]

    if tag == "E":
        row[column] = value
        return
    
    if definition["data_type"] == "float":
        try:
            row[column] = parse_number(value)
        except ValueError:
            errors.append(
                f"invalid_numeric_value:{tag}={value}"
            )
        return
    row[column] = value

def _parse_line(path, line_number, raw_line) -> dict:
    row, errors = _new_row(path, line_number, raw_line), []
    match = TIMESTAMP_RE.match(raw_line.strip())
    body = ""
    if not match:
        errors.append("invalid_or_missing_timestamp")
    else:
        row["timestamp"], row["timestamp_utc"], ok = parse_timestamp(match.group("timestamp"))
        if not ok:
            errors.append("invalid_timestamp")
        body = match.group("body")

    _parse_measurements(_parse_header(body, row, errors), row, errors)
    return finalize_row(row, errors)


def parse_a_log(path: str | Path, *, encoding: str = "utf-8") -> pd.DataFrame:
    source = Path(path)
    return pd.DataFrame(_parse_line(source, n, raw) for n, raw in iter_lines(source, encoding))
