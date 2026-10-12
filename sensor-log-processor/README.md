# Sensor Log Processor

Python project for parsing and validating Rheonics A-LOG and P-LOG files.

## Features

- Parses A-LOG files containing timestamps, sensor identification fields, and tagged measurements.
- Parses P-LOG files containing semicolon-separated measurement fields.
- Converts the input records into structured pandas DataFrames.
- Preserves the original line number and source filename for traceability.
- Handles malformed or incomplete records without stopping the entire import.
- Records data-quality issues using `description_error` and `is_valid`.
- Exports the processed records to CSV files.

## Requirements

- Python 3.10 or later
- Dependencies listed in `requirements.txt`

## Project Structure

```text
sensor-log-processor/
├── data/
│   ├── input/
│   │   ├── SAMPLE-A.LOG
│   │   └── SAMPLE-P.LOG
│   └── output/
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
│   └── main.py
├── requirements.txt
└── README.md
```

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage

Place the input files in `data/input/` using the filenames expected by the application.

Run the processor from the project root:

```bash
python -m src.main
```

The application parses the input files and exports the resulting CSV files to the configured output directory.

## Validation Fields

Each processed record includes:

| Field | Description |
|---|---|
| `source_file` | Name of the input file |
| `line_number` | Original line number in the input file |
| `timestamp` | Unix timestamp extracted from the record |
| `timestamp_utc` | UTC representation of the timestamp |
| `description_error` | Error descriptions joined into a single text field; empty when no errors are detected |
| `is_valid` | `True` when no validation errors are detected; otherwise, `False` |

Additional columns depend on the log format and its measurement fields.

## A-LOG Format

A-LOG records contain a Unix timestamp, a quoted identification header, and tag-value pairs. The identification header provides the sensor serial, firmware version, and electronics serial.

Known measurement tags are mapped to their corresponding fields. Numeric measurements are parsed as numbers, while string fields such as error codes are preserved as strings.

## P-LOG Format

P-LOG records contain a Unix timestamp followed by 23 parameter blocks. Each parameter block consists of four fields:

- `primary`
- `secondary`
- `status1`
- `status2`

The final fields represent the overall device status and pressure. The expected record length is 95 semicolon-separated fields.

## Data Quality

Malformed timestamps, incomplete records, unknown A-LOG tags, and invalid numeric values can be reported as validation errors.

The parser retains malformed records when possible so they can be reviewed instead of silently discarded.

Validation identifies structural and parsing problems. It does not automatically determine whether every numeric measurement is physically plausible.

## Limitations

- The implementation follows the supplied Sensor Log Parsing Specification.
- The parser does not infer undocumented meanings for status codes.
- Physical plausibility checks and advanced trend analysis are outside the scope of basic parsing.
