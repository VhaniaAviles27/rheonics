import type { OverviewMetricKey } from "../constants/overview.constants";
import type { OverviewData } from "../types/overview.types";
import { formatDate, formatSize } from "./formatters";

export function buildMetricValues(
  data: OverviewData,
): Record<OverviewMetricKey, string> {
  return {
    totalReports: data.totalReports > 0 ? String(data.totalReports) : "—",
    latestReportName: data.latestReportName ?? "—",
    latestReportAt: formatDate(data.latestReportAt),
    totalSize: formatSize(data.totalSizeBytes),
  };
}