import { Badge, Button, Group, Paper, Table, Text } from "@mantine/core";
import { IconEye, IconFileSpreadsheet } from "@tabler/icons-react";
import { formatDate, formatSize } from "../../../lib/format";
import { ReportFile } from "../types/report.types";

interface ReportsListProps {
  reports: ReportFile[];
  onView: (path: string) => void;
}

export function ReportsList({ reports, onView }: ReportsListProps) {
  return (
    <Paper className="reports-panel__list">
      <Table highlightOnHover verticalSpacing="sm">
        <Table.Thead>
          <Table.Tr>
            <Table.Th>File</Table.Th>
            <Table.Th>Generated</Table.Th>
            <Table.Th>Size</Table.Th>
            <Table.Th />
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>
          {reports.map((r) => (
            <Table.Tr key={r.path}>
              <Table.Td>
                <Group gap="xs">
                  <IconFileSpreadsheet size={16} />
                  <Text size="sm" fw={500}>
                    {r.name}
                  </Text>
                </Group>
              </Table.Td>
              <Table.Td>
                <Text size="sm">{formatDate(r.modifiedAt)}</Text>
              </Table.Td>
              <Table.Td>
                <Badge variant="light">{formatSize(r.sizeBytes)}</Badge>
              </Table.Td>
              <Table.Td>
                <Button
                  size="xs"
                  variant="subtle"
                  leftSection={<IconEye size={14} />}
                  onClick={() => onView(r.path)}
                >
                  View
                </Button>
              </Table.Td>
            </Table.Tr>
          ))}
        </Table.Tbody>
      </Table>
    </Paper>
  );
}