type StatusBadgeVariant = "success" | "warning" | "neutral";

export interface StatusBadgeProps {
  label: string;
  variant?: StatusBadgeVariant;
}