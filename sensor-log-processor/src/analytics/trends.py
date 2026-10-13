import numpy as np


def linear_trend(x: np.ndarray, y: np.ndarray) -> dict:
    """
    Regresión lineal por mínimos cuadrados ordinarios (OLS).
    Devuelve slope, intercept, r2 y el array ajustado.
    """
    mask = np.isfinite(x) & np.isfinite(y)
    x_clean = x[mask].astype(float)
    y_clean = y[mask].astype(float)

    if len(x_clean) < 3:
        return {"method": "linear", "fitted": None, "reason": "not_enough_points"}

    x_mean = x_clean.mean()
    y_mean = y_clean.mean()
    num = np.sum((x_clean - x_mean) * (y_clean - y_mean))
    den = np.sum((x_clean - x_mean) ** 2)

    if den == 0:
        return {"method": "linear", "fitted": None, "reason": "constant_x"}

    slope = num / den
    intercept = y_mean - slope * x_mean

    y_hat = slope * x_clean + intercept
    ss_res = np.sum((y_clean - y_hat) ** 2)
    ss_tot = np.sum((y_clean - y_mean) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0

    fitted = np.full_like(y, np.nan, dtype=float)
    fitted[mask] = y_hat

    return {
        "method": "linear",
        "slope": float(slope),
        "intercept": float(intercept),
        "r2": float(r2),
        "fitted": fitted.tolist(),
    }