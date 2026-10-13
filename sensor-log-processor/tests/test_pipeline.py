import json
import numpy as np

from src.analytics.pipeline import analyze_series


def test_analyze_series_returns_expected_keys(linear_series):
    x, y = linear_series

    result = analyze_series(x, y)

    assert "trend" in result
    assert "anomalies" in result
    for key in ("spikes", "steps", "gaps", "nan_runs"):
        assert key in result["anomalies"]


def test_analyze_series_is_json_serializable(linear_series):
    x, y = linear_series
    y = y.copy()
    y[10] = np.nan  # forzar NaN en la salida

    result = analyze_series(x, y)

    # allow_nan=False lanza si queda algún NaN
    json.dumps(result, allow_nan=False)


def test_analyze_series_converts_nan_to_none():
    x = np.array([0.0, 1.0, 2.0, 3.0])
    y = np.array([1.0, np.nan, 5.0, 7.0])

    result = analyze_series(x, y)

    # fitted[1] debe ser None (no NaN) tras sanitize
    assert result["trend"]["fitted"][1] is None