import pytest

from src.analytics.service import analyze_log


def test_analyze_log_on_sample_a(sample_a_csv):
    result = analyze_log(str(sample_a_csv), "a.temperature")

    assert result["trend"]["method"] == "linear"
    assert isinstance(result["trend"]["slope"], float)
    assert "anomalies" in result


def test_analyze_log_on_sample_p_with_nan(sample_p_csv):
    result = analyze_log(str(sample_p_csv), "p.pressure")

    assert result["trend"]["method"] == "linear"


def test_analyze_log_rejects_mismatched_sample_type(sample_a_csv):
    with pytest.raises(ValueError, match="El CSV es A-LOG"):
        analyze_log(str(sample_a_csv), "p.pressure")


def test_analyze_log_rejects_missing_file(tmp_path):
    missing = tmp_path / "nope.csv"
    with pytest.raises(FileNotFoundError):
        analyze_log(str(missing), "a.temperature")


def test_analyze_log_rejects_unknown_column(sample_a_csv):
    # forzar un plot cuyo y_column no existe en el CSV
    with pytest.raises(ValueError):
        analyze_log(str(sample_a_csv), "a.damping")