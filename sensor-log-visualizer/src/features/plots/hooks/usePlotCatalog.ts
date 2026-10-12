import { useEffect, useState } from "react";
import { listPlots } from "../services/plots.service";
import type { PlotCatalogEntry, SampleType } from "../types/plots.types";

export function usePlotCatalog(sampleType: SampleType) {
  const [catalog, setCatalog] = useState<PlotCatalogEntry[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setIsLoading(true);
    setError(null);

    listPlots(sampleType)
      .then((items) => {
        if (!cancelled) setCatalog(items);
      })
      .catch((cause) => {
        if (!cancelled) {
          setError(cause instanceof Error ? cause.message : String(cause));
        }
      })
      .finally(() => {
        if (!cancelled) setIsLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [sampleType]);

  return { catalog, isLoading, error };
}