import { invoke } from "@tauri-apps/api/core";
import { LogAnalysisResult } from "../types/log-analysis.types";

export async function analyzeLog(
  inputPath: string,
): Promise<LogAnalysisResult> {
  const fileName = inputPath.split(/[\\/]/).pop() ?? "";
  const normalizedName = fileName.toUpperCase();

  let logType: string;
  if (normalizedName.includes("SAMPLE-A") || normalizedName.includes("A-LOG")) {
    logType = "A-LOG";
  } else if (
    normalizedName.includes("SAMPLE-P") ||
    normalizedName.includes("P-LOG")
  ) {
    logType = "P-LOG";
  } else {
    throw new Error(
      "No se pudo identificar el tipo de log por el nombre. " +
        "Usa un archivo cuyo nombre identifique A-LOG o P-LOG.",
    );
  }

  return invoke<LogAnalysisResult>("process_log", {
    path: inputPath, 
    logType,
  });
}