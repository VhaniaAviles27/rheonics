use serde::Serialize;
use std::fs;
use std::path::PathBuf;
use std::time::SystemTime;
use tauri::{AppHandle, Manager};

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct ReportFile {
    pub name: String,
    pub path: String,
    pub size_bytes: u64,
    pub modified_at: u64, 
}

fn reports_dir(_app: &AppHandle) -> Result<PathBuf, String> {
    Ok(PathBuf::from(r"C:\Users\Vannia\Desktop\Vhania\Rheonics\Rheonics\rheonics\sensor-log-processor\data\output"))
}

#[tauri::command]
pub fn list_reports(app: AppHandle) -> Result<Vec<ReportFile>, String> {
    let dir = reports_dir(&app)?;

    if !dir.exists() {
        return Ok(vec![]);
    }

    let mut items = Vec::new();

    for entry in fs::read_dir(&dir).map_err(|e| e.to_string())? {
        let entry = entry.map_err(|e| e.to_string())?;
        let path = entry.path();

        let is_csv = path
            .extension()
            .and_then(|s| s.to_str())
            .map(|s| s.eq_ignore_ascii_case("csv"))
            .unwrap_or(false);

        if !is_csv {
            continue;
        }

        let meta = entry.metadata().map_err(|e| e.to_string())?;
        let modified = meta.modified().unwrap_or(SystemTime::UNIX_EPOCH);
        let millis = modified
            .duration_since(SystemTime::UNIX_EPOCH)
            .map(|d| d.as_millis() as u64)
            .unwrap_or(0);

        items.push(ReportFile {
            name: path
                .file_name()
                .map(|n| n.to_string_lossy().into_owned())
                .unwrap_or_default(),
            path: path.to_string_lossy().into_owned(),
            size_bytes: meta.len(),
            modified_at: millis,
        });
    }
    items.sort_by(|a, b| b.modified_at.cmp(&a.modified_at));
    Ok(items)
}

#[tauri::command]
pub fn read_report(path: String, max_bytes: Option<u64>) -> Result<String, String> {
    let limit = max_bytes.unwrap_or(2_000_000) as usize; // 2MB por defecto
    let bytes = fs::read(&path).map_err(|e| e.to_string())?;

    let slice = if bytes.len() > limit {
        &bytes[..limit]
    } else {
        &bytes[..]
    };

    String::from_utf8(slice.to_vec()).map_err(|e| e.to_string())
}