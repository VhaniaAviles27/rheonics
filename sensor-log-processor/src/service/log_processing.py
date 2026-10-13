import json
from pathlib import Path
from typing import Literal

from src.parsers.a_log_parser import parse_a_log
from src.parsers.p_log_parser import parse_p_log

LogType = Literal["A-LOG", "P-LOG"]

_DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[2] / "data" / "output"

def process_log(
    path: str | Path,
    log_type: LogType,
    output_path: str | Path | None = None,
    write_csv: bool = True,
) -> dict:
    source = Path(path)

    if not source.is_file():
        raise FileNotFoundError(f"No se encontró el archivo: {source}")

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
        df.to_json(orient="records", date_format="iso", force_ascii=False)
    )

    result = {
        "log_type": log_type,
        "file_name": source.name,
        "total_records": len(df),
        "valid_records": valid_records,
        "invalid_records": invalid_records,
        "columns": list(df.columns),
        "records": records,
    }

    if write_csv:
        out = (
            Path(output_path)
            if output_path is not None
            else _DEFAULT_OUTPUT_DIR / f"{source.stem}.CSV"
        )
        out.parent.mkdir(parents=True, exist_ok=True)

        export_df = df
        if "raw_line" in export_df.columns:
            cols = [c for c in export_df.columns if c != "raw_line"]
            export_df = export_df[cols + ["raw_line"]]

        export_df.to_csv(out, index=False, encoding="utf-8-sig")
        result["output_path"] = str(out)

    return result