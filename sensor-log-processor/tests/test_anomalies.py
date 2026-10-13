import numpy as np
import pytest

from src.analytics.anomalies import (
    find_spikes,
    find_steps,
    find_gaps,
    find_nan_runs,
)


def test_find_spikes_detects_single_outlier(series_with_spike):
    x, y = series_with_spike
    fitted = 2.0 * x + 3.0  # verdad de base

    spikes = find_spikes(y, fitted, z_threshold=4.0)

    indexes = [s["index"] for s in spikes]
    assert 50 in indexes


def test_find_spikes_none_on_clean_signal(linear_series):
    x, y = linear_series
    fitted = 2.0 * x + 3.0

    spikes = find_spikes(y, fitted, z_threshold=4.0)

    assert len(spikes) == 0


def test_find_steps_detects_level_jump(series_with_step):
    x, y = series_with_step

    steps = find_steps(y, threshold_factor=6.0)

    indexes = [s["index"] for s in steps]
    assert 49 in indexes or 50 in indexes  # el salto ocurre entre 49 y 50


def test_find_gaps_detects_missing_records(series_with_gap):
    t, _ = series_with_gap

    gaps = find_gaps(t, tolerance=2.0)

    assert len(gaps) == 1
    assert gaps[0]["kind"] == "record_gap"
    assert gaps[0]["missing_estimate"] > 100


def test_find_gaps_none_on_regular_timestamps():
    t = np.arange(0, 100, 1.0)

    gaps = find_gaps(t)

    assert gaps == []


def test_find_nan_runs_detects_consecutive_nans():
    y = np.array([1.0, 2.0, np.nan, np.nan, np.nan, 6.0, 7.0])

    runs = find_nan_runs(y)

    assert len(runs) == 1
    assert runs[0]["start_index"] == 2
    assert runs[0]["end_index"] == 4
    assert runs[0]["length"] == 3


def test_find_nan_runs_none_when_all_finite():
    y = np.array([1.0, 2.0, 3.0, 4.0])

    assert find_nan_runs(y) == []