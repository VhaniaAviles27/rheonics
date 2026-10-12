import { Select, SimpleGrid } from "@mantine/core";
import type {
  ChartType,
  PlotCatalogEntry,
  SampleType,
} from "../types/plots.types";

interface PlotControlsProps {
  sampleType: SampleType;
  onSampleTypeChange: (value: SampleType) => void;
  availableSampleTypes: Set<SampleType>;
  catalog: PlotCatalogEntry[];
  selectedPlotId: string | null;
  onPlotChange: (value: string) => void;
  chartType: ChartType;
  onChartTypeChange: (value: ChartType) => void;
  disabled?: boolean;
}

export function PlotControls({
  sampleType,
  onSampleTypeChange,
  availableSampleTypes,
  catalog,
  selectedPlotId,
  onPlotChange,
  disabled,
}: PlotControlsProps) {
  const grouped = catalog.reduce<Record<string, { value: string; label: string }[]>>(
    (acc, item) => {
      (acc[item.category] ??= []).push({ value: item.id, label: item.label });
      return acc;
    },
    {},
  );

  const selectData = Object.entries(grouped).map(([group, items]) => ({
    group,
    items,
  }));

  return (
    <SimpleGrid cols={{ base: 1, sm: 3 }} className="plot-controls">
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
        onChange={(v) => v && onSampleTypeChange(v as SampleType)}
        allowDeselect={false}
        disabled={disabled}
      />

      <Select
        label="Plot"
        placeholder="Select a plot"
        data={selectData}
        value={selectedPlotId}
        onChange={(v) => v && onPlotChange(v)}
        searchable
        nothingFoundMessage="No plots"
        disabled={disabled}
      />
    </SimpleGrid>
  );
}