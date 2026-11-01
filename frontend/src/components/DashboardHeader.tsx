"use client";

import React, { useState, useEffect } from "react";
import { 
  Shield, 
  Activity, 
  RefreshCw, 
  Zap, 
  Volume2, 
  VolumeX, 
  Radio, 
  Clock, 
  Flame,
  Cpu
} from "lucide-react";
import { useSecurityStore } from "@/store/useSecurityStore";
import { soundManager } from "@/lib/sound";

interface Props {
  onOpenTrafficControl: () => void;
  onRefresh: () => void;
}

export const DashboardHeader: React.FC<Props> = ({ onOpenTrafficControl, onRefresh }) => {
  const { connectionStatus, metrics, soundEnabled, toggleSound } = useSecurityStore();
  const [currentTime, setCurrentTime] = useState<string>("");

  useEffect(() => {
    const update = () => {
      const now = new Date();
      setCurrentTime(now.toUTCString().slice(17, 25) + " UTC");
    };
    update();
    const interval = setInterval(update, 1000);
    return () => clearInterval(interval);
  }, []);

  const handleSoundToggle = () => {
    toggleSound();
    soundManager.enabled = !soundEnabled;
    if (!soundEnabled) {
      soundManager.playActionChime();
    }
  };

  // Dynamic DEFCON calculation
  const criticalCount = metrics?.critical_alerts || 0;
  const highCount = metrics?.high_alerts || 0;
  const activeCount = metrics?.active_alerts || 0;

  let defconLevel = 5;
  let defconText = "DEFCON 5 // NORMAL OPS";
  let defconColor = "text-emerald-400 border-emerald-500/40 bg-emerald-950/30";
  let defconDot = "bg-emerald-400";

  if (criticalCount > 0) {
    defconLevel = 1;
    defconText = "DEFCON 1 // MAXIMUM DANGER";
    defconColor = "text-rose-400 border-rose-500/60 bg-rose-950/60 animate-threat-pulse";
    defconDot = "bg-rose-500 animate-ping";
  } else if (highCount > 0) {
    defconLevel = 2;
    defconText = "DEFCON 2 // SEVERE THREAT";
    defconColor = "text-amber-400 border-amber-500/50 bg-amber-950/40";
    defconDot = "bg-amber-400 animate-pulse";
  } else if (activeCount > 5) {
    defconLevel = 3;
    defconText = "DEFCON 3 // ELEVATED RISK";
    defconColor = "text-yellow-400 border-yellow-500/40 bg-yellow-950/30";
    defconDot = "bg-yellow-400";
  } else if (connectionStatus === "CONNECTED") {
    defconLevel = 4;
    defconText = "DEFCON 4 // ACTIVE SENTINEL";
    defconColor = "text-cyan-400 border-cyan-500/40 bg-cyan-950/30";
    defconDot = "bg-cyan-400";
  }

  const getStatusBadge = () => {
    switch (connectionStatus) {
      case "CONNECTED":
        return (
          <div className="flex items-center gap-2 px-2.5 py-1 rounded bg-[#061325] border border-cyan-500/40 text-cyan-300 text-xs font-mono">
            <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
            LIVE STREAM
          </div>
        );
      case "CONNECTING":
      case "RECONNECTING":
        return (
          <div className="flex items-center gap-2 px-2.5 py-1 rounded bg-amber-950/60 border border-amber-500/40 text-amber-300 text-xs font-mono">
            <span className="w-2 h-2 rounded-full bg-amber-400 animate-ping"></span>
            RECONNECTING
          </div>
        );
      default:
        return (
          <div className="flex items-center gap-2 px-2.5 py-1 rounded bg-rose-950/60 border border-rose-500/40 text-rose-300 text-xs font-mono">
            <span className="w-2 h-2 rounded-full bg-rose-500"></span>
            OFFLINE
          </div>
        );
    }
  };

  return (
    <header className="border-b border-zinc-800/80 bg-[#040814]/95 backdrop-blur-md sticky top-0 z-40 px-4 sm:px-6 py-2.5">
      <div className="max-w-[1700px] mx-auto flex flex-col md:flex-row items-center justify-between gap-3">
        {/* Brand / Title */}
        <div className="flex items-center gap-3">
          <div className="relative flex items-center justify-center w-9 h-9 rounded-md bg-gradient-to-br from-cyan-950 to-slate-900 border border-cyan-500/50 shadow-[0_0_20px_rgba(6,182,212,0.2)]">
            <Shield className="w-5 h-5 text-cyan-400" />
            <span className="absolute -top-1 -right-1 w-2 h-2 bg-cyan-400 rounded-full animate-ping"></span>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-base font-extrabold tracking-wider text-slate-100 font-mono flex items-center gap-1.5">
                AETHERIS <span className="text-cyan-400">SOC</span>
              </h1>
              <span className="px-1.5 py-0.2 text-[9px] font-mono tracking-widest bg-cyan-950/70 text-cyan-300 rounded border border-cyan-800/60">
                PROD v1.0
              </span>
              <span className="hidden sm:inline-block text-[10px] text-zinc-400 font-mono bg-zinc-900/80 px-1.5 py-0.5 rounded border border-zinc-800">
                Dual ML: XGBoost + iForest
              </span>
            </div>
            <p className="text-[11px] text-zinc-400 font-mono">
              High-Velocity Network Intrusion Detection & Real-Time Incident Response
            </p>
          </div>
        </div>

        {/* Tactical HUD & Status Center */}
        <div className="flex flex-wrap items-center gap-2.5">
          {/* DEFCON Indicator */}
          <div className={`flex items-center gap-2 px-3 py-1 rounded text-xs font-mono font-bold tracking-wider border shadow-sm ${defconColor}`}>
            <span className={`w-2 h-2 rounded-full ${defconDot}`}></span>
            {defconText}
          </div>

          {/* Connection Status */}
          {getStatusBadge()}

          {/* Live Clock */}
          <div className="hidden xl:flex items-center gap-1.5 text-xs font-mono text-zinc-400 bg-zinc-900/70 px-2.5 py-1 rounded border border-zinc-800">
            <Clock className="w-3.5 h-3.5 text-zinc-500" />
            {currentTime}
          </div>

          {/* Audio Alarm Toggle */}
          <button
            onClick={handleSoundToggle}
            title={soundEnabled ? "Mute Cyber Audio Alarm" : "Enable Cyber Audio Alarm"}
            className={`p-1.5 rounded border transition text-xs font-mono flex items-center gap-1 ${
              soundEnabled
                ? "bg-cyan-950/60 border-cyan-700/60 text-cyan-300 hover:bg-cyan-900/50"
                : "bg-zinc-900 border-zinc-800 text-zinc-500 hover:text-zinc-300"
            }`}
          >
            {soundEnabled ? <Volume2 className="w-4 h-4 text-cyan-400" /> : <VolumeX className="w-4 h-4" />}
          </button>

          {/* Manual Refresh */}
          <button
            onClick={onRefresh}
            title="Refresh Metrics Snapshot"
            className="p-1.5 rounded border border-zinc-800 bg-zinc-900/80 hover:bg-zinc-800 text-zinc-400 hover:text-zinc-200 transition"
          >
            <RefreshCw className="w-4 h-4" />
          </button>

          {/* Attack Simulator Trigger */}
          <button
            onClick={onOpenTrafficControl}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-gradient-to-r from-cyan-600 via-cyan-500 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-zinc-950 font-bold text-xs font-mono transition shadow-[0_0_15px_rgba(6,182,212,0.35)] active:scale-95"
          >
            <Flame className="w-3.5 h-3.5 fill-current" />
            <span>SIMULATE ATTACK</span>
          </button>
        </div>
      </div>
    </header>
  );
};
