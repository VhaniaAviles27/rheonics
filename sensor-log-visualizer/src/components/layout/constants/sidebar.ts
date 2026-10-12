import {
  IconChartLine,
  IconClipboardData,
  IconFileAnalytics,
  IconGauge,
} from "@tabler/icons-react";
import { NavigationItem } from "../types/app-layout.types";

export const navigationItems = [
  {
    id: "log-analysis",
    label: "Log analysis",
    description: "Import and process",
    icon: IconClipboardData,
  },
  {
    id: "overview",
    label: "Overview",
    description: "Workspace summary",
    icon: IconGauge,
  },
  {
    id: "graphs",
    label: "Graphs",
    description: "Visualize data series",
    icon: IconChartLine,
  },
  {
    id: "trends",
    label: "Trends",
    description: "Analyze data over time",
    icon: IconChartLine,
  },
  {
    id: "reports",
    label: "Reports",
    description: "Analysis outputs",
    icon: IconFileAnalytics,
  },
] satisfies NavigationItem[];
