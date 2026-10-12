import { Badge } from "@mantine/core";
import "./styles/status-badge.css";
import { variantColors } from "./constants/status-badge.constants";
import type { StatusBadgeProps } from "./types/status-badge.types";

export function StatusBadge({ label, variant = "neutral" }: StatusBadgeProps) {
  return (
    <Badge
      className="status-badge"
      data-variant={variant}
      color={variantColors[variant]}
    >
      {label}
    </Badge>
  );
}
