# Setup and Dependencies — `sensor-log-processor`

Python engine for processing Rheonics `A-LOG` and `P-LOG` files, validating records, exporting CSV files, and generating figures and analysis data for the desktop visualizer.

## 1. Prerequisites

- **Python 3.10 or later.**
- `pip` and `venv` (usually included with Python).
- A **Bash terminal** (Git Bash or WSL on Windows; Bash on Linux/macOS).
- If integrating with `sensor-log-visualizer`, the Tauri 2/Rust build environment must also be installed in the visualizer project. This is a desktop application dependency, not a dependency of this Python engine.

Check the installed versions:

```bash
python --version
python -m pip --version
```

If `python` is not available in your terminal, try `python3`.

## 2. Create and Activate the Virtual Environment

From the repository root directory:

```bash
cd sensor-log-processor
python -m venv .venv
source .venv/Scripts/activate
```

On Linux/macOS/WSL, use the following command instead:

```bash
source .venv/bin/activate
```

Upgrade `pip`:

```bash
python -m pip install --upgrade pip
```

> On Windows, run the `Scripts` activation command from Git Bash. If the virtual environment was created in WSL, activate it using `source .venv/bin/activate`.

## 3. Install Dependencies

Runtime dependencies declared in `requirements.txt`:

- `pandas>=2.0`: Reading, transforming, and exporting tabular data.
- `plotly>=5.20`: Generating figures that can be serialized for the visualizer.
- `numpy`: Used directly by the analysis and visualization modules. It is usually installed as a dependency of `pandas`, but explicitly declaring it in `requirements.txt` is recommended.

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

To also install the testing dependencies (`pytest`, `pytest-cov`, and `pytest-mock`):

```bash
python -m pip install -r requirements-dev.txt
```

If you want to explicitly declare NumPy, add the following line to `requirements.txt`:

```text
numpy>=1.24
```

## 4. Relevant Project Structure

```text
sensor-log-processor/
├── data/
│   ├── input/                 # Input LOG files
│   └── output/                # Generated CSV files
├── src/
│   ├── constants/             # A-LOG and P-LOG constants
│   ├── parsers/               # Parsers for each format
│   ├── validation/            # Record validation and summaries
│   ├── service/
│   │   └── log_processing.py  # Processing API: process_log()
│   ├── plotting/              # Plotly chart catalog and generation
│   ├── analytics/             # Trend analysis and anomaly detection
│   └── main.py                # Example execution entry point
├── tests/                     # Automated tests
├── requirements.txt
├── requirements-dev.txt
└── pytest.ini
```

## 5. Run the Example Processing Workflow

The main program processes the following files:

- `data/input/SAMPLE-A.LOG`
- `data/input/SAMPLE-P.LOG`

The corresponding CSV files are generated in `data/output/`.

From the project root, with the virtual environment activated, run:

```bash
python -m src.main
```

The program displays the validation summary, the number of records, and the path of each generated CSV file.

To process other files from an integration or script, use the public function available in `src.service.log_processing`:

```python
from src.service.log_processing import process_log

result = process_log("path/to/file.LOG", "A-LOG")
# For P-LOG files, use "P-LOG".
```

The result includes the file type and name, total number of records, valid and invalid record counts, column names, and serializable records.

## 6. Run the Tests

Install the development dependencies and run:

```bash
python -m pytest
```

To generate a test coverage report in the terminal:

```bash
python -m pytest --cov=src --cov-report=term-missing
```

## 7. Integration with `sensor-log-visualizer` (Tauri)

The visualizer and the processor are separate projects. The Rust/Tauri application must invoke Python and point it to this project's directory.

In the existing integration, configure `SENSOR_LOG_PROCESSOR_DIR` with the **absolute path** to the `sensor-log-processor` root directory. For example, in Bash:

```bash
export SENSOR_LOG_PROCESSOR_DIR="/absolute/path/to/sensor-log-processor"
```

The integration can prioritize the Python interpreter from the virtual environment:

- Windows: `.venv/Scripts/python.exe`
- Linux/macOS: `.venv/bin/python`

If the integration executes `desktop_runner.py`, verify that this file exists in the version of the project you are using. It is not listed in the project structure included in this package. Do not assume the integration command will work until you confirm that the runner exists and that the Tauri code points to the correct path.

Keep processed CSV files in `desktop-output` when required by the visualizer. This directory belongs to the desktop integration workflow and is separate from `data/output`, which is used by the example processing workflow.

## 8. Troubleshooting

### `ModuleNotFoundError`

Make sure the virtual environment is activated, then reinstall the dependencies:

```bash
python -m pip install -r requirements.txt
```

### LOG File Not Found

Verify the file path and exact filename. The example program expects `SAMPLE-A.LOG` and `SAMPLE-P.LOG` inside `data/input/`.

### CSV File Not Generated

Run `python -m src.main` from the project root and check the error messages. Make sure `data/input/` contains the example files and that `data/output/` is writable.

### Tests Cannot Find Modules

Run `python -m pytest` from the project root. The `pytest.ini` file configures `pythonpath = .`.

## 9. Dependency Summary

| Package | Purpose | Type |
|---|---|---|
| `pandas>=2.0` | DataFrames, CSV import/export | Runtime |
| `plotly>=5.20` | Interactive figures serialized to JSON | Runtime |
| `numpy` | Numerical calculations and time-series analysis | Recommended direct runtime dependency |
| `pytest>=8.0` | Automated testing | Development |
| `pytest-cov>=5.0` | Test coverage | Development |
| `pytest-mock>=3.12` | Mocking utilities for tests | Development |
