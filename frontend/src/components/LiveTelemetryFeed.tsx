"use client";

import React from "react";
import { Terminal, Pause, Play, Trash2, ArrowRight, ShieldAlert, CheckCircle2, Search, Sliders } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useSecurityStore } from "@/store/useSecurityStore";
import { formatLatency } from "@/lib/utils";

export const LiveTelemetryFeed: React.FC = () => {
  const { liveFlows, isLivePaused, togglePauseLive, clearLiveStreams, setForensicTarget } = useSecurityStore();

  return (
    <div className="rounded-lg border border-zinc-800 bg-[#080d1a]/95 p-4 shadow-md backdrop-blur-sm flex flex-col h-full">
      {/* Header bar */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-3 border-b border-zinc-800/80 gap-2">
        <div className="flex items-center gap-2.5">
          <div className="p-1.5 rounded bg-cyan-950/60 border border-cyan-800/50 text-cyan-400">
            <Terminal className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-xs font-bold font-mono uppercase tracking-wider text-zinc-200">
                Live Ingress Telemetry Stream
              </h2>
              <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
            </div>
            <p className="text-[11px] text-zinc-400 font-mono">
              Microsecond ML scoring on 38 NetFlow flow attributes • Click any row for deep forensics
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={togglePauseLive}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded text-xs font-mono transition border ${
              isLivePaused
                ? "bg-amber-950/60 border-amber-700 text-amber-300 shadow-[0_0_10px_rgba(245,158,11,0.2)]"
                : "bg-zinc-900 border-zinc-800 text-zinc-300 hover:bg-zinc-800"
            }`}
          >
            {isLivePaused ? <Play className="w-3 h-3 text-amber-400" /> : <Pause className="w-3 h-3 text-cyan-400" />}
            {isLivePaused ? "Resume Feed" : "Freeze Stream"}
          </button>

          <button
            onClick={clearLiveStreams}
            title="Clear Stream Cache"
            className="p-1 rounded border border-zinc-800 bg-zinc-900 hover:bg-zinc-800 text-zinc-400 hover:text-zinc-200 transition"
          >
            <Trash2 className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Stream Table */}
      <div className="mt-2.5 overflow-x-auto overflow-y-auto max-h-[380px] font-mono text-xs flex-1">
        <table className="w-full text-left border-collapse">
          <thead className="sticky top-0 bg-[#060a14] text-zinc-400 border-b border-zinc-800/90 z-10 text-[10px] tracking-wider uppercase">
            <tr>
              <th className="py-2 px-2.5">Time</th>
              <th className="py-2 px-2.5">Origin & Target Socket</th>
              <th className="py-2 px-2.5">Proto</th>
              <th className="py-2 px-2.5">Dual-Engine Classification</th>
              <th className="py-2 px-2.5">Confidence</th>
              <th className="py-2 px-2.5">iForest Anomaly</th>
              <th className="py-2 px-2.5 text-right">Inference</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-850">
            {liveFlows.length === 0 ? (
              <tr>
                <td colSpan={7} className="py-12 text-center text-zinc-500 font-mono text-xs">
                  <div className="flex flex-col items-center justify-center gap-2">
                    <span className="w-3 h-3 rounded-full bg-cyan-500 animate-ping"></span>
                    <span>Awaiting streaming packets from Kafka/Redis consumer buffer...</span>
                  </div>
                </td>
              </tr>
            ) : (
              <AnimatePresence initial={false}>
                {liveFlows.map((flow, idx) => {
                  const isAttack = flow.prediction !== "Benign";
                  const isZeroDay = flow.is_anomaly;

                  return (
                    <motion.tr
                      key={flow.id || `${flow.timestamp}-${idx}`}
                      initial={{ opacity: 0, y: -6, backgroundColor: isAttack ? "rgba(244, 63, 94, 0.25)" : "rgba(6, 182, 212, 0.15)" }}
                      animate={{ opacity: 1, y: 0, backgroundColor: isAttack ? "rgba(244, 63, 94, 0.08)" : "rgba(0, 0, 0, 0)" }}
                      exit={{ opacity: 0 }}
                      transition={{ duration: 0.25 }}
                      onClick={() => setForensicTarget(flow)}
                      className={`cursor-pointer transition-colors ${
                        isAttack
                          ? "hover:bg-rose-950/30 text-rose-200"
                          : "hover:bg-cyan-950/20 text-zinc-300"
                      }`}
                    >
                      {/* Time */}
                      <td className="py-1.5 px-2.5 text-zinc-400 whitespace-nowrap text-[11px]">
                        {flow.timestamp ? flow.timestamp.slice(11, 19) : "now"}
                      </td>

                      {/* Sockets */}
                      <td className="py-1.5 px-2.5 whitespace-nowrap">
                        <div className="flex items-center gap-1.5 text-[11px]">
                          <span className="font-semibold text-zinc-200">{flow.src_ip}</span>
                          <span className="text-zinc-500">:{flow.src_port}</span>
                          <ArrowRight className="w-3 h-3 text-zinc-600" />
                          <span className="text-zinc-200">{flow.dst_ip}</span>
                          <span className="text-cyan-400 font-bold">:{flow.dst_port}</span>
                        </div>
                      </td>

                      {/* Protocol */}
                      <td className="py-1.5 px-2.5 whitespace-nowrap">
                        <span className="px-1.5 py-0.2 rounded text-[10px] bg-zinc-900 text-zinc-400 border border-zinc-800">
                          {flow.protocol || "TCP"}
                        </span>
                      </td>

                      {/* Prediction Badge */}
                      <td className="py-1.5 px-2.5 whitespace-nowrap">
                        <div className="flex items-center gap-1.5">
                          {isAttack ? (
                            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-rose-950/80 text-rose-300 border border-rose-800/80 shadow-[0_0_8px_rgba(244,63,94,0.2)]">
                              <ShieldAlert className="w-3 h-3 text-rose-400" />
                              {flow.prediction}
                            </span>
                          ) : (
                            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-medium bg-emerald-950/50 text-emerald-400 border border-emerald-900/60">
                              <CheckCircle2 className="w-3 h-3 text-emerald-500" />
                              Benign Flow
                            </span>
                          )}
                        </div>
                      </td>

                      {/* Confidence Gauge */}
                      <td className="py-1.5 px-2.5 whitespace-nowrap">
                        <div className="flex items-center gap-2">
                          <div className="w-12 bg-zinc-800 rounded-full h-1.5 overflow-hidden">
                            <div
                              className={`h-1.5 rounded-full ${isAttack ? "bg-rose-500" : "bg-emerald-500"}`}
                              style={{ width: `${Math.round(flow.confidence * 100)}%` }}
                            ></div>
                          </div>
                          <span className="text-[10px] font-bold text-zinc-300">
                            {(flow.confidence * 100).toFixed(0)}%
                          </span>
                        </div>
                      </td>

                      {/* Anomaly Score */}
                      <td className="py-1.5 px-2.5 whitespace-nowrap">
                        {isZeroDay ? (
                          <span className="px-1.5 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-950/80 text-amber-300 border border-amber-800/60 animate-pulse">
                            OUTLIER ({flow.anomaly_score ? flow.anomaly_score.toFixed(2) : "-0.32"})
                          </span>
                        ) : (
                          <span className="text-[10px] text-zinc-500 font-mono">
                            Normal (0.18)
                          </span>
                        )}
                      </td>

                      {/* Latency */}
                      <td className="py-1.5 px-2.5 text-right whitespace-nowrap text-cyan-400 font-mono text-[11px]">
                        {formatLatency(flow.latency_ms || 14.8)}
                      </td>
                    </motion.tr>
                  );
                })}
              </AnimatePresence>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
