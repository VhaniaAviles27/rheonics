use serde_json::Value;
use std::path::PathBuf;
use std::process::Command;

#[tauri::command]
fn process_log(path: String, log_type: String) -> Result<Value, String> {
    if log_type != "A-LOG" && log_type != "P-LOG" {
        return Err(format!("Tipo de log no soportado: {log_type}"));
    }

    let processor_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../../sensor-log-processor")
        .canonicalize()
        .map_err(|e| format!("No se encontró sensor-log-processor: {e}"))?;

    let output = Command::new("python")
        .args([
            "-c",
            "import json, sys; from src.service.log_processing import process_log; print(json.dumps(process_log(sys.argv[1], sys.argv[2]), ensure_ascii=False))",
            &path,
            &log_type,
        ])
        .current_dir(&processor_dir)
        .output()
        .map_err(|e| format!("No se pudo ejecutar Python: {e}"))?;

    if !output.status.success() {
        return Err(format!(
            "Error al procesar el log:\n{}",
            String::from_utf8_lossy(&output.stderr)
        ));
    }

    serde_json::from_slice(&output.stdout)
        .map_err(|e| format!("Python no devolvió JSON válido: {e}"))
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .plugin(tauri_plugin_dialog::init())
        .invoke_handler(tauri::generate_handler![process_log])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
