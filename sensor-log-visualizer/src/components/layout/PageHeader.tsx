import { Badge, Group, Stack, Text, Title } from "@mantine/core";
import { IconDeviceDesktop } from "@tabler/icons-react";
import type { PageHeaderProps } from "./types/page-header.types";
import "./styles/page-header.css";

export function PageHeader({ title, subtitle }: PageHeaderProps) {
  return (
    <Group className="page-header">
      <Stack className="page-header__content">
        <Text className="page-header__eyebrow">Equipment diagnostics</Text>

        <Title className="page-header__title" order={2}>
          {title}
        </Title>

        <Text className="page-header__subtitle">{subtitle}</Text>
      </Stack>

      <Badge
        className="page-header__workspace-badge"
        leftSection={<IconDeviceDesktop size={15} />}
      >
        Local workspace
      </Badge>
    </Group>
  );
}
