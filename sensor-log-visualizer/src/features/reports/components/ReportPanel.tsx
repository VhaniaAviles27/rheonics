import { Alert, Button, Group, Loader, Stack, Text, Title } from "@mantine/core";
import { IconAlertCircle, IconRefresh } from "@tabler/icons-react";
import { useReports } from "../hooks/useReports";

import "../styles/reports-panel.css";
import { ReportsEmptyState } from "./ReportEmptyState";
import { ReportsList } from "./ReportList";
import { ReportsPreview } from "./ReportPreview";

export function ReportsPanel() {
  const {
    reports,
    isLoading,
    error,
    preview,
    refresh,
    openPreview,
    closePreview,
  } = useReports();

  const showLoader = isLoading && reports.length === 0;
  const showEmpty = !isLoading && reports.length === 0;

  return (
    <Stack className="reports-panel">
      <Group className="reports-panel__header" justify="space-between">
        <Stack gap={4}>
          <Title order={4}>Generated reports</Title>
          <Text c="dimmed" size="sm">
            CSV files produced by the analysis pipeline.
          </Text>
        </Stack>

        <Button
          variant="light"
          leftSection={<IconRefresh size={16} />}
          onClick={refresh}
          loading={isLoading}
        >
          Refresh
        </Button>
      </Group>

      {error && (
        <Alert
          color="red"
          icon={<IconAlertCircle size={18} />}
          title="Could not load reports"
        >
          {error}
        </Alert>
      )}

      {showLoader && (
        <Group justify="center" py="xl">
          <Loader />
        </Group>
      )}

      {showEmpty && <ReportsEmptyState />}

      {reports.length > 0 && (
        <ReportsList reports={reports} onView={openPreview} />
      )}

      {preview && (
        <ReportsPreview
          path={preview.path}
          content={preview.content}
          onClose={closePreview}
        />
      )}
    </Stack>
  );
}