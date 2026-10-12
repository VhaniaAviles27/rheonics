export interface CsvPreview {
  header: string[];
  rows: string[][];
  total: number;
}

const PREVIEW_ROW_LIMIT = 100;

export function parseCsvPreview(content: string): CsvPreview {
  const lines = content.split(/\r?\n/).filter((l) => l.length > 0);
  const header = lines[0]?.split(",").map((c) => c.trim()) ?? [];
  const rows = lines
    .slice(1, PREVIEW_ROW_LIMIT + 1)
    .map((line) => line.split(","));

  return { header, rows, total: Math.max(0, lines.length - 1) };
}