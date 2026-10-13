import math
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

    result = {
        "trend": trend,
        "anomalies": {
            "spikes": find_spikes(y, fitted),
            "steps": find_steps(y),
            "gaps": find_gaps(x),
            "nan_runs": find_nan_runs(y),
        },
    }
    return _sanitize(result)


def _sanitize(obj):
    if obj is None:
        return None
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_sanitize(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return _sanitize(obj.tolist())
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