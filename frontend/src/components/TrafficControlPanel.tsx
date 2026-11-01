"use client";

import React, { useState } from "react";
import { X, Play, Pause, Flame, Skull, KeyRound, Bug, Check } from "lucide-react";
import { controlTraffic } from "@/lib/api";
import { useSecurityStore } from "@/store/useSecurityStore";

interface Props {
  isOpen: boolean;
  onClose: () => void;
}

export const TrafficControlPanel: React.FC<Props> = ({ isOpen, onClose }) => {
  const { simulationRate, setSimulationRate } = useSecurityStore();
  const [rate, setRate] = useState<number>(simulationRate);
  const [isInjecting, setIsInjecting] = useState<string | null>(null);
  const [statusMsg, setStatusMsg] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleRateUpdate = async (newRate: number) => {
    setRate(newRate);
    setSimulationRate(newRate);
    try {
      await controlTraffic({ rate_eps: newRate });
      showStatus(`Replay rate set to ${newRate} EPS`);
    } catch (err) {
      console.error(err);
    }
  };

  const handleInjectAttack = async (attackType: string, burstCount: number = 40) => {
    try {
      setIsInjecting(attackType);
      await controlTraffic({ burst_attack: attackType, burst_count: burstCount });
      showStatus(`Injected ${burstCount} packets of ${attackType}!`);
    } catch (err) {
      console.error(err);
    } finally {
      setIsInjecting(null);
    }
  };

  const showStatus = (msg: string) => {
    setStatusMsg(msg);
    setTimeout(() => setStatusMsg(null), 3500);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
      <div className="w-full max-w-lg rounded-2xl border border-slate-700 bg-[#090d16] p-6 shadow-2xl">
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div>
            <h3 className="text-base font-bold font-mono text-slate-100 uppercase tracking-wider flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-cyan-400"></span>
              Traffic Simulation Controller
            </h3>
            <p className="text-xs text-slate-400 font-mono mt-0.5">
              Live replay rate modulation & attack vector injection
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg border border-slate-800 bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-slate-200 transition"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {statusMsg && (
          <div className="mt-4 p-2.5 rounded-lg bg-cyan-950/60 border border-cyan-800/80 text-cyan-300 text-xs font-mono flex items-center gap-2">
            <Check className="w-4 h-4 text-cyan-400" />
            {statusMsg}
          </div>
        )}

        {/* EPS Slider */}
        <div className="mt-5 space-y-2">
          <div className="flex justify-between items-center text-xs font-mono">
            <span className="text-slate-300">Throughput Target:</span>
            <span className="text-cyan-400 font-bold text-sm">{rate} EPS</span>
          </div>
          <input
            type="range"
            min="10"
            max="300"
            step="10"
            value={rate}
            onChange={(e) => handleRateUpdate(Number(e.target.value))}
            className="w-full accent-cyan-500 cursor-pointer h-2 bg-slate-800 rounded-lg"
          />
          <div className="flex justify-between text-[10px] font-mono text-slate-500">
            <span>10 EPS (Low)</span>
            <span>100 EPS (Normal)</span>
            <span>300 EPS (High)</span>
          </div>
        </div>

        {/* Quick Attack Injection Grid */}
        <div className="mt-6">
          <h4 className="text-xs font-mono text-slate-400 uppercase tracking-wider mb-3">
            On-Demand Attack Burst Injection
          </h4>
          <div className="grid grid-cols-2 gap-3">
            <button
              onClick={() => handleInjectAttack("DDoS-LOIC-HTTP", 50)}
              disabled={isInjecting !== null}
              className="flex items-center gap-2.5 p-3 rounded-xl border border-rose-800/60 bg-rose-950/20 hover:bg-rose-950/40 text-rose-300 text-xs font-mono font-medium transition text-left"
            >
              <Flame className="w-4 h-4 text-rose-400 shrink-0" />
              <div>
                <div className="font-bold">DDoS LOIC Flood</div>
                <div className="text-[10px] text-rose-400/80">50 High-rate flows</div>
              </div>
            </button>

            <button
              onClick={() => handleInjectAttack("DoS-Hulk", 40)}
              disabled={isInjecting !== null}
              className="flex items-center gap-2.5 p-3 rounded-xl border border-rose-800/60 bg-rose-950/20 hover:bg-rose-950/40 text-rose-300 text-xs font-mono font-medium transition text-left"
            >
              <Skull className="w-4 h-4 text-rose-400 shrink-0" />
              <div>
                <div className="font-bold">DoS Hulk Attack</div>
                <div className="text-[10px] text-rose-400/80">HTTP Port 80 flood</div>
              </div>
            </button>

            <button
              onClick={() => handleInjectAttack("Botnet", 30)}
              disabled={isInjecting !== null}
              className="flex items-center gap-2.5 p-3 rounded-xl border border-purple-800/60 bg-purple-950/20 hover:bg-purple-950/40 text-purple-300 text-xs font-mono font-medium transition text-left"
            >
              <Bug className="w-4 h-4 text-purple-400 shrink-0" />
              <div>
                <div className="font-bold">Botnet C2 Beacons</div>
                <div className="text-[10px] text-purple-400/80">Port 6667 / 8080</div>
              </div>
            </button>

            <button
              onClick={() => handleInjectAttack("SSH-Bruteforce", 35)}
              disabled={isInjecting !== null}
              className="flex items-center gap-2.5 p-3 rounded-xl border border-amber-800/60 bg-amber-950/20 hover:bg-amber-950/40 text-amber-300 text-xs font-mono font-medium transition text-left"
            >
              <KeyRound className="w-4 h-4 text-amber-400 shrink-0" />
              <div>
                <div className="font-bold">SSH Bruteforce</div>
                <div className="text-[10px] text-amber-400/80">Credential stuffing</div>
              </div>
            </button>
          </div>
        </div>

        <div className="mt-6 pt-4 border-t border-slate-800 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-mono font-semibold transition"
          >
            Close Controller
          </button>
        </div>
      </div>
    </div>
  );
};
