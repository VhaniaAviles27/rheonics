from pathlib import Path
import pandas as pd

from .pipeline import analyze_series
from ..plotting.catalog import get_plot


def _detect_sample_type(df: pd.DataFrame) -> str:
    if "source_file" not in df.columns or df.empty:
        raise ValueError("El CSV no tiene columna source_file.")
    name = str(df["source_file"].iloc[0]).upper()
    if "SAMPLE-A" in name or "A-LOG" in name:
        return "A-LOG"
    if "SAMPLE-P" in name or "P-LOG" in name:
        return "P-LOG"
    raise ValueError(f"No se pudo determinar el tipo de muestra desde {name!r}")


def analyze_log(
    csv_path: str,
    plot_id: str,
    sensor_serial: str | None = None,
) -> dict:
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"No existe: {csv_path}")

    df = pd.read_csv(path, encoding="utf-8-sig", low_memory=False)
    definition = get_plot(plot_id)

    detected = _detect_sample_type(df)
    if detected != definition.sample_type:
        raise ValueError(
            f"El CSV es {detected} pero el plot {plot_id} es para "
            f"{definition.sample_type}."
        )

    target = df
    if sensor_serial and "sensor_serial" in df.columns:
        target = df[df["sensor_serial"] == sensor_serial]
        if target.empty:
            raise ValueError(f"Serie no encontrada: {sensor_serial}")

    col = definition.y_columns[0][0]
    if col not in target.columns:
        raise ValueError(f"Columna '{col}' no existe en el CSV.")

    x = pd.to_numeric(target["timestamp"], errors="coerce").to_numpy()
    y = pd.to_numeric(target[col], errors="coerce").to_numpy()

    return analyze_series(x, y)