import { useEffect, useState } from "react";
import { analyzeLog } from "../services/analytics.service";
import type { AnalyticsResult } from "../types/analytics.types";

export function useAnalytics(
  csvPath: string | null,
  plotId: string | null,
  sensorSerial: string | null,
) {
  const [result, setResult] = useState<AnalyticsResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!csvPath || !plotId) {
      setResult(null);
      return;
    }
    let cancelled = false;
    setIsLoading(true);
    setError(null);

    analyzeLog(csvPath, plotId, sensorSerial)
      .then((r) => { if (!cancelled) setResult(r); })
      .catch((cause) => {
        if (!cancelled) {
          setError(cause instanceof Error ? cause.message : String(cause));
          setResult(null);
        }
      })
      .finally(() => { if (!cancelled) setIsLoading(false); });

    return () => { cancelled = true; };
  }, [csvPath, plotId, sensorSerial]);

  return { result, isLoading, error };
}