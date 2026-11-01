"use client";

import React, { useState, useEffect } from "react";
import { useWebSocket } from "@/hooks/useWebSocket";
import { useSecurityStore } from "@/store/useSecurityStore";
import { fetchMetricsSummary, fetchMetricsHistory } from "@/lib/api";
import { DashboardHeader } from "@/components/DashboardHeader";
import { NavigationTabs } from "@/components/NavigationTabs";
import { KpiCards } from "@/components/KpiCards";
import { LiveThroughputChart } from "@/components/LiveThroughputChart";
import { AttackDistributionChart } from "@/components/AttackDistributionChart";
import { LiveTelemetryFeed } from "@/components/LiveTelemetryFeed";
import { AlertsDataTable } from "@/components/AlertsDataTable";
import { TrafficControlPanel } from "@/components/TrafficControlPanel";
import { AlertDetailModal } from "@/components/AlertDetailModal";
import { FlowForensicDrawer } from "@/components/FlowForensicDrawer";
import { ModelGovernanceView } from "@/components/ModelGovernanceView";
import { MitigationEngineView } from "@/components/MitigationEngineView";

export default function SOCDashboard() {
  const [isTrafficControlOpen, setIsTrafficControlOpen] = useState(false);
  const { reconnect } = useWebSocket();

  const {
    activeTab,
    metrics,
    setMetrics,
    timeSeries,
    setTimeSeries,
    selectedAlert,
    setSelectedAlert,
    forensicTarget,
    setForensicTarget,
  } = useSecurityStore();

  const loadData = async () => {
    try {
      const [sum, hist] = await Promise.all([
        fetchMetricsSummary().catch(() => null),
        fetchMetricsHistory().catch(() => []),
      ]);
      if (sum) setMetrics(sum);
      if (hist && hist.length > 0) {
        setTimeSeries(hist);
      }
    } catch {
      // Backend starting up
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 2500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-[#030712] text-zinc-100 flex flex-col font-sans selection:bg-cyan-500 selection:text-black">
      {/* 1. Tactical Command Header */}
      <DashboardHeader
        onOpenTrafficControl={() => setIsTrafficControlOpen(true)}
        onRefresh={loadData}
      />

      {/* 2. Tactical Navigation Bar */}
      <NavigationTabs />

      {/* 3. Main Multi-Module Viewport */}
      <main className="flex-1 max-w-[1700px] w-full mx-auto px-4 sm:px-6 py-5 space-y-5">
        {/* KPI Cards: Always visible across all operations */}
        <KpiCards metrics={metrics} />

        {/* TAB 1: Live Operations / Battleground */}
        {activeTab === "operations" && (
          <div className="space-y-5 animate-fade-in">
            {/* Live Throughput & Vector Distribution Charts */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
              <div className="lg:col-span-8">
                <LiveThroughputChart data={timeSeries} />
              </div>
              <div className="lg:col-span-4">
                <AttackDistributionChart metrics={metrics} />
              </div>
            </div>

            {/* Live Streaming Telemetry Feed & Incident Quick Triage */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
              <div className="lg:col-span-7">
                <LiveTelemetryFeed />
              </div>
              <div className="lg:col-span-5">
                <AlertsDataTable onSelectAlert={(alert) => setForensicTarget(alert)} />
              </div>
            </div>
          </div>
        )}

        {/* TAB 2: Threat Forensics & Full Investigation */}
        {activeTab === "forensics" && (
          <div className="space-y-5 animate-fade-in">
            <div className="p-4 rounded-lg border border-zinc-800 bg-[#080d1a]/90 flex items-center justify-between">
              <div>
                <h2 className="text-sm font-bold font-mono uppercase tracking-wider text-zinc-200">
                  Incident Triage & Deep Forensics Database
                </h2>
                <p className="text-xs text-zinc-400 font-mono mt-0.5">
                  Search, filter by severity, transition analyst workflow statuses, and inspect 38 NetFlow flow attributes.
                </p>
              </div>
              <span className="text-xs font-mono text-cyan-400 bg-cyan-950 px-2.5 py-1 rounded border border-cyan-800">
                TanStack Table v8
              </span>
            </div>
            <AlertsDataTable onSelectAlert={(alert) => setForensicTarget(alert)} />
          </div>
        )}

        {/* TAB 3: ML Model Governance & Explainability */}
        {activeTab === "models" && <ModelGovernanceView />}

        {/* TAB 4: Mitigation Engine (eBPF Firewall Blocklist) */}
        {activeTab === "mitigation" && <MitigationEngineView />}
      </main>

      {/* 4. Tactical Footer */}
      <footer className="border-t border-zinc-800/80 bg-[#040814] py-3.5 px-6 text-center text-xs font-mono text-zinc-500">
        <div className="max-w-[1700px] mx-auto flex flex-col sm:flex-row items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
            <span className="text-zinc-400">
              AETHERIS SOC | Enterprise AI-Based Network Threat Detection Platform
            </span>
          </div>
          <span className="text-zinc-600">
            Pipeline: Kafka/Redis Streams ──► FastAPI ASGI ──► PostgreSQL ──► WebSockets ──► Next.js 14
          </span>
        </div>
      </footer>

      {/* 5. Modals & Side Drawers */}
      <TrafficControlPanel
        isOpen={isTrafficControlOpen}
        onClose={() => setIsTrafficControlOpen(false)}
      />

      <AlertDetailModal
        alert={selectedAlert}
        onClose={() => setSelectedAlert(null)}
        onAlertUpdated={() => loadData()}
      />

      <FlowForensicDrawer />
    </div>
  );
}
