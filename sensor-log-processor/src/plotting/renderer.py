import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
import json

from .catalog import PlotDefinition, ChartType


def _detect_sample_type(df: pd.DataFrame) -> str:
    """Lee la primera fila de source_file y devuelve A-LOG o P-LOG."""
    if "source_file" not in df.columns or df.empty:
        raise ValueError("El CSV no tiene columna source_file.")
    name = str(df["source_file"].iloc[0]).upper()
    if "SAMPLE-A" in name or "A-LOG" in name:
        return "A-LOG"
    if "SAMPLE-P" in name or "P-LOG" in name:
        return "P-LOG"
    raise ValueError(f"No se pudo determinar el tipo de muestra desde {name!r}")


def _prepare_x(df: pd.DataFrame) -> pd.Series:
    """Eje X: usa timestamp_utc como datetime. Fallback a timestamp numérico."""
    if "timestamp_utc" in df.columns:
        return pd.to_datetime(df["timestamp_utc"], errors="coerce")
    return pd.to_numeric(df["timestamp"], errors="coerce")


def _render_a_log(df: pd.DataFrame, definition: PlotDefinition, mode: str) -> list[go.Scatter]:
    col, _ = definition.y_columns[0]
    x = _prepare_x(df)
    traces = []
    for serial, group in df.groupby("sensor_serial", sort=False):
        traces.append(
            go.Scatter(
                x=x.loc[group.index],
                y=group[col],
                mode=mode,
                name=str(serial),
                hovertemplate=(
                    "%{x|%Y-%m-%d %H:%M}<br>%{y}"
                    "<extra>" + str(serial) + "</extra>"
                ),
            )
        )
    return traces


def _render_p_log(df: pd.DataFrame, definition: PlotDefinition, mode: str) -> list[go.Scatter]:
    x = _prepare_x(df)
    traces = []
    for col, label in definition.y_columns:
        if col not in df.columns:
            continue
        traces.append(
            go.Scatter(
                x=x,
                y=pd.to_numeric(df[col], errors="coerce"),
                mode=mode,
                name=label,
                hovertemplate=(
                    "%{x|%Y-%m-%d %H:%M}<br>%{y}"
                    "<extra>" + label + "</extra>"
                ),
            )
        )
    return traces


def render_plot(
    df: pd.DataFrame,
    definition: PlotDefinition,
    chart_type: ChartType,
) -> dict:
    """Construye la figura Plotly y la devuelve como dict serializable a JSON."""
    detected = _detect_sample_type(df)
    if detected != definition.sample_type:
        raise ValueError(
            f"El CSV es {detected} pero el plot {definition.id} es para {definition.sample_type}."
        )

    mode = "lines" if chart_type == "line" else "markers"

    traces = (
        _render_a_log(df, definition, mode)
        if definition.sample_type == "A-LOG"
        else _render_p_log(df, definition, mode)
    )

    y_axis_title = definition.y_label
    if definition.unit:
        y_axis_title += f" ({definition.unit})"

    fig = go.Figure(data=traces)
    fig.update_layout(
        title={"text": definition.label, "x": 0.02, "xanchor": "left"},
        xaxis_title="Time (UTC)",
        yaxis_title=y_axis_title,
        hovermode="x unified",
        margin={"l": 60, "r": 20, "t": 50, "b": 50},
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1,
        },
        template="plotly_white",
    )

    return json.loads(json.dumps(fig, cls=PlotlyJSONEncoder))