# Sensor Log Processor

Python engine that parses Rheonics `A-LOG` / `P-LOG` files, validates their
records, exports them as CSV, and renders interactive Plotly figures for the
desktop visualizer.

## Features

### Parsing & validation
- Parses A-LOG files containing timestamps, sensor identification fields, and tagged measurements.
- Parses P-LOG files containing semicolon-separated measurement blocks.
- Converts input records into structured pandas DataFrames.
- Preserves the original line number and source filename for traceability.
- Handles malformed or incomplete records without stopping the entire import.
- Records data-quality issues using `description_error` and `is_valid`.
- Exports processed records to CSV files under `data/output/`.

### Plotting
- Catalog of 37 predefined plots covering thermal, frequency, fluid, electrical,
  phase, signal, model and diagnostic metrics across both sample types.
- Renders Plotly figures (JSON) with `line` or `scatter` modes.
- For A-LOG, series are automatically split per `sensor_serial`.
- For P-LOG, plots expose the `primary` / `secondary` channel pair.

## Requirements

- Python 3.10 or later
- Dependencies listed in `requirements.txt` (`pandas`, `plotly`)

## Project Structure

```text
sensor-log-processor/
├── data/
│   ├── input/
│   │   ├── SAMPLE-A.LOG
│   │   └── SAMPLE-P.LOG
│   └── output/
│       ├── SAMPLE-A.CSV
│       └── SAMPLE-P.CSV
├── src/
│   ├── constants/
│   │   ├── a_log_constants.py
│   │   └── p_log_constants.py
│   ├── parsers/
│   │   ├── a_log_parser.py
│   │   └── p_log_parser.py
│   ├── utils/
│   │   └── log_parser_util.py
│   ├── validation/
│   │   └── log_validation.py
│   ├── plotting/
│   │   ├── __init__.py
│   │   ├── catalog.py     # 37 plot definitions
│   │   ├── renderer.py    # builds Plotly figures
│   │   └── service.py     # public API: plot_log(), list_plots()
│   ├── service/
│   │   └── log_processing.py
│   └── main.py
├── requirements.txt
└── README.md