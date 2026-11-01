import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatNumber(num: number): string {
  if (num >= 1_000_000) {
    return (num / 1_000_000).toFixed(1) + "M";
  }
  if (num >= 1_000) {
    return (num / 1_000).toFixed(1) + "k";
  }
  return num.toString();
}

export function formatLatency(ms: number): string {
  if (ms < 1.0) {
    return `${(ms * 1000).toFixed(0)} µs`;
  }
  return `${ms.toFixed(2)} ms`;
}

export function getSeverityColor(severity: string) {
  switch (severity?.toUpperCase()) {
    case "CRITICAL":
      return {
        badge: "bg-rose-950/80 text-rose-400 border-rose-800/80 shadow-[0_0_12px_rgba(244,63,94,0.3)]",
        dot: "bg-rose-500",
        border: "border-rose-500/50"
      };
    case "HIGH":
      return {
        badge: "bg-amber-950/80 text-amber-400 border-amber-800/80",
        dot: "bg-amber-500",
        border: "border-amber-500/50"
      };
    case "MEDIUM":
      return {
        badge: "bg-yellow-950/80 text-yellow-400 border-yellow-800/80",
        dot: "bg-yellow-500",
        border: "border-yellow-500/50"
      };
    case "LOW":
      return {
        badge: "bg-blue-950/80 text-blue-400 border-blue-800/80",
        dot: "bg-blue-500",
        border: "border-blue-500/50"
      };
    default:
      return {
        badge: "bg-slate-800 text-slate-400 border-slate-700",
        dot: "bg-slate-500",
        border: "border-slate-700"
      };
  }
}
