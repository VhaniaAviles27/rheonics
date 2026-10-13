import { useMemo, useState } from "react";
import {
  Alert,
  Loader,
  Paper,
  Select,
  SimpleGrid,
  Stack,
  Text,
} from "@mantine/core";
import { IconAlertCircle } from "@tabler/icons-react";
import { useAnalytics } from "../hooks/useAnalytics";
import { usePlotCatalog } from "../../plots/hooks/usePlotCatalog";

import type { ReportFile, SampleType } from "../../plots/types/plots.types";

import "../styles/analytics-viewer.css";

interface AnalyticsViewerProps {
  reports: ReportFile[];
}

function detectSampleType(fileName: string): SampleType | null {
  const name = fileName.toUpperCase();
  if (name.includes("SAMPLE-A") || name.includes("A-LOG")) return "A-LOG";
  if (name.includes("SAMPLE-P") || name.includes("P-LOG")) return "P-LOG";
  return null;
}

export function AnalyticsViewer({ reports }: AnalyticsViewerProps) {
  const [sampleType, setSampleType] = useState<SampleType>("A-LOG");
  const [plotId, setPlotId] = useState<string | null>(null);
  const [sensorSerial, setSensorSerial] = useState<string | null>(null);

  const availableSampleTypes = useMemo(() => {
    const types = new Set<SampleType>();
    reports.forEach((r) => {
      const t = detectSampleType(r.name);
      if (t) types.add(t);
    });
    return types;
  }, [reports]);

  const csvPath = useMemo(() => {
    const match = reports.find((r) => detectSampleType(r.name) === sampleType);
    return match?.path ?? null;
  }, [reports, sampleType]);

  const { catalog, isLoading: catalogLoading } = usePlotCatalog(sampleType);

  const currentPlotId =
    plotId && catalog.some((p) => p.id === plotId)
      ? plotId
      : (catalog[0]?.id ?? null);

  const { result, isLoading, error } = useAnalytics(
    csvPath,
    currentPlotId,
    sensorSerial,
  );

  const grouped = catalog.reduce<
    Record<string, { value: string; label: string }[]>
  >((acc, item) => {
    (acc[item.category] ??= []).push({ value: item.id, label: item.label });
    return acc;
  }, {});
  const plotData = Object.entries(grouped).map(([group, items]) => ({
    group,
    items,
  }));

  return (
    <Paper className="analytics-viewer">
      <Stack className="analytics-viewer__content">

        <SimpleGrid cols={{ base: 1, sm: 3 }}>
          <Select
            label="Sample"
            data={[
              {
                value: "A-LOG",
                label: "SAMPLE-A",
                disabled: !availableSampleTypes.has("A-LOG"),
              },
              {
                value: "P-LOG",
                label: "SAMPLE-P",
                disabled: !availableSampleTypes.has("P-LOG"),
              },
            ]}
            value={sampleType}
            onChange={(v) => {
              if (v) {
                setSampleType(v as SampleType);
                setPlotId(null);
                setSensorSerial(null);
              }
            }}
            allowDeselect={false}
            disabled={catalogLoading}
          />

          <Select
            label="Plot"
            placeholder="Select a plot"
            data={plotData}
            value={currentPlotId}
            onChange={(v) => v && setPlotId(v)}
            searchable
            nothingFoundMessage="No plots"
            disabled={catalogLoading}
          />
        </SimpleGrid>

        {!csvPath && (
          <Alert color="yellow" icon={<IconAlertCircle size={18} />}>
            No CSV found for <strong>{sampleType}</strong>.
          </Alert>
        )}

        {error && (
          <Alert
            color="red"
            icon={<IconAlertCircle size={18} />}
            title="Analysis failed"
          >
            {error}
          </Alert>
        )}

        {isLoading && (
          <Stack align="center" py="xl">
            <Loader />
            <Text size="sm">Analyzing series…</Text>
          </Stack>
        )}

        {!isLoading && result?.figure && (
          <Stack>
            <Paper withBorder p="md">
              <Stack gap={4}>
                <Text fw={500}>Analysis</Text>
                <Text size="sm">
                  Trend: {result.trend.method}
                  {result.trend.r2 != null &&
                    ` · R² = ${result.trend.r2.toFixed(3)}`}
                </Text>
                <Text size="sm">Spikes: {result.anomalies.spikes.length}</Text>
                <Text size="sm">Steps: {result.anomalies.steps.length}</Text>
                <Text size="sm">Gaps: {result.anomalies.gaps.length}</Text>
                <Text size="sm">
                  Missing runs: {result.anomalies.nan_runs.length}
                </Text>
              </Stack>
            </Paper>
          </Stack>
        )}
      </Stack>
    </Paper>
  );
}
