export type Severity = "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";

export type AlertStatus = "new" | "acknowledged" | "resolved" | "false_positive";

export interface Alert {
  id: number;
  alert_id: string;
  timestamp: string;
  severity: Severity;
  attack_type: string;
  confidence: number;
  anomaly_score: number;
  src_ip: string;
  dst_ip: string;
  dst_port: number;
  protocol: string;
  hit_count: number;
  status: AlertStatus;
  mitigation_action?: string;
  notes?: string;
  first_seen?: string;
  last_seen?: string;
  is_new?: boolean;
}

export interface FlowEvent {
  id: number;
  timestamp: string;
  src_ip: string;
  dst_ip: string;
  src_port: number;
  dst_port: number;
  protocol: string;
  prediction: string;
  confidence: number;
  anomaly_score: number;
  is_anomaly: boolean;
  latency_ms: number;
}

export interface MetricsSummary {
  total_events_processed: number;
  total_alerts: number;
  active_alerts: number;
  critical_alerts: number;
  high_alerts: number;
  medium_alerts: number;
  low_alerts: number;
  current_eps: number;
  avg_inference_latency_ms: number;
  p95_inference_latency_ms: number;
  anomaly_rate_percent: number;
  top_attacks: { attack_type: string; count: number }[];
  system_status: "HEALTHY" | "WARNING" | "CRITICAL";
}

export interface TimeSeriesPoint {
  timestamp: string;
  events_count: number;
  alerts_count: number;
  avg_latency_ms: number;
}

export type ConnectionStatus = "CONNECTING" | "CONNECTED" | "RECONNECTING" | "DISCONNECTED";
