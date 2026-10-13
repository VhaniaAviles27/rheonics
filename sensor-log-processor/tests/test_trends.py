import numpy as np
import pytest

from src.analytics.trends import linear_trend

def test_linear_trend_recovers_slope(linear_series):
    x, y = linear_series
    result = linear_trend(x, y)

    assert result["method"] == "linear"
    assert result["slope"] == pytest.approx(2.0, abs=0.1)
    assert result["intercept"] == pytest.approx(3.0, abs=1.0)
    assert result["r2"] > 0.99

def test_linear_trend_fitted_length_matches_input(linear_series):
    x, y = linear_series
    result = linear_trend(x, y)

    assert len(result["fitted"]) == len(y)

def test_linear_trend_ignores_nan():
    x = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
    y = np.array([1.0, np.nan, 5.0, 7.0, 9.0])  

    result = linear_trend(x, y)

    assert result["slope"] == pytest.approx(2.0, abs=0.01)
    assert result["fitted"][1] is None or np.isnan(result["fitted"][1])

def test_linear_trend_not_enough_points():
    x = np.array([1.0, 2.0])
    y = np.array([1.0, 2.0])

    result = linear_trend(x, y)

    assert result["fitted"] is None
    assert result["reason"] == "not_enough_points"

def test_linear_trend_constant_x():
    x = np.full(10, 5.0)
    y = np.arange(10, dtype=float)

    result = linear_trend(x, y)

    assert result["fitted"] is None
    assert result["reason"] == "constant_x"