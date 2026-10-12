PARAMETERS = {
    0: "viscosity_median_5_measurements",
    1: "density_median_5_measurements",
    2: "temperature_median_5_measurements",
    3: "kinematic_viscosity",
    4: "density_average_5_measurements",
    5: "viscosity_raw",
    6: "density_raw",
    7: "temperature_raw",
    8: "resonant_frequency",
    9: "compensated_resonant_frequency",
    10: "damping",
    11: "coil_temperature",
    12: "viscosity_median_last_good",
    13: "density_median_last_good",
    14: "modbus_register_512",
    15: "modbus_register_514",
    16: "modbus_register_516",
    17: "estimated_temperature",
    18: "pt1000_temperature",
    19: "calculated_viscosity_model_parameter",
    20: "calculated_density_model_parameter",
    21: "calculated_concentration_model_parameter",
    22: "sensor_cleanliness_ratio",
}
FIELDS_PER_PARAMETER = ("primary", "secondary", "status1", "status2")
PARAMETER_FIELD_COUNT = len(PARAMETERS) * len(FIELDS_PER_PARAMETER)
EXPECTED_FIELD_COUNT = 1 + PARAMETER_FIELD_COUNT + 2 