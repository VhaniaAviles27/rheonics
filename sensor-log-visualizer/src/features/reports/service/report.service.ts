import { invoke } from "@tauri-apps/api/core";
import { ReportFile } from "../types/report.types";

export function listReports(): Promise<ReportFile[]> {
  return invoke<ReportFile[]>("list_reports");
}

export function readReport(path: string): Promise<string> {
  return invoke<string>("read_report", { path });
}