import math

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
import json

SIGNAL_COLOR = "#1c7ed6"
TREND_COLOR = "#f59f00"
BAND_FILL = "#ffe066"
BAND_OPACITY = 0.35
SPIKE_MARKER = "#e67700"

def build_figure(
    x: np.ndarray,
    y: np.ndarray,
    analysis: dict,
    title: str,
    y_label: str,
    unit: str | None = None,
) -> dict:
    x_series = _to_datetime(x)
    y_series = pd.Series(y)

    traces: list[go.Scatter] = []

    traces.append(
        go.Scatter(
            x=x_series,
            y=y_series,
            mode="lines",
            name="Signal",
            line=dict(color=SIGNAL_COLOR, width=1.5),
            hovertemplate="%{x}<br>%{y:.4g}<extra>Signal</extra>",
        )
    )

    trend = analysis.get("trend") or {}
    fitted = trend.get("fitted")
    if fitted is not None:
        label = "Trend (linear)"
        if trend.get("r2") is not None:
            label += f"  R²={trend['r2']:.3f}"
        traces.append(
            go.Scatter(
                x=x_series,
                y=fitted,
                mode="lines",
                name=label,
                line=dict(color=TREND_COLOR, width=2),
                hovertemplate="Trend: %{y:.4g}<extra></extra>",
            )
        )

    anomalies = analysis.get("anomalies") or {}

    spikes = anomalies.get("spikes", [])
    if spikes:
        idx = [s["index"] for s in spikes]
        xs = _at_many(x_series, idx)
        ys = [s["value"] for s in spikes]
        texts = [
            f"Spike<br>value={s['value']:.4g}"
            + (f"<br>expected={s['expected']:.4g}" if s.get("expected") is not None else "")
            + f"<br>z={s['z_score']:.2f}"
            for s in spikes
        ]
        traces.append(
            go.Scatter(
                x=xs,
                y=ys,
                mode="markers",
                name=f"Spikes ({len(spikes)})",
                marker=dict(
                    color=SPIKE_MARKER,
                    size=8,
                    symbol="circle",
                    line=dict(width=1, color="white"),
                ),
                text=texts,
                hovertemplate="%{text}<extra></extra>",
            )
        )
    shapes: list[dict] = []
    for s in spikes:
        shapes.append(_step_line(x_series, s["index"]))
    for st in anomalies.get("steps", []):
        shapes.append(_step_line(x_series, st["index"]))
    for g in anomalies.get("gaps", []):
        shapes.append(_wide_band(x_series, g["start_index"], g["end_index"]))
    for r in anomalies.get("nan_runs", []):
        shapes.append(_wide_band(x_series, r["start_index"], r["end_index"]))

    y_title = y_label + (f" ({unit})" if unit else "")

    fig = go.Figure(data=traces)
    fig.update_layout(
        title={"text": title, "x": 0.02, "xanchor": "left"},
        xaxis_title="Time",
        yaxis_title=y_title,
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
        shapes=shapes,
    )

    fig_dict = fig.to_plotly_json()
    return sanitize(fig_dict)

def _to_datetime(x: np.ndarray) -> pd.Series:
    finite = x[np.isfinite(x)]
    if len(finite) > 0 and finite.min() > 1e9:
        dt = pd.to_datetime(x, unit="s", errors="coerce")
        return pd.Series(
            [None if pd.isna(t) else t.isoformat() for t in dt]
        )
    return pd.Series(x)

def _at(x_series, i: int):
    return x_series.iloc[i] if hasattr(x_series, "iloc") else x_series[i]


def _at_many(x_series, indices: list[int]):
    if hasattr(x_series, "iloc"):
        return x_series.iloc[indices]
    return [x_series[i] for i in indices]

def _step_line(x_series, index: int) -> dict:
    xv = _at(x_series, index)
    return dict(
        type="line",
        xref="x",
        yref="paper",
        x0=xv,
        x1=xv,
        y0=0,
        y1=1,
        line=dict(color=BAND_FILL, width=2),
        layer="below",
    )

def _wide_band(x_series, start_idx: int, end_idx: int) -> dict:
    return dict(
        type="rect",
        xref="x",
        yref="paper",
        x0=_at(x_series, start_idx),
        x1=_at(x_series, end_idx),
        y0=0,
        y1=1,
        fillcolor=BAND_FILL,
        opacity=BAND_OPACITY,
        line=dict(width=0),
        layer="below",
    )

import datetime

def sanitize(obj):
    if obj is None:
        return None
    if isinstance(obj, dict):
        return {k: sanitize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [sanitize(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return sanitize(obj.tolist())
    if isinstance(obj, (pd.Timestamp, datetime.datetime, datetime.date)):
        if pd.isna(obj):
            return None
        return obj.isoformat()
    if obj is pd.NaT:
        return None
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, (float, np.floating)):
        f = float(obj)
        if math.isnan(f) or math.isinf(f):
            return None
        return f
    return obj