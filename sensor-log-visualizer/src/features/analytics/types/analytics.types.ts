export type TrendMethod = "linear" | "sine" | "stl" | "none";

export interface TrendResult {
  method: TrendMethod;
  fitted: number[] | null;
  r2?: number;
  slope?: number;
  intercept?: number;
  amplitude?: number;
  frequency?: number;
  period?: number;
  offset?: number;
  aic?: number;
  reason?: string;
}

export interface OffsetAnomaly {
  index: number;
  delta: number;
  z_score: number;
}

export interface SpikeAnomaly {
  index: number;
  value: number;
  expected: number | null;
  residual: number;
  z_score: number;
}

export interface GapAnomaly {
  start_index: number;
  end_index: number;
  kind: "record_gap" | "invalid_timestamp";
  duration?: number;
  missing_estimate?: number;
}

export interface NanRunAnomaly {
  start_index: number;
  end_index: number;
  length: number;
}

export interface StepAnomaly {
  index: number;
  delta: number;
  magnitude: number;
}

export interface AnalyticsResult {
  trend: TrendResult;
  anomalies: {
    offsets: OffsetAnomaly[];   
    spikes: SpikeAnomaly[];
    steps: StepAnomaly[];      
    gaps: GapAnomaly[];
    nan_runs: NanRunAnomaly[];
  };
}