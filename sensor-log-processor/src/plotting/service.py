from pathlib import Path

import pandas as pd

from .catalog import ChartType, get_plot, list_plots
from .renderer import render_plot


def load_log_csv(csv_path: str | Path) -> pd.DataFrame:
    """Carga un CSV generado por el pipeline."""
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"No existe: {csv_path}")
    return pd.read_csv(path, encoding="utf-8-sig", low_memory=False)


def plot_log(csv_path: str, plot_id: str, chart_type: ChartType = "line") -> dict:
    if chart_type not in ("line", "scatter"):
        raise ValueError(f"chart_type inválido: {chart_type}")

    definition = get_plot(plot_id)
    df = load_log_csv(csv_path)
    return render_plot(df, definition, chart_type)