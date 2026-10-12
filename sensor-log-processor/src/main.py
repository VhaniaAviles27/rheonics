
from pathlib import Path

from src.parsers.a_log_parser import parse_a_log
from src.parsers.p_log_parser import parse_p_log
from src.validation.log_validation import (
    validation_summary,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_DIR = PROJECT_ROOT / "data" / "input"
OUTPUT_DIR = PROJECT_ROOT / "data" / "output"


def main() -> None:
    a_log_path = INPUT_DIR / "SAMPLE-A.LOG"
    p_log_path = INPUT_DIR / "SAMPLE-P.LOG"

    for path in (a_log_path, p_log_path):
        if not path.is_file():
            raise FileNotFoundError(
                f"No se encontró el archivo de entrada: {path}"
            )

    a_df = parse_a_log(a_log_path)
    p_df = parse_p_log(p_log_path)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    a_csv_path = OUTPUT_DIR / "SAMPLE-A.CSV"
    p_csv_path = OUTPUT_DIR / "SAMPLE-P.CSV"

    if "raw_line" in a_df.columns:
        a_columns = [
            col for col in a_df.columns if col != "raw_line"
        ]
        a_df = a_df[a_columns + ["raw_line"]]

    if "raw_line" in p_df.columns:
        p_columns = [
            col for col in p_df.columns if col != "raw_line"
        ]
        p_df = p_df[p_columns + ["raw_line"]]

    a_df.to_csv(a_csv_path, index=False, encoding="utf-8-sig")
    p_df.to_csv(p_csv_path, index=False, encoding="utf-8-sig")

    print("A-LOG")
    print(validation_summary(a_df))

    print("\nP-LOG")
    print(validation_summary(p_df))

    print(f"\nRegistros A-LOG: {len(a_df)}")
    print(f"Registros P-LOG: {len(p_df)}")

    print(f"\nCSV generado: {a_csv_path}")
    print(f"CSV generado: {p_csv_path}")


if __name__ == "__main__":
    main()
