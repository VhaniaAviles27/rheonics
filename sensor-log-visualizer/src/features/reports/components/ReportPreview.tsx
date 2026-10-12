import {
  Button,
  Group,
  Paper,
  ScrollArea,
  Table,
  Text,
} from "@mantine/core";
import { parseCsvPreview } from "../utils/csv";

interface ReportsPreviewProps {
  path: string;
  content: string;
  onClose: () => void;
}

function basename(path: string): string {
  return path.split(/[\\/]/).pop() ?? path;
}

export function ReportsPreview({ path, content, onClose }: ReportsPreviewProps) {
  const parsed = parseCsvPreview(content);

  return (
    <Paper className="reports-panel__preview" p="md">
      <Group justify="space-between" mb="sm">
        <Text fw={500} size="sm">
          {basename(path)} — showing {parsed.rows.length} of {parsed.total} rows
        </Text>
        <Button size="xs" variant="subtle" onClick={onClose}>
          Close
        </Button>
      </Group>

      <ScrollArea h={420} type="auto">
        <Table stickyHeader striped withTableBorder>
          <Table.Thead>
            <Table.Tr>
              {parsed.header.map((h, i) => (
                <Table.Th key={`${h}-${i}`}>{h}</Table.Th>
              ))}
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>
            {parsed.rows.map((row, ri) => (
              <Table.Tr key={ri}>
                {parsed.header.map((_, ci) => (
                  <Table.Td key={ci}>
                    <Text size="xs">{row[ci] ?? ""}</Text>
                  </Table.Td>
                ))}
              </Table.Tr>
            ))}
          </Table.Tbody>
        </Table>
      </ScrollArea>
    </Paper>
  );
}