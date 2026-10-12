import {
  Badge,
  Box,
  Divider,
  Group,
  NavLink,
  Stack,
  Text,
  ThemeIcon,
} from "@mantine/core";

import { IconChartLine } from "@tabler/icons-react";
import type { SidebarProps } from "./types/sidebar.types";
import "./styles/sidebar.css";
import { navigationItems } from "./constants/sidebar";

export function Sidebar({ activeView, onNavigate }: SidebarProps) {
  return (
    <Stack className="sidebar">
      <Box className="sidebar__main">
        <Group className="sidebar__brand">
          <ThemeIcon className="sidebar__brand-icon">
            <IconChartLine />
          </ThemeIcon>

          <Box className="sidebar__brand-info">
            <Text className="sidebar__brand-title">Sensor Logs</Text>
            <Text className="sidebar__brand-subtitle">Analysis workspace</Text>
          </Box>
        </Group>

        <Stack className="sidebar__navigation">
          {navigationItems.map((item) => {
            const Icon = item.icon;

            return (
              <NavLink
                className="sidebar__navigation-root"
                key={item.id}
                label={item.label}
                description={item.description}
                leftSection={<Icon size={19} stroke={1.7} />}
                active={activeView === item.id}
                onClick={() => onNavigate(item.id)}
              />
            );
          })}
        </Stack>
      </Box>

      <Box className="sidebar__footer">
        <Divider className="sidebar__divider" />
        <Group className="sidebar__environment">
          <Text className="sidebar__environment-label">
            Desktop environment
          </Text>
          <Badge className="sidebar__version">v0.1.0</Badge>
        </Group>
      </Box>
    </Stack>
  );
}
