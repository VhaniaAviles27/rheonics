import { invoke } from "@tauri-apps/api/core";
import type { AnalyticsResult } from "../types/analytics.types";

export function analyzeLog(
  csvPath: string,
  plotId: string,
  sensorSerial?: string | null,
): Promise<AnalyticsResult> {
  return invoke<AnalyticsResult>("analyze_log", {
    csvPath,
    plotId,
    sensorSerial: sensorSerial ?? null,
  });
}