import numpy as np

from .trends import linear_trend
from .anomalies import find_spikes, find_steps, find_gaps, find_nan_runs


def analyze_series(x: np.ndarray, y: np.ndarray) -> dict:
    """Trend lineal + detección de anomalías. Todo en un dict serializable."""
    trend = linear_trend(x, y)
    fitted = (
        np.array(trend["fitted"], dtype=float)
        if trend.get("fitted") is not None
        else np.full_like(y, np.nan, dtype=float)
    )

    return {
        "trend": trend,
        "anomalies": {
            "spikes": find_spikes(y, fitted),
            "steps": find_steps(y),
            "gaps": find_gaps(x),
            "nan_runs": find_nan_runs(y),
        },
    }