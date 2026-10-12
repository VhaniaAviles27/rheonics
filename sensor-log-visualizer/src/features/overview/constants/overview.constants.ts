export type OverviewMetricKey =
  | "totalReports"
  | "latestReportName"
  | "latestReportAt"
  | "totalSize";

export interface OverviewMetric {
  key: OverviewMetricKey;
  label: string;
  description: string;
}

export const OVERVIEW_METRICS: OverviewMetric[] = [
  {
    key: "totalReports",
    label: "Reports generated",
    description: "Total CSV files produced by the pipeline.",
  },
  {
    key: "latestReportName",
    label: "Latest report",
    description: "Most recently generated CSV file.",
  },
  {
    key: "latestReportAt",
    label: "Generated at",
    description: "Date and time of the latest report.",
  },
  {
    key: "totalSize",
    label: "Total storage",
    description: "Combined size of all reports.",
  },
];

export const OVERVIEW_METRIC_ORDER: OverviewMetricKey[] = [
  "totalReports",
  "latestReportName",
  "latestReportAt",
  "totalSize",
];