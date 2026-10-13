from pathlib import Path

import numpy as np
import pandas as pd
import pytest

DATA_INPUT = Path(__file__).parent.parent / "data" / "input"

@pytest.fixture
def linear_series():
    rng = np.random.default_rng(42)
    x = np.arange(100, dtype=float)
    y = 2.0 * x + 3.0 + rng.normal(0, 0.5, size=100)
    return x, y


@pytest.fixture
def series_with_spike(linear_series):
    x, y = linear_series
    y = y.copy()
    y[50] = y[50] + 50
    return x, y


@pytest.fixture
def series_with_step():
    x = np.arange(100, dtype=float)
    y = np.concatenate([np.full(50, 10.0), np.full(50, 20.0)])
    return x, y


@pytest.fixture
def series_with_gap():
    t = np.concatenate([
        np.arange(0, 50, 1.0),
        np.arange(550, 600, 1.0),
    ])
    y = np.sin(t / 10.0)
    return t, y

@pytest.fixture
def sample_a_csv(tmp_path):
    df = pd.DataFrame({
        "source_file": ["SAMPLE-A.LOG"] * 5,
        "timestamp": [1_791_500_000 + i * 45 for i in range(5)],
        "sensor_serial": ["SRD-1"] * 5,
        "temperature": [22.0, 22.1, 22.2, 22.3, 22.4],
        "resonant_frequency": [7423.0, 7425.0, 7424.0, 7426.0, 7423.0],
    })
    path = tmp_path / "SAMPLE-A.CSV"
    df.to_csv(path, index=False)
    return path


@pytest.fixture
def sample_p_csv(tmp_path):
    df = pd.DataFrame({
        "source_file": ["SAMPLE-P.LOG"] * 5,
        "timestamp": [1_791_400_000 + i * 47 for i in range(5)],
        "pressure": [1.05, 1.06, None, 1.08, 1.09],
    })
    path = tmp_path / "SAMPLE-P.CSV"
    df.to_csv(path, index=False)
    return path

@pytest.fixture
def sample_a_path():
    path = DATA_INPUT / "SAMPLE-A.LOG"
    if not path.exists():
        pytest.skip(f"Missing sample: {path}")
    return str(path)


@pytest.fixture
def sample_p_path():
    path = DATA_INPUT / "SAMPLE-P.LOG"
    if not path.exists():
        pytest.skip(f"Missing sample: {path}")
    return str(path)