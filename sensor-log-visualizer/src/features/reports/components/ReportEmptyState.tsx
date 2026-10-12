import { Paper, Stack, Text } from "@mantine/core";
import { IconFileSpreadsheet } from "@tabler/icons-react";

export function ReportsEmptyState() {
  return (
    <Paper className="reports-panel__empty" p="xl">
      <Stack align="center" gap="xs">
        <IconFileSpreadsheet size={36} />
        <Text fw={500}>No reports yet</Text>
        <Text c="dimmed" size="sm">
          Process a log file first — the resulting CSV will appear here.
        </Text>
      </Stack>
    </Paper>
  );
}