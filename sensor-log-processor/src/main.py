from pathlib import Path

from src.service.log_processing import process_log
from src.validation.log_validation import validation_summary

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_DIR = PROJECT_ROOT / "data" / "input"


def main() -> None:
    files = [
        ("SAMPLE-A.LOG", "A-LOG"),
        ("SAMPLE-P.LOG", "P-LOG"),
    ]

    for input_name, log_type in files:
        input_path = INPUT_DIR / input_name

        if not input_path.is_file():
            raise FileNotFoundError(f"No se encontró: {input_path}")

        result = process_log(input_path, log_type)

        print(f"\n{log_type}")
        print(f"Registros: {result['total_records']}")
        print(f"Válidos: {result['valid_records']}")
        print(f"Inválidos: {result['invalid_records']}")
        print(f"CSV generado: {result['output_path']}")


if __name__ == "__main__":
    main()