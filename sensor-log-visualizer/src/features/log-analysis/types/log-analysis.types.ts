export interface QualityIssue {
  category: "record_status" | "quality_issue";
  name: string;
  count: number;
}

export interface AnalysisReportPaths {
  quality: string;
  numericSummary: string;
  outliers: string;
}

export interface LogAnalysisResult {
  log_type: string;
  file_name: string;
  total_records: number;
  valid_records: number;
  invalid_records: number;
  columns: string[];
  records: Record<string, unknown>[];
}

export interface LogAnalysisState {
  isAnalyzing: boolean;
  result: LogAnalysisResult | null;
  error: string | null;
}
