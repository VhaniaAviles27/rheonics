import pytest

from src.plotting.catalog import list_plots, get_plot, CATALOG


def test_catalog_has_expected_size():
    assert len(CATALOG) == 37


def test_list_plots_returns_serializable_dicts():
    items = list_plots()

    assert len(items) == 37
    first = items[0]
    assert set(first.keys()) == {"id", "label", "category", "sampleType", "yLabel", "unit"}


def test_list_plots_filters_by_sample_type():
    a_plots = list_plots("A-LOG")
    p_plots = list_plots("P-LOG")

    assert all(p["sampleType"] == "A-LOG" for p in a_plots)
    assert all(p["sampleType"] == "P-LOG" for p in p_plots)
    assert len(a_plots) + len(p_plots) == 37


def test_get_plot_returns_definition():
    definition = get_plot("a.temperature")

    assert definition.sample_type == "A-LOG"
    assert definition.y_columns[0][0] == "temperature"


def test_get_plot_raises_on_unknown_id():
    with pytest.raises(KeyError):
        get_plot("does.not.exist")