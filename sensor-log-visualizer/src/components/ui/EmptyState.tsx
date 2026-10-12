import { Paper, Stack, Text } from "@mantine/core";
import "../styles/metric-card.css";
import type { MetricCardProps } from "./types/metric-card.types";

export function MetricCard({ label, value, description }: MetricCardProps) {
  return (
    <Paper className="metric-card">
      <Stack className="metric-card__content">
        <Text className="metric-card__label">{label}</Text>
        <Text className="metric-card__value">{value}</Text>
        <Text className="metric-card__description">{description}</Text>
      </Stack>
    </Paper>
  );
}
