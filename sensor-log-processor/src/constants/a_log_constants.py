import re

TIMESTAMP_RE = re.compile(r"^\s*(?P<timestamp>\d+)\s*:\s*(?P<body>.*)$")
HEADER_RE = re.compile(r'^\s*"(?P<header>[^"]*)"\s*(?P<measurements>.*)$')

TAG_DEFINITIONS = {
    "T": {
        "name": "temperature",
        "description": "Temperature",
        "data_type": "float",
        "unit": "°C",
    },
    "f": {
        "name": "resonant_frequency",
        "description": "Resonant frequency",
        "data_type": "float",
        "unit": "Hz",
    },
    "df": {
        "name": "damping",
        "description": "Damping",
        "data_type": "float",
        "unit": "Hz",
    },
    "Fv": {
        "name": "vco_frequency",
        "description": "VCO frequency",
        "data_type": "float",
        "unit": None,
    },
    "ph": {
        "name": "resonator_phase_preset",
        "description": "Resonator phase preset",
        "data_type": "float",
        "unit": None,
    },
    "V": {
        "name": "viscosity_estimate",
        "description": "Viscosity estimate (median of 5 measurements)",
        "data_type": "float",
        "unit": None,
    },
    "D": {
        "name": "density_estimate",
        "description": "Density estimate",
        "data_type": "float",
        "unit": None,
    },
    "P": {
        "name": "pressure_input",
        "description": "Pressure input",
        "data_type": "float",
        "unit": None,
    },
    "fc": {
        "name": "compensated_frequency",
        "description": "Compensated frequency",
        "data_type": "float",
        "unit": None,
    },
    "I-": {
        "name": "excitation_current_negative",
        "description": "Excitation current negative",
        "data_type": "float",
        "unit": None,
    },
    "I+": {
        "name": "excitation_current_positive",
        "description": "Excitation current positive",
        "data_type": "float",
        "unit": None,
    },
    "Q": {
        "name": "df_ratio",
        "description": "Ratio df-/df+",
        "data_type": "float",
        "unit": None,
    },
    "fr": {
        "name": "reference_frequency",
        "description": "Reference frequency",
        "data_type": "float",
        "unit": None,
    },
    "df-": {
        "name": "negative_phase_slope",
        "description": "Negative phase slope",
        "data_type": "float",
        "unit": None,
    },
    "df+": {
        "name": "positive_phase_slope",
        "description": "Positive phase slope",
        "data_type": "float",
        "unit": None,
    },
    "Tc": {
        "name": "coil_temperature",
        "description": "Coil temperature",
        "data_type": "float",
        "unit": None,
    },
    "Tp": {
        "name": "pt1000_temperature",
        "description": "PT1000 temperature",
        "data_type": "float",
        "unit": None,
    },
    "Te": {
        "name": "estimated_internal_temperature",
        "description": "Estimated internal temperature",
        "data_type": "float",
        "unit": None,
    },
    "E": {
        "name": "error_code",
        "description": "Error code",
        "data_type": "string",
        "unit": None,
    },
    "A": {
        "name": "measurement_age",
        "description": "Age of the measurement string",
        "data_type": "string",
        "unit": None,
    },
}

KNOWN_TAGS = set(TAG_DEFINITIONS)

NUMERIC_TAGS = {
    tag
    for tag, definition in TAG_DEFINITIONS.items()
    if definition["data_type"] == "float"
}

STRING_TAGS = {
    tag
    for tag, definition in TAG_DEFINITIONS.items()
    if definition["data_type"] == "string"
}