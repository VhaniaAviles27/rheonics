import type { AppView } from "./app-layout.types";

export interface SidebarProps {
  activeView: AppView;
  onNavigate: (view: AppView) => void;
}