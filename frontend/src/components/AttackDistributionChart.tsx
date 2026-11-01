"use client";

import React from "react";
import { MetricsSummary } from "@/types";
import { ShieldAlert, Crosshair } from "lucide-react";

interface Props {
  metrics: MetricsSummary | null;
}

const ATTACK_COLORS: Record<string, string> = {
  "DoS-Hulk": "#f43f5e", // rose
  "DDoS-LOIC-HTTP": "#e11d48", // deep rose
  "Botnet": "#a855f7", // purple
  "SSH-Bruteforce": "#f59e0b", // amber
  "Infiltration": "#ef4444", // red
  "Zero-Day Anomaly": "#ec4899", // pink
  "Benign": "#10b981", // emerald
};

export const AttackDistributionChart: React.FC<Props> = ({ metrics }) => {
  const topAttacks = metrics?.top_attacks || [];
  const totalAttackHits = topAttacks.reduce((acc, curr) => acc + curr.count, 0) || 1;

  return (
    <div className="rounded-xl border border-slate-800 bg-[#090d16]/90 p-5 shadow-lg backdrop-blur-sm flex flex-col justify-between">
      <div>
        <div className="flex items-center justify-between pb-3 border-b border-slate-800/80">
          <div>
            <h2 className="text-sm font-semibold font-mono uppercase tracking-wider text-slate-200 flex items-center gap-2">
              <Crosshair className="w-4 h-4 text-cyan-400" />
              Threat Vectors
            </h2>
            <p className="text-xs text-slate-400 font-mono mt-0.5">
              Top attack classes detected
            </p>
          </div>
          <span className="text-xs font-mono text-cyan-400 bg-cyan-950/40 border border-cyan-800/60 px-2 py-0.5 rounded">
            {topAttacks.length} Types
          </span>
        </div>

        <div className="mt-4 space-y-3.5">
          {topAttacks.length === 0 ? (
            <div className="py-12 text-center text-xs text-slate-500 font-mono">
              Awaiting threat stream detections...
            </div>
          ) : (
            topAttacks.map((item) => {
              const pct = Math.round((item.count / totalAttackHits) * 100);
              const color = ATTACK_COLORS[item.attack_type] || "#38bdf8";

              return (
                <div key={item.attack_type} className="space-y-1.5">
                  <div className="flex items-center justify-between text-xs font-mono">
                    <span className="text-slate-300 font-medium">{item.attack_type}</span>
                    <div className="flex items-center gap-2">
                      <span className="text-slate-400">{item.count} pkts</span>
                      <span className="text-slate-500 font-bold">({pct}%)</span>
                    </div>
                  </div>
                  <div className="w-full h-2 rounded-full bg-slate-800 overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all duration-500"
                      style={{
                        width: `${pct}%`,
                        backgroundColor: color,
                        boxShadow: `0 0 8px ${color}80`,
                      }}
                    ></div>
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>

      <div className="mt-6 pt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px] font-mono text-slate-400">
        <span>Classifier: XGBoost (CICIDS2018)</span>
        <span className="text-emerald-400">Accuracy: 99.8%</span>
      </div>
    </div>
  );
};
