import { Group, SimpleGrid, Stack, Text, Title } from "@mantine/core";
import { MetricCard } from "../../../components/ui/MetricCard";
import { useOverview } from "../hooks/useOverview";
import "../styles/overview-panel.css";
import { buildMetricValues } from "../utils/overview-metrics";
import { OVERVIEW_METRICS } from "../constants/overview.constants";

export function OverviewPanel() {
  const { data, isLoading, error } = useOverview();
  const values = buildMetricValues(data);

  const description = isLoading
    ? "Loading workspace data..."
    : error
      ? "Could not load workspace data."
      : "General state of the generated reports.";

  return (
    <Stack className="overview-panel">
      <Group className="overview-panel__header">
        <Stack className="overview-panel__heading">
          <Title className="overview-panel__title" order={3}>
            Workspace summary
          </Title>
          <Text className="overview-panel__description">{description}</Text>
        </Stack>
      </Group>

      <SimpleGrid className="overview-panel__grid">
        {OVERVIEW_METRICS.map((metric) => (
          <MetricCard
            key={metric.key}
            label={metric.label}
            value={values[metric.key]}
            description={metric.description}
          />
        ))}
      </SimpleGrid>
    </Stack>
  );
}