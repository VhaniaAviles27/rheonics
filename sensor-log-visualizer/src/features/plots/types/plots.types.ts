export type SampleType = "A-LOG" | "P-LOG";
export type ChartType = "line" | "scatter";
export type { ReportFile } from "../../reports/types/report.types";

export interface PlotCatalogEntry {
  id: string;
  label: string;
  category: string;
  sampleType: SampleType;
  yLabel: string;
  unit: string | null;
}

export interface PlotlyFigure {
  data: unknown[];
  layout: Record<string, unknown>;
}