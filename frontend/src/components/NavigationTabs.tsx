"use client";

import React from "react";
import { Activity, ShieldAlert, Cpu, Flame, ListFilter, ShieldCheck } from "lucide-react";
import { useSecurityStore, TabType } from "@/store/useSecurityStore";

export const NavigationTabs: React.FC = () => {
  const { activeTab, setActiveTab, metrics, liveAlerts } = useSecurityStore();

  const criticalCount = metrics?.critical_alerts || 0;
  const activeAlertsCount = metrics?.active_alerts || 0;

  const tabs: { id: TabType; label: string; icon: React.ElementType; badge?: string | number; badgeColor?: string }[] = [
    {
      id: "operations",
      label: "Live Battleground",
      icon: Activity,
    },
    {
      id: "forensics",
      label: "Threat Forensics & Triage",
      icon: ShieldAlert,
      badge: activeAlertsCount > 0 ? activeAlertsCount : undefined,
      badgeColor: criticalCount > 0 ? "bg-rose-500 text-black font-bold" : "bg-cyan-900 text-cyan-300",
    },
    {
      id: "models",
      label: "ML Governance & Explainability",
      icon: Cpu,
      badge: "99.8% F1",
      badgeColor: "bg-emerald-950 text-emerald-400 border border-emerald-800",
    },
    {
      id: "mitigation",
      label: "Mitigation Engine (eBPF)",
      icon: ShieldCheck,
      badge: "eBPF Drop",
      badgeColor: "bg-blue-950 text-blue-300 border border-blue-800",
    },
  ];

  return (
    <div className="border-b border-zinc-800/80 bg-[#060a14]/90 px-4 sm:px-6">
      <div className="max-w-[1700px] mx-auto flex items-center justify-between overflow-x-auto no-scrollbar gap-2">
        <div className="flex items-center gap-1.5 py-2">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;

            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-3.5 py-2 rounded-md text-xs font-mono transition-all relative ${
                  isActive
                    ? "bg-zinc-900 text-cyan-400 font-bold border border-zinc-700/80 shadow-[0_0_12px_rgba(6,182,212,0.15)]"
                    : "text-zinc-400 hover:text-zinc-200 hover:bg-zinc-900/40 border border-transparent"
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${isActive ? "text-cyan-400" : "text-zinc-500"}`} />
                <span>{tab.label}</span>
                {tab.badge && (
                  <span className={`px-1.5 py-0.2 rounded-full text-[10px] font-mono ${tab.badgeColor}`}>
                    {tab.badge}
                  </span>
                )}
                {isActive && (
                  <span className="absolute bottom-0 left-2 right-2 h-[2px] bg-cyan-400 shadow-[0_0_8px_#06b6d4]"></span>
                )}
              </button>
            );
          })}
        </div>

        {/* Global Pipeline Telemetry Tag */}
        <div className="hidden lg:flex items-center gap-3 text-[11px] font-mono text-zinc-400">
          <div className="flex items-center gap-1.5">
            <span className="text-zinc-500">Pipeline:</span>
            <span className="text-zinc-300">Redis Streams ──► FastAPI ──► XGBoost + iForest ──► WebSockets</span>
          </div>
          <span className="text-zinc-700">|</span>
          <div className="flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
            <span className="text-emerald-400">Zero Train-Serve Skew</span>
          </div>
        </div>
      </div>
    </div>
  );
};
