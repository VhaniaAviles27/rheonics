import { AppView } from "../types/app-layout.types";

export const pageInfo: Record<AppView, { title: string; subtitle: string }> = {
  "log-analysis": {
    title: "Log Analysis",
    subtitle: "Import and inspect equipment log files.",
  },
  overview: {
    title: "Overview",
    subtitle: "Review your latest sensor log analysis.",
  },
  graphs: {
    title: "Graphs",
    subtitle: "Visualize data series.",
  },
  trends: {
    title: "Trends",
    subtitle: "Analyze data over time.",
  },
  reports: {
    title: "Reports",
    subtitle: "Access analysis reports and quality summaries.",
  },
};
