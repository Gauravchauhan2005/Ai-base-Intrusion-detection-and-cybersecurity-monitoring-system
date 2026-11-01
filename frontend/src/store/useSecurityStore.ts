import { create } from "zustand";
import { Alert, FlowEvent, MetricsSummary, TimeSeriesPoint, ConnectionStatus } from "@/types";

export type TabType = "operations" | "forensics" | "models" | "mitigation";

interface SecurityState {
  activeTab: TabType;
  connectionStatus: ConnectionStatus;
  isLivePaused: boolean;
  soundEnabled: boolean;
  liveFlows: FlowEvent[];
  liveAlerts: Alert[];
  metrics: MetricsSummary | null;
  timeSeries: TimeSeriesPoint[];
  selectedAlert: Alert | null;
  forensicTarget: (FlowEvent | Alert) | null;
  simulationRate: number;

  setActiveTab: (tab: TabType) => void;
  setConnectionStatus: (status: ConnectionStatus) => void;
  togglePauseLive: () => void;
  toggleSound: () => void;
  addLiveFlow: (flow: FlowEvent) => void;
  addLiveAlert: (alert: Alert) => void;
  setMetrics: (metrics: MetricsSummary) => void;
  setTimeSeries: (points: TimeSeriesPoint[]) => void;
  addTimeSeriesPoint: (point: TimeSeriesPoint) => void;
  setSelectedAlert: (alert: Alert | null) => void;
  setForensicTarget: (target: (FlowEvent | Alert) | null) => void;
  setSimulationRate: (rate: number) => void;
  clearLiveStreams: () => void;
}

export const useSecurityStore = create<SecurityState>((set) => ({
  activeTab: "operations",
  connectionStatus: "DISCONNECTED",
  isLivePaused: false,
  soundEnabled: true,
  liveFlows: [],
  liveAlerts: [],
  metrics: null,
  timeSeries: [],
  selectedAlert: null,
  forensicTarget: null,
  simulationRate: 25,

  setActiveTab: (tab) => set({ activeTab: tab }),

  setConnectionStatus: (status) => set({ connectionStatus: status }),

  togglePauseLive: () => set((state) => ({ isLivePaused: !state.isLivePaused })),

  toggleSound: () => set((state) => ({ soundEnabled: !state.soundEnabled })),

  addLiveFlow: (flow) =>
    set((state) => {
      if (state.isLivePaused) return state;
      const updated = [flow, ...state.liveFlows.slice(0, 49)];
      return { liveFlows: updated };
    }),

  addLiveAlert: (alert) =>
    set((state) => {
      const existingIdx = state.liveAlerts.findIndex((a) => a.alert_id === alert.alert_id);
      if (existingIdx !== -1) {
        const copy = [...state.liveAlerts];
        copy[existingIdx] = { ...copy[existingIdx], ...alert };
        return { liveAlerts: copy };
      }
      const updated = [alert, ...state.liveAlerts.slice(0, 49)];
      return { liveAlerts: updated };
    }),

  setMetrics: (metrics) => set({ metrics }),

  setTimeSeries: (timeSeries) => set({ timeSeries }),

  addTimeSeriesPoint: (point) =>
    set((state) => {
      const copy = [...state.timeSeries.slice(-44), point];
      return { timeSeries: copy };
    }),

  setSelectedAlert: (selectedAlert) => set({ selectedAlert }),

  setForensicTarget: (forensicTarget) => set({ forensicTarget }),

  setSimulationRate: (rate) => set({ simulationRate: rate }),

  clearLiveStreams: () => set({ liveFlows: [], liveAlerts: [] }),
}));
