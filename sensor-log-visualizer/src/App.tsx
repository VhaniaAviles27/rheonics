
import { useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import { open } from "@tauri-apps/plugin-dialog";
import "./App.css";

interface LogResult {
  log_type: string;
  file_name: string;
  total_records: number;
  valid_records: number;
  invalid_records: number;
  columns: string[];
  records: Record<string, unknown>[];
}

function App() {
  const [result, setResult] = useState<LogResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSelectFile() {
    const selected = await open({
      multiple: false,
      filters: [
        {
          name: "Archivos de registro",
          extensions: ["LOG", "log"],
        },
      ],
    });

    if (!selected || Array.isArray(selected)) return;

    const fileName = selected.split(/[\\/]/).pop() ?? "";
    const normalizedName = fileName.toUpperCase();

    let logType: string;

    if (normalizedName.includes("SAMPLE-A") ||
        normalizedName.includes("A-LOG")) {
      logType = "A-LOG";
    } else if (
      normalizedName.includes("SAMPLE-P") ||
      normalizedName.includes("P-LOG")
    ) {
      logType = "P-LOG";
    } else {
      setError(
        "No se pudo identificar el tipo de log por el nombre. " +
        "Usa un archivo cuyo nombre identifique A-LOG o P-LOG."
      );
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await invoke<LogResult>("process_log", {
        path: selected,
        logType,
      });

      setResult(response);
    } catch (err) {
      setError(String(err));
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app">
      <header className="app-header">
        <div>
          <p className="eyebrow">RHEONICS · SENSOR LOGS</p>
          <h1>Log Analyzer</h1>
          <p className="subtitle">
            Procesamiento y validación de registros de sensores.
          </p>
        </div>

        <button
          className="primary-button"
          onClick={handleSelectFile}
          disabled={loading}
        >
          {loading ? "Procesando..." : "Seleccionar archivo"}
        </button>
      </header>

      {error && (
        <section className="message error-message" role="alert">
          <strong>No se pudo procesar el archivo</strong>
          <p>{error}</p>
        </section>
      )}

      {loading && (
        <section className="message">
          Procesando el archivo con los parsers de Python...
        </section>
      )}

      {result && (
        <>
          <section className="result-heading">
            <div>
              <p className="eyebrow">ARCHIVO PROCESADO</p>
              <h2>{result.file_name}</h2>
            </div>
            <span className="type-badge">{result.log_type}</span>
          </section>

          <section className="metrics">
            <article className="metric-card">
              <span>Total de registros</span>
              <strong>{result.total_records}</strong>
            </article>
            <article className="metric-card">
              <span>Válidos</span>
              <strong>{result.valid_records}</strong>
            </article>
            <article className="metric-card">
              <span>Inválidos</span>
              <strong>{result.invalid_records}</strong>
            </article>
          </section>

          <section className="table-section">
            <div className="table-heading">
              <h2>Registros</h2>
              <span>{result.records.length} filas</span>
            </div>

            {result.records.length === 0 ? (
              <p className="empty-state">
                El archivo no contiene registros.
              </p>
            ) : (
              <div className="table-wrapper">
                <table>
                  <thead>
                    <tr>
                      {result.columns.map((column) => (
                        <th key={column}>{column}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {result.records.map((record, index) => (
                      <tr key={index}>
                        {result.columns.map((column) => (
                          <td key={column}>
                            {record[column] == null
                              ? "—"
                              : String(record[column])}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </section>
        </>
      )}

      {!result && !loading && !error && (
        <section className="empty-panel">
          <div className="empty-icon">LOG</div>
          <h2>Comienza con un archivo</h2>
          <p>
            Selecciona un A-LOG o P-LOG para consultar sus registros
            y el resultado de la validación.
          </p>
        </section>
      )}
    </main>
  );
}

export default App;
