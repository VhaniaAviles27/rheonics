import { useEffect, useState } from "react";
import { plotLog } from "../services/plots.service";
import type { ChartType, PlotlyFigure } from "../types/plots.types";

export function usePlot(
  csvPath: string | null,
  plotId: string | null,
  chartType: ChartType,
) {
  const [figure, setFigure] = useState<PlotlyFigure | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!csvPath || !plotId) {
      setFigure(null);
      setError(null);
      return;
    }

    let cancelled = false;
    setIsLoading(true);
    setError(null);

    plotLog(csvPath, plotId, chartType)
      .then((fig) => {
        if (!cancelled) setFigure(fig);
      })
      .catch((cause) => {
        if (!cancelled) {
          setError(cause instanceof Error ? cause.message : String(cause));
          setFigure(null);
        }
      })
      .finally(() => {
        if (!cancelled) setIsLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [csvPath, plotId, chartType]);

  return { figure, isLoading, error };
}