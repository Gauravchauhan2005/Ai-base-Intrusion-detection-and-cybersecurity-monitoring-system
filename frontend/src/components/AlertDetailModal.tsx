"use client";

import React, { useState } from "react";
import { X, ShieldAlert, Cpu, Fingerprint, ShieldCheck, CheckCircle2, Clock } from "lucide-react";
import { Alert } from "@/types";
import { updateAlertStatus } from "@/lib/api";
import { getSeverityColor } from "@/lib/utils";

interface Props {
  alert: Alert | null;
  onClose: () => void;
  onAlertUpdated?: (updated: Alert) => void;
}

export const AlertDetailModal: React.FC<Props> = ({ alert, onClose, onAlertUpdated }) => {
  const [notes, setNotes] = useState<string>(alert?.notes || "");
  const [updating, setUpdating] = useState<boolean>(false);

  if (!alert) return null;

  const severityStyle = getSeverityColor(alert.severity);

  const handleUpdate = async (newStatus: string) => {
    try {
      setUpdating(true);
      const res = await updateAlertStatus(alert.alert_id, newStatus, notes);
      if (onAlertUpdated) onAlertUpdated(res);
      onClose();
    } catch (e) {
      console.error(e);
    } finally {
      setUpdating(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75 backdrop-blur-sm p-4">
      <div className="w-full max-w-2xl rounded-2xl border border-slate-700 bg-[#090d16] p-6 shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className={`p-2 rounded-lg ${severityStyle.badge}`}>
              <ShieldAlert className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-base font-bold font-mono text-slate-100 uppercase tracking-wide">
                  {alert.attack_type}
                </h3>
                <span className={`px-2 py-0.5 rounded text-[10px] font-mono border uppercase ${severityStyle.badge}`}>
                  {alert.severity}
                </span>
              </div>
              <p className="text-xs text-slate-400 font-mono mt-0.5">
                Incident ID: {alert.alert_id}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg border border-slate-800 bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-slate-200 transition"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Incident Details Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-5">
          <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
            <span className="text-[10px] font-mono uppercase text-slate-500">Attacker IP</span>
            <div className="text-xs font-mono font-bold text-rose-400 mt-1 break-all">
              {alert.src_ip}
            </div>
          </div>
          <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
            <span className="text-[10px] font-mono uppercase text-slate-500">Target Socket</span>
            <div className="text-xs font-mono font-bold text-cyan-400 mt-1">
              {alert.dst_ip}:{alert.dst_port}
            </div>
          </div>
          <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
            <span className="text-[10px] font-mono uppercase text-slate-500">ML Confidence</span>
            <div className="text-xs font-mono font-bold text-emerald-400 mt-1">
              {(alert.confidence * 100).toFixed(1)}%
            </div>
          </div>
          <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
            <span className="text-[10px] font-mono uppercase text-slate-500">Aggregated Packets</span>
            <div className="text-xs font-mono font-bold text-slate-200 mt-1">
              {alert.hit_count} flows
            </div>
          </div>
        </div>

        {/* Dual-Engine Explainability */}
        <div className="mt-4 p-4 rounded-xl bg-slate-900/50 border border-slate-800 space-y-2">
          <div className="flex items-center gap-2 text-xs font-mono text-slate-300 font-semibold">
            <Cpu className="w-4 h-4 text-cyan-400" />
            Detection Pipeline Breakdown
          </div>
          <p className="text-xs text-slate-400 font-mono leading-relaxed">
            Supervised XGBoost multi-class classifier matched packet flow patterns to <strong>{alert.attack_type}</strong> with {(alert.confidence * 100).toFixed(1)}% probability. Unsupervised Isolation Forest evaluated deviation score at <strong>{alert.anomaly_score.toFixed(3)}</strong>.
          </p>
        </div>

        {/* Automated Playbook Mitigation */}
        {alert.mitigation_action && (
          <div className="mt-4 p-4 rounded-xl bg-cyan-950/20 border border-cyan-800/60 space-y-1.5">
            <div className="flex items-center gap-2 text-xs font-mono text-cyan-400 font-semibold">
              <ShieldCheck className="w-4 h-4" />
              Automated Mitigation Playbook
            </div>
            <p className="text-xs text-slate-300 font-mono">
              {alert.mitigation_action}
            </p>
          </div>
        )}

        {/* Analyst Notes */}
        <div className="mt-4 space-y-2">
          <label className="text-xs font-mono text-slate-400 uppercase">
            Analyst Investigation Notes:
          </label>
          <textarea
            rows={2}
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            placeholder="Add SOC investigation notes or mitigation verification details..."
            className="w-full p-2.5 rounded-lg bg-slate-900 border border-slate-800 text-xs font-mono text-slate-200 focus:outline-none focus:border-cyan-500"
          />
        </div>

        {/* Action Buttons */}
        <div className="mt-6 pt-4 border-t border-slate-800 flex flex-wrap justify-between items-center gap-3">
          <div className="text-xs font-mono text-slate-500 flex items-center gap-1.5">
            <Clock className="w-3.5 h-3.5" />
            Last detected: {alert.timestamp ? alert.timestamp.slice(0, 19).replace("T", " ") : "Just now"}
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => handleUpdate("false_positive")}
              disabled={updating}
              className="px-3 py-1.5 rounded-lg border border-slate-700 bg-slate-800 hover:bg-slate-750 text-slate-400 hover:text-slate-200 text-xs font-mono transition"
            >
              False Positive
            </button>
            <button
              onClick={() => handleUpdate("acknowledged")}
              disabled={updating}
              className="px-3 py-1.5 rounded-lg border border-amber-800 bg-amber-950/40 hover:bg-amber-950/70 text-amber-300 text-xs font-mono transition"
            >
              Acknowledge
            </button>
            <button
              onClick={() => handleUpdate("resolved")}
              disabled={updating}
              className="px-4 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-slate-950 font-bold text-xs font-mono transition flex items-center gap-1.5 shadow-[0_0_12px_rgba(16,185,129,0.3)]"
            >
              <CheckCircle2 className="w-3.5 h-3.5" />
              Mark Resolved
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
