import { Alert, MetricsSummary, TimeSeriesPoint } from "@/types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function fetchMetricsSummary(): Promise<MetricsSummary> {
  const res = await fetch(`${API_BASE}/api/metrics/summary`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch metrics summary");
  return res.json();
}

export async function fetchMetricsHistory(): Promise<TimeSeriesPoint[]> {
  const res = await fetch(`${API_BASE}/api/metrics/history`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch metrics history");
  return res.json();
}

export async function fetchAlerts(params: {
  page?: number;
  pageSize?: number;
  severity?: string;
  attackType?: string;
  status?: string;
  search?: string;
} = {}): Promise<{ total: number; page: number; page_size: number; items: Alert[] }> {
  const query = new URLSearchParams();
  if (params.page) query.set("page", params.page.toString());
  if (params.pageSize) query.set("page_size", params.pageSize.toString());
  if (params.severity) query.set("severity", params.severity);
  if (params.attackType) query.set("attack_type", params.attackType);
  if (params.status) query.set("status", params.status);
  if (params.search) query.set("search", params.search);

  const res = await fetch(`${API_BASE}/api/alerts?${query.toString()}`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch alerts");
  return res.json();
}

export async function updateAlertStatus(alertId: string, status: string, notes?: string): Promise<Alert> {
  const res = await fetch(`${API_BASE}/api/alerts/${alertId}/status`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status, notes }),
  });
  if (!res.ok) throw new Error("Failed to update alert status");
  return res.json();
}

export async function controlTraffic(payload: {
  rate_eps?: number;
  burst_attack?: string;
  burst_count?: number;
  is_paused?: boolean;
}) {
  const res = await fetch(`${API_BASE}/api/traffic/control`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to control traffic");
  return res.json();
}

export async function fetchModelMetrics() {
  const res = await fetch(`${API_BASE}/api/metrics/models`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch model metrics");
  return res.json();
}

export async function fetchModelInfo() {
  const res = await fetch(`${API_BASE}/api/models/info`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch model info");
  return res.json();
}

export async function fetchConfusionMatrix() {
  const res = await fetch(`${API_BASE}/api/models/confusion-matrix`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch confusion matrix");
  return res.json();
}

export async function fetchMitigationRules() {
  const res = await fetch(`${API_BASE}/api/mitigation/rules`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch mitigation rules");
  return res.json();
}

export async function blockIP(payload: { ip_address: string; reason?: string; ttl_seconds?: number; action?: string }) {
  const res = await fetch(`${API_BASE}/api/mitigation/block`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to block IP");
  return res.json();
}

export async function unblockIP(ipAddress: string) {
  const res = await fetch(`${API_BASE}/api/mitigation/unblock/${ipAddress}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to unblock IP");
  return res.json();
}

export async function flushMitigationRules() {
  const res = await fetch(`${API_BASE}/api/mitigation/flush`, {
    method: "POST",
  });
  if (!res.ok) throw new Error("Failed to flush mitigation rules");
  return res.json();
}
