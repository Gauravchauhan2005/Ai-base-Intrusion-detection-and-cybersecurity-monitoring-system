"use client";

import { useEffect, useRef } from "react";
import { toast } from "sonner";
import { useSecurityStore } from "@/store/useSecurityStore";
import { soundManager } from "@/lib/sound";

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000/ws/live-stream";

export function useWebSocket() {
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const pingIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const retryCountRef = useRef<number>(0);
  const lastToastRef = useRef<number>(0);

  const { setConnectionStatus, addLiveFlow, addLiveAlert, soundEnabled } = useSecurityStore();

  const connect = () => {
    try {
      setConnectionStatus(retryCountRef.current > 0 ? "RECONNECTING" : "CONNECTING");
      const ws = new WebSocket(WS_URL);
      wsRef.current = ws;

      ws.onopen = () => {
        setConnectionStatus("CONNECTED");
        retryCountRef.current = 0;

        if (pingIntervalRef.current) clearInterval(pingIntervalRef.current);
        pingIntervalRef.current = setInterval(() => {
          if (ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: "PING" }));
          }
        }, 15000);
      };

      ws.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data);
          if (payload.type === "FLOW" && payload.data) {
            addLiveFlow(payload.data);
          } else if (payload.type === "ALERT" && payload.data) {
            addLiveAlert(payload.data);

            const alertData = payload.data;
            soundManager.enabled = soundEnabled;
            if (alertData.severity === "CRITICAL" || alertData.severity === "HIGH") {
              soundManager.playCriticalAlert();
            }

            // Rate-limit toast notifications to at most 1 every 1.5 seconds to avoid flooding
            const now = Date.now();
            if (now - lastToastRef.current > 1500) {
              lastToastRef.current = now;
              const isCrit = alertData.severity === "CRITICAL";
              toast[isCrit ? "error" : "warning"](`DEFCON ALERT: ${alertData.attack_type}`, {
                description: `Src: ${alertData.src_ip} ──► Dst: ${alertData.dst_ip}:${alertData.dst_port} (${alertData.severity})`,
                duration: 4000,
                action: {
                  label: "Inspect",
                  onClick: () => {
                    useSecurityStore.getState().setSelectedAlert(alertData);
                  },
                },
              });
            }
          }
        } catch {
          // ignore parsing error
        }
      };

      ws.onclose = () => {
        setConnectionStatus("DISCONNECTED");
        if (pingIntervalRef.current) clearInterval(pingIntervalRef.current);

        const delay = Math.min(1000 * Math.pow(1.5, retryCountRef.current), 10000);
        retryCountRef.current += 1;
        reconnectTimeoutRef.current = setTimeout(() => {
          connect();
        }, delay);
      };

      ws.onerror = () => {
        ws.close();
      };
    } catch {
      setConnectionStatus("DISCONNECTED");
    }
  };

  useEffect(() => {
    connect();

    return () => {
      if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current);
      if (pingIntervalRef.current) clearInterval(pingIntervalRef.current);
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  return {
    reconnect: () => {
      retryCountRef.current = 0;
      if (wsRef.current) wsRef.current.close();
      connect();
    },
  };
}
