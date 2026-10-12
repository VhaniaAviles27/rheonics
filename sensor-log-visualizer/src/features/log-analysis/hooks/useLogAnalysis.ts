import { useState } from "react";
import type { LogAnalysisResult } from "../types/log-analysis.types";
import { analyzeLog } from "../services/log-analysis.service";

export function useLogAnalysis() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<LogAnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function runAnalysis(inputPath: string) {
    setIsAnalyzing(true);
    setResult(null);
    setError(null);

    try {
      const analysisResult = await analyzeLog(inputPath);
      setResult(analysisResult);
    } catch (cause) {
      setError(
        cause instanceof Error
          ? cause.message
          : String(cause),
      );
    } finally {
      setIsAnalyzing(false);
    }
  }

  return {
    isAnalyzing,
    result,
    error,
    runAnalysis,
  };
}
