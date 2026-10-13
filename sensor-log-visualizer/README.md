# Sensor Log Visualizer

Desktop application (Tauri + React + TypeScript) for analyzing Rheonics
sensor logs end to end: import `.LOG` files, review the parsed records,
inspect generated reports, and explore interactive measurement plots.

The heavy lifting (parsing, validation, plotting) is delegated to the
Python engine in `../sensor-log-processor`, invoked from the Rust backend.

## Features

### Log analysis
- Pick a `SAMPLE-A.LOG` or `SAMPLE-P.LOG` file from disk.
- Detects the log type from the file name and forwards it to the Python
  engine (`process_log`).
- Shows the number of total / valid / invalid records and the log type.

### Reports
- Lists every CSV produced by the engine under the configured output folder.
- Shows file name, generation timestamp, and size.
- Previews the first 100 rows of any CSV inline.

### Overview
- Dashboard-style summary of the workspace: total reports, latest report,
  last generation time, total storage used.

### Graphs
- Interactive Plotly viewer for the 37 plots defined by the Python engine.
- Sample picker (SAMPLE-A / SAMPLE-P) and plot catalog grouped by category.
- `line` / `scatter` toggle without re-running the engine.
- Series are auto-split by sensor serial (A-LOG) or channel (P-LOG).

## Tech Stack

| Layer | Technology |
|---|---|
| Shell | Tauri 2 |
| Backend | Rust |
| Frontend | React 19 + TypeScript + Vite |
| UI | Mantine 7 + Tabler Icons |
| Charts (legacy) | Recharts |
| Charts (catalog plots) | Plotly.js via `react-plotly.js` |
| Engine | Python 3.10+ (`pandas`, `plotly`) |

## Project Structure

```text
sensor-log-visualizer/
├── src/
│   ├── components/
│   │   ├── layout/          # AppLayout, sidebar, page info
│   │   └── ui/              # MetricCard, EmptyState, ...
│   ├── features/
│   │   ├── log-analysis/    # log upload + analysis state
│   │   ├── reports/         # CSV list + preview
│   │   ├── overview/        # workspace summary
│   │   └── plots/           # Plotly catalog viewer
│   ├── lib/                 # shared formatters, plotly factory
│   ├── App.tsx
│   └── main.tsx
└── src-tauri/
    ├── src/
    │   ├── commands/
    │   │   ├── reports.rs   # list_reports, read_report
    │   │   └── plots.rs     # list_plots, plot_log
    │   └── lib.rs           # process_log + handler registration
    └── tauri.conf.json