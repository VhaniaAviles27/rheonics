import type { ReactNode } from "react";
import type { TablerIcon } from "@tabler/icons-react";

export type AppView =
  | "log-analysis"
  | "overview"
  | "graphs"
  | "trends"
  | "reports";

export interface NavigationItem {
  id: AppView;
  label: string;
  description: string;
  icon: TablerIcon;
}

export interface AppLayoutProps {
  children: ReactNode;
  title: string;
  subtitle: string;
  activeView: AppView;
  onNavigate: (view: AppView) => void;
}



