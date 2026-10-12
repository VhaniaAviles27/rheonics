import { useCallback, useEffect, useState } from "react";
import { listReports, readReport } from "../service/report.service";
import type { ReportFile } from "../types/report.types";

export function useReports() {
  const [reports, setReports] = useState<ReportFile[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [preview, setPreview] = useState<{ path: string; content: string } | null>(null);

  const refresh = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const items = await listReports();
      setReports(items);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : String(cause));
    } finally {
      setIsLoading(false);
    }
  }, []);

  const openPreview = useCallback(async (path: string) => {
    try {
      const content = await readReport(path);
      setPreview({ path, content });
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : String(cause));
    }
  }, []);

  const closePreview = useCallback(() => setPreview(null), []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  return {
    reports,
    isLoading,
    error,
    preview,
    refresh,
    openPreview,
    closePreview,
  };
}