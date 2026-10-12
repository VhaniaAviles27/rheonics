import { invoke } from "@tauri-apps/api/core";
import type {
  ChartType,
  PlotCatalogEntry,
  PlotlyFigure,
  SampleType,
} from "../types/plots.types";

export function listPlots(sampleType?: SampleType): Promise<PlotCatalogEntry[]> {
  return invoke<PlotCatalogEntry[]>("list_plots", {
    sampleType: sampleType ?? null,
  });
}

export function plotLog(
  csvPath: string,
  plotId: string,
  chartType: ChartType,
): Promise<PlotlyFigure> {
  return invoke<PlotlyFigure>("plot_log", {
    csvPath,
    plotId,
    chartType,
  });
}