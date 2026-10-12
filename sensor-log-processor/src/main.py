from pathlib import Path
from src.service.log_processing import process_log
from src.validation.log_validation import validation_summary

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_DIR = PROJECT_ROOT / "data" / "input"
OUTPUT_DIR = PROJECT_ROOT / "data" / "output"

def main() -> None:
    files = [
        ("SAMPLE-A.LOG", "A-LOG", "SAMPLE-A.CSV"),
        ("SAMPLE-P.LOG", "P-LOG", "SAMPLE-P.CSV"),
    ]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for input_name, log_type, output_name in files:
        input_path = INPUT_DIR / input_name

        if not input_path.is_file():
            raise FileNotFoundError(
                f"No se encontró el archivo de entrada: {input_path}"
            )

        result = process_log(input_path, log_type)
        import pandas as pd

        df = pd.DataFrame(result["records"], columns=result["columns"])

        if "raw_line" in df.columns:
            columns = [col for col in df.columns if col != "raw_line"]
            df = df[columns + ["raw_line"]]

        output_path = OUTPUT_DIR / output_name
        df.to_csv(output_path, index=False, encoding="utf-8-sig")

        print(f"\n{log_type}")
        print(validation_summary(df))
        print(f"Registros: {result['total_records']}")
        print(f"CSV generado: {output_path}")


if __name__ == "__main__":
    main()