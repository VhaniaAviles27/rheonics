import { useCallback, useEffect, useState } from "react";

import type { OverviewData } from "../types/overview.types";
import { listReports } from "../../reports/service/report.service";

const EMPTY: OverviewData = {
  totalReports: 0,
  latestReportName: null,
  latestReportAt: null,
  totalSizeBytes: 0,
};

export function useOverview() {
  const [data, setData] = useState<OverviewData>(EMPTY);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const reports = await listReports();
      const totalSizeBytes = reports.reduce((sum, r) => sum + r.sizeBytes, 0);
      const latest = reports[0] ?? null;

      setData({
        totalReports: reports.length,
        latestReportName: latest?.name ?? null,
        latestReportAt: latest?.modifiedAt ?? null,
        totalSizeBytes,
      });
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : String(cause));
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  return { data, isLoading, error, refresh };
}