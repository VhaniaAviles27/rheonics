import { AppShell, Box } from "@mantine/core";
import { Sidebar } from "./Sidebar";
import { PageHeader } from "./PageHeader";
import type { AppLayoutProps } from "./types/app-layout.types";
import "./styles/app-layout.css";

export function AppLayout({
  children,
  title,
  subtitle,
  activeView,
  onNavigate,
}: AppLayoutProps) {
  return (
    <AppShell className="app-layout">
      <AppShell.Navbar className="app-layout__navbar">
        <Sidebar activeView={activeView} onNavigate={onNavigate} />
      </AppShell.Navbar>

      <AppShell.Main className="app-layout__main">
        <Box className="app-layout__container">
          <PageHeader title={title} subtitle={subtitle} />
          {children}
        </Box>
      </AppShell.Main>
    </AppShell>
  );
}
