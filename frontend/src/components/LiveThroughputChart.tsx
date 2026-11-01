"use client";

import React from "react";
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
} from "recharts";
import { TimeSeriesPoint } from "@/types";

interface Props {
  data: TimeSeriesPoint[];
}

export const LiveThroughputChart: React.FC<Props> = ({ data }) => {
  // If data is empty or short, provide a few default zero placeholders
  const chartData = data.length > 0 ? data : [
    { timestamp: "00:00:00", events_count: 0, alerts_count: 0, avg_latency_ms: 0 }
  ];

  return (
    <div className="rounded-xl border border-slate-800 bg-[#090d16]/90 p-5 shadow-lg backdrop-blur-sm">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-4 border-b border-slate-800/80 gap-2">
        <div>
          <h2 className="text-sm font-semibold font-mono uppercase tracking-wider text-slate-200">
            Real-Time Pipeline Telemetry
          </h2>
          <p className="text-xs text-slate-400 font-mono mt-0.5">
            Sliding 60-second window: Ingestion EPS vs Threat Detections
          </p>
        </div>
        <div className="flex items-center gap-4 text-xs font-mono">
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-cyan-400"></span>
            <span className="text-slate-300">Throughput (EPS)</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-rose-500"></span>
            <span className="text-slate-300">Alerts Triggered</span>
          </div>
        </div>
      </div>

      <div className="h-64 mt-4 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="epsGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#06b6d4" stopOpacity={0.0} />
              </linearGradient>
              <linearGradient id="alertsGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#f43f5e" stopOpacity={0.5} />
                <stop offset="95%" stopColor="#f43f5e" stopOpacity={0.0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" opacity={0.6} />
            <XAxis
              dataKey="timestamp"
              stroke="#64748b"
              fontSize={11}
              fontFamily="monospace"
              tickLine={false}
            />
            <YAxis
              stroke="#64748b"
              fontSize={11}
              fontFamily="monospace"
              tickLine={false}
              allowDecimals={false}
            />
            <Tooltip
              content={({ active, payload, label }) => {
                if (active && payload && payload.length) {
                  return (
                    <div className="rounded-lg border border-slate-700 bg-slate-900/95 p-2.5 shadow-xl backdrop-blur-md text-xs font-mono">
                      <div className="text-slate-400 border-b border-slate-800 pb-1 mb-1.5">
                        Time: {label}
                      </div>
                      <div className="text-cyan-400 flex items-center justify-between gap-4">
                        <span>Throughput:</span>
                        <span className="font-bold">{payload[0]?.value} EPS</span>
                      </div>
                      <div className="text-rose-400 flex items-center justify-between gap-4 mt-0.5">
                        <span>Alerts:</span>
                        <span className="font-bold">{payload[1]?.value}</span>
                      </div>
                    </div>
                  );
                }
                return null;
              }}
            />
            <Area
              type="monotone"
              dataKey="events_count"
              stroke="#06b6d4"
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#epsGradient)"
              isAnimationActive={false}
            />
            <Area
              type="monotone"
              dataKey="alerts_count"
              stroke="#f43f5e"
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#alertsGradient)"
              isAnimationActive={false}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
