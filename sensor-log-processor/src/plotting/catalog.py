from dataclasses import dataclass
from typing import Literal

SampleType = Literal["A-LOG", "P-LOG"]
ChartType = Literal["line", "scatter"]


@dataclass(frozen=True)
class PlotDefinition:
    id: str
    label: str
    category: str
    sample_type: SampleType
    y_columns: list[tuple[str, str]]
    y_label: str
    unit: str | None = None


_A_PLOTS: list[PlotDefinition] = [
    PlotDefinition("a.temperature", "Temperature", "Thermal", "A-LOG",
                   [("temperature", "Temperature")], "Temperature", "°C"),
    PlotDefinition("a.resonant_frequency", "Resonant frequency", "Frequency", "A-LOG",
                   [("resonant_frequency", "Resonant frequency")], "Frequency", "Hz"),
    PlotDefinition("a.compensated_frequency", "Compensated frequency", "Frequency", "A-LOG",
                   [("compensated_frequency", "Compensated frequency")], "Frequency", "Hz"),
    PlotDefinition("a.reference_frequency", "Reference frequency", "Frequency", "A-LOG",
                   [("reference_frequency", "Reference frequency")], "Frequency", "Hz"),
    PlotDefinition("a.vco_frequency", "VCO frequency", "Frequency", "A-LOG",
                   [("vco_frequency", "VCO frequency")], "Frequency", "Hz"),
    PlotDefinition("a.damping", "Damping", "Signal", "A-LOG",
                   [("damping", "Damping")], "Damping", None),
    PlotDefinition("a.df_ratio", "DF ratio", "Signal", "A-LOG",
                   [("df_ratio", "DF ratio")], "DF ratio", None),
    PlotDefinition("a.viscosity_estimate", "Viscosity estimate", "Fluid", "A-LOG",
                   [("viscosity_estimate", "Viscosity")], "Viscosity", "cP"),
    PlotDefinition("a.density_estimate", "Density estimate", "Fluid", "A-LOG",
                   [("density_estimate", "Density")], "Density", "g/cm³"),
    PlotDefinition("a.pressure_input", "Pressure input", "Process", "A-LOG",
                   [("pressure_input", "Pressure")], "Pressure", None),
    PlotDefinition("a.excitation_current_negative", "Excitation current (neg)", "Electrical", "A-LOG",
                   [("excitation_current_negative", "I-")], "Current", None),
    PlotDefinition("a.excitation_current_positive", "Excitation current (pos)", "Electrical", "A-LOG",
                   [("excitation_current_positive", "I+")], "Current", None),
    PlotDefinition("a.negative_phase_slope", "Negative phase slope", "Phase", "A-LOG",
                   [("negative_phase_slope", "Negative slope")], "Phase slope", None),
    PlotDefinition("a.positive_phase_slope", "Positive phase slope", "Phase", "A-LOG",
                   [("positive_phase_slope", "Positive slope")], "Phase slope", None),
    PlotDefinition("a.coil_temperature", "Coil temperature", "Thermal", "A-LOG",
                   [("coil_temperature", "Coil temperature")], "Temperature", "°C"),
    PlotDefinition("a.pt1000_temperature", "PT1000 temperature", "Thermal", "A-LOG",
                   [("pt1000_temperature", "PT1000")], "Temperature", "°C"),
    PlotDefinition("a.estimated_internal_temperature", "Estimated internal temperature", "Thermal", "A-LOG",
                   [("estimated_internal_temperature", "Estimated internal")], "Temperature", "°C"),
    PlotDefinition("a.measurement_age", "Measurement age", "Diagnostics", "A-LOG",
                   [("measurement_age", "Measurement age")], "Age", None),
]

def _p_pair(col_base: str, label: str, category: str, y_label: str, unit: str | None = None) -> PlotDefinition:
    return PlotDefinition(
        id=f"p.{col_base}",
        label=label,
        category=category,
        sample_type="P-LOG",
        y_columns=[
            (f"{col_base}_primary", "Primary"),
            (f"{col_base}_secondary", "Secondary"),
        ],
        y_label=y_label,
        unit=unit,
    )


_P_PLOTS: list[PlotDefinition] = [
    _p_pair("viscosity_median_5_measurements", "Viscosity (median of 5)", "Fluid", "Viscosity", "cP"),
    _p_pair("density_median_5_measurements", "Density (median of 5)", "Fluid", "Density", "g/cm³"),
    _p_pair("temperature_median_5_measurements", "Temperature (median of 5)", "Thermal", "Temperature", "°C"),
    _p_pair("kinematic_viscosity", "Kinematic viscosity", "Fluid", "Kinematic viscosity", "cSt"),
    _p_pair("density_average_5_measurements", "Density (average of 5)", "Fluid", "Density", "g/cm³"),
    _p_pair("viscosity_raw", "Viscosity (raw)", "Fluid", "Viscosity", "cP"),
    _p_pair("density_raw", "Density (raw)", "Fluid", "Density", "g/cm³"),
    _p_pair("temperature_raw", "Temperature (raw)", "Thermal", "Temperature", "°C"),
    _p_pair("resonant_frequency", "Resonant frequency", "Frequency", "Frequency", "Hz"),
    _p_pair("compensated_resonant_frequency", "Compensated resonant frequency", "Frequency", "Frequency", "Hz"),
    _p_pair("damping", "Damping", "Signal", "Damping"),
    _p_pair("coil_temperature", "Coil temperature", "Thermal", "Temperature", "°C"),
    _p_pair("estimated_temperature", "Estimated temperature", "Thermal", "Temperature", "°C"),
    _p_pair("pt1000_temperature", "PT1000 temperature", "Thermal", "Temperature", "°C"),
    _p_pair("calculated_viscosity_model_parameter", "Viscosity model parameter", "Model", "Parameter"),
    _p_pair("calculated_density_model_parameter", "Density model parameter", "Model", "Parameter"),
    _p_pair("calculated_concentration_model_parameter", "Concentration model parameter", "Model", "Parameter"),
    _p_pair("sensor_cleanliness_ratio", "Sensor cleanliness ratio", "Diagnostics", "Ratio"),
    PlotDefinition("p.pressure", "Pressure", "Process", "P-LOG",
                   [("pressure", "Pressure")], "Pressure", None),
]


CATALOG: list[PlotDefinition] = _A_PLOTS + _P_PLOTS
CATALOG_BY_ID: dict[str, PlotDefinition] = {p.id: p for p in CATALOG}


def list_plots(sample_type: SampleType | None = None) -> list[dict]:
    """Devuelve el catálogo serializable para el frontend."""
    items = CATALOG if sample_type is None else [p for p in CATALOG if p.sample_type == sample_type]
    return [
        {
            "id": p.id,
            "label": p.label,
            "category": p.category,
            "sampleType": p.sample_type,
            "yLabel": p.y_label,
            "unit": p.unit,
        }
        for p in items
    ]


def get_plot(plot_id: str) -> PlotDefinition:
    if plot_id not in CATALOG_BY_ID:
        raise KeyError(f"Plot desconocido: {plot_id}")
    return CATALOG_BY_ID[plot_id]