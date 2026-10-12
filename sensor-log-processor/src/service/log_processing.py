import json
from pathlib import Path
from typing import Literal
from src.parsers.a_log_parser import parse_a_log
from src.parsers.p_log_parser import parse_p_log

LogType = Literal["A-LOG", "P-LOG"]

def process_log(path: str | Path, log_type: LogType) -> dict:
    source = Path(path)

    if not source.is_file():
        raise FileNotFoundError(
            f"No se encontró el archivo: {source}"
        )

    if log_type == "A-LOG":
        df = parse_a_log(source)
    elif log_type == "P-LOG":
        df = parse_p_log(source)
    else:
        raise ValueError(f"Tipo de log no soportado: {log_type}")

    if "is_valid" in df.columns:
        valid_records = int(df["is_valid"].eq(True).sum())
        invalid_records = int(df["is_valid"].eq(False).sum())
    else:
        valid_records = 0
        invalid_records = 0

    records = json.loads(
        df.to_json(
            orient="records",
            date_format="iso",
            force_ascii=False,
        )
    )

    return {
        "log_type": log_type,
        "file_name": source.name,
        "total_records": len(df),
        "valid_records": valid_records,
        "invalid_records": invalid_records,
        "columns": list(df.columns),
        "records": records,
    }