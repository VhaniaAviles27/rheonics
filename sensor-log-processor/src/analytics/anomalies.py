import numpy as np


def find_spikes(y: np.ndarray, fitted: np.ndarray, z_threshold: float = 4.0) -> list[dict]:
    residual = y - fitted
    mask = np.isfinite(residual)
    if mask.sum() < 5:
        return []

    med = np.nanmedian(residual)
    mad = np.nanmedian(np.abs(residual - med))
    scale = 1.4826 * mad
    if scale < 1e-12:
        return []

    spikes = []
    for i in np.where(mask)[0]:
        z = abs(residual[i] - med) / scale
        if z > z_threshold:
            spikes.append({
                "index": int(i),
                "value": float(y[i]),
                "expected": float(fitted[i]) if np.isfinite(fitted[i]) else None,
                "residual": float(residual[i]),
                "z_score": float(z),
            })
    return spikes


def find_steps(y: np.ndarray, threshold_factor: float = 6.0) -> list[dict]:
    mask = np.isfinite(y)
    if mask.sum() < 10:
        return []

    diffs = np.diff(y)
    finite_diffs = np.abs(diffs[np.isfinite(diffs)])
    if len(finite_diffs) == 0:
        return []

    med_diff = float(np.median(finite_diffs))
    mad_diff = float(np.median(np.abs(finite_diffs - med_diff)))
    scale = 1.4826 * mad_diff
    if scale <= 0:
        scale = float(np.std(finite_diffs))

    threshold = threshold_factor * scale
    if threshold <= 0:
        return []

    steps = []
    for i, d in enumerate(diffs):
        if np.isfinite(d) and abs(d) > threshold:
            steps.append({
                "index": int(i),
                "delta": float(d),
                "magnitude": float(abs(d)),
            })
    return steps


def find_gaps(t: np.ndarray, tolerance: float = 2.0) -> list[dict]:
    if len(t) < 3:
        return []

    diffs = np.diff(t)
    finite = diffs[np.isfinite(diffs)]
    if len(finite) == 0:
        return []

    expected = float(np.median(finite))
    threshold = expected * tolerance

    gaps = []
    for i, d in enumerate(diffs):
        if not np.isfinite(d):
            gaps.append({
                "start_index": i,
                "end_index": i + 1,
                "kind": "invalid_timestamp",
            })
        elif d > threshold:
            gaps.append({
                "start_index": i,
                "end_index": i + 1,
                "kind": "record_gap",
                "duration": float(d),
                "missing_estimate": int(round(d / expected) - 1),
            })
    return gaps


def find_nan_runs(y: np.ndarray) -> list[dict]:
    """Runs consecutivos de valores vacíos en una columna."""
    mask = ~np.isfinite(y)
    runs: list[dict] = []
    start = None

    for i, m in enumerate(mask):
        if m and start is None:
            start = i
        elif not m and start is not None:
            runs.append({"start_index": start, "end_index": i - 1, "length": i - start})
            start = None

    if start is not None:
        runs.append({
            "start_index": start,
            "end_index": len(y) - 1,
            "length": len(y) - start,
        })
    return runs