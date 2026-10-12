use serde_json::Value;
use std::path::PathBuf;
use std::process::Command;

fn processor_dir() -> Result<PathBuf, String> {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../../sensor-log-processor")
        .canonicalize()
        .map_err(|e| format!("No se encontró sensor-log-processor: {e}"))
}

#[tauri::command]
pub fn list_plots(sample_type: Option<String>) -> Result<Value, String> {
    let code = "import json, sys; from src.plotting import list_plots; print(json.dumps(list_plots(sys.argv[1] or None)))";
    let st = sample_type.unwrap_or_default();

    let out = Command::new("python")
        .args(["-c", code, &st])
        .current_dir(processor_dir()?)
        .output()
        .map_err(|e| format!("No se pudo ejecutar Python: {e}"))?;

    if !out.status.success() {
        return Err(String::from_utf8_lossy(&out.stderr).into_owned());
    }
    serde_json::from_slice(&out.stdout).map_err(|e| format!("JSON inválido: {e}"))
}

#[tauri::command]
pub fn plot_log(
    csv_path: String,
    plot_id: String,
    chart_type: String,
) -> Result<Value, String> {
    let code = "import json, sys; from src.plotting import plot_log; print(json.dumps(plot_log(sys.argv[1], sys.argv[2], sys.argv[3])))";

    let out = Command::new("python")
        .args(["-c", code, &csv_path, &plot_id, &chart_type])
        .current_dir(processor_dir()?)
        .output()
        .map_err(|e| format!("No se pudo ejecutar Python: {e}"))?;

    if !out.status.success() {
        return Err(String::from_utf8_lossy(&out.stderr).into_owned());
    }
    serde_json::from_slice(&out.stdout).map_err(|e| format!("JSON inválido: {e}"))
}