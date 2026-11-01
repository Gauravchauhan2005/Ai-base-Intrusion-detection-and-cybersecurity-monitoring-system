"use client";

import React, { useState, useEffect, useMemo } from "react";
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  ColumnDef,
  flexRender,
  SortingState,
} from "@tanstack/react-table";
import { Alert, Severity } from "@/types";
import { fetchAlerts, updateAlertStatus } from "@/lib/api";
import { getSeverityColor } from "@/lib/utils";
import { Search, Filter, CheckCircle2, Eye, ShieldAlert, ChevronLeft, ChevronRight } from "lucide-react";
import { useSecurityStore } from "@/store/useSecurityStore";

interface Props {
  onSelectAlert: (alert: Alert) => void;
}

export const AlertsDataTable: React.FC<Props> = ({ onSelectAlert }) => {
  const [data, setData] = useState<Alert[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [sorting, setSorting] = useState<SortingState>([{ id: "timestamp", desc: true }]);
  const [globalFilter, setGlobalFilter] = useState<string>("");
  const [selectedSeverity, setSelectedSeverity] = useState<string>("ALL");
  const [selectedStatus, setSelectedStatus] = useState<string>("ALL");
  const [page, setPage] = useState<number>(1);
  const [pageSize, setPageSize] = useState<number>(10);
  const [totalCount, setTotalCount] = useState<number>(0);

  const { liveAlerts } = useSecurityStore();

  const loadAlerts = async () => {
    try {
      setLoading(true);
      const res = await fetchAlerts({
        page,
        pageSize,
        severity: selectedSeverity !== "ALL" ? selectedSeverity : undefined,
        status: selectedStatus !== "ALL" ? selectedStatus : undefined,
        search: globalFilter || undefined,
      });
      setData(res.items);
      setTotalCount(res.total);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAlerts();
  }, [page, pageSize, selectedSeverity, selectedStatus]);

  // If new live alerts arrive from WebSocket, prepend to current view if on page 1
  useEffect(() => {
    if (liveAlerts.length > 0 && page === 1) {
      setData((prev) => {
        const combined = [...liveAlerts, ...prev];
        // Deduplicate by alert_id
        const unique = Array.from(new Map(combined.map((item) => [item.alert_id, item])).values());
        return unique.slice(0, pageSize);
      });
    }
  }, [liveAlerts]);

  const handleStatusChange = async (alertId: string, newStatus: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      const updated = await updateAlertStatus(alertId, newStatus);
      setData((prev) => prev.map((a) => (a.alert_id === alertId ? { ...a, status: updated.status } : a)));
    } catch (err) {
      console.error(err);
    }
  };

  const columns = useMemo<ColumnDef<Alert>[]>(
    () => [
      {
        accessorKey: "severity",
        header: "Severity",
        cell: (info) => {
          const val = info.getValue() as string;
          const styling = getSeverityColor(val);
          return (
            <span className={`px-2 py-0.5 rounded-full text-[10px] font-mono font-bold border uppercase ${styling.badge}`}>
              {val}
            </span>
          );
        },
      },
      {
        accessorKey: "attack_type",
        header: "Attack Vector",
        cell: (info) => (
          <span className="font-mono text-xs font-semibold text-slate-200">
            {info.getValue() as string}
          </span>
        ),
      },
      {
        accessorKey: "src_ip",
        header: "Attacker IP",
        cell: (info) => (
          <span className="font-mono text-xs text-rose-400">
            {info.getValue() as string}
          </span>
        ),
      },
      {
        accessorKey: "dst_port",
        header: "Target Port",
        cell: (info) => (
          <span className="font-mono text-xs text-cyan-400">
            :{info.getValue() as number}
          </span>
        ),
      },
      {
        accessorKey: "confidence",
        header: "Confidence",
        cell: (info) => {
          const conf = info.getValue() as number;
          return (
            <span className="font-mono text-xs text-slate-300">
              {(conf * 100).toFixed(1)}%
            </span>
          );
        },
      },
      {
        accessorKey: "hit_count",
        header: "Aggregated Hits",
        cell: (info) => (
          <span className="px-2 py-0.5 rounded bg-slate-800 border border-slate-700 font-mono text-xs text-slate-200 font-bold">
            {info.getValue() as number} pkts
          </span>
        ),
      },
      {
        accessorKey: "status",
        header: "Status",
        cell: (info) => {
          const st = info.getValue() as string;
          const badgeClass =
            st === "new"
              ? "bg-rose-950/60 border-rose-800 text-rose-400"
              : st === "acknowledged"
              ? "bg-amber-950/60 border-amber-800 text-amber-400"
              : "bg-emerald-950/60 border-emerald-800 text-emerald-400";
          return (
            <span className={`px-2 py-0.5 rounded text-[10px] font-mono border uppercase ${badgeClass}`}>
              {st}
            </span>
          );
        },
      },
      {
        id: "actions",
        header: "Action",
        cell: ({ row }) => {
          const alert = row.original;
          return (
            <div className="flex items-center gap-1.5" onClick={(e) => e.stopPropagation()}>
              {alert.status === "new" && (
                <button
                  onClick={(e) => handleStatusChange(alert.alert_id, "acknowledged", e)}
                  className="px-2 py-0.5 text-[10px] font-mono rounded bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition"
                  title="Acknowledge alert"
                >
                  ACK
                </button>
              )}
              {alert.status !== "resolved" && (
                <button
                  onClick={(e) => handleStatusChange(alert.alert_id, "resolved", e)}
                  className="px-2 py-0.5 text-[10px] font-mono rounded bg-emerald-950/60 hover:bg-emerald-900 border border-emerald-800 text-emerald-300 transition"
                  title="Mark as resolved"
                >
                  Resolve
                </button>
              )}
              <button
                onClick={() => onSelectAlert(alert)}
                className="p-1 rounded text-slate-400 hover:text-cyan-400 transition"
                title="Inspect Alert"
              >
                <Eye className="w-3.5 h-3.5" />
              </button>
            </div>
          );
        },
      },
    ],
    []
  );

  const table = useReactTable({
    data,
    columns,
    state: { sorting },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    manualPagination: true,
  });

  const totalPages = Math.ceil(totalCount / pageSize) || 1;

  return (
    <div className="rounded-xl border border-slate-800 bg-[#090d16]/90 p-5 shadow-lg backdrop-blur-sm">
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between pb-4 border-b border-slate-800/80 gap-3">
        <div className="flex items-center gap-2.5">
          <div className="p-1.5 rounded-lg bg-rose-950/60 border border-rose-800/50 text-rose-400">
            <ShieldAlert className="w-4 h-4" />
          </div>
          <div>
            <h2 className="text-sm font-semibold font-mono uppercase tracking-wider text-slate-200">
              Security Incidents & Detections
            </h2>
            <p className="text-xs text-slate-400 font-mono">
              TanStack Table with deduplicated threat streams & status workflows
            </p>
          </div>
        </div>

        {/* Filter controls */}
        <div className="flex flex-wrap items-center gap-2.5 w-full md:w-auto">
          {/* Search */}
          <div className="relative flex-1 md:w-48">
            <Search className="absolute left-2.5 top-2.5 w-3.5 h-3.5 text-slate-500" />
            <input
              type="text"
              placeholder="Search IP or ID..."
              value={globalFilter}
              onChange={(e) => setGlobalFilter(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && loadAlerts()}
              className="w-full pl-8 pr-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs font-mono text-slate-200 focus:outline-none focus:border-cyan-500"
            />
          </div>

          {/* Severity Filter */}
          <select
            value={selectedSeverity}
            onChange={(e) => {
              setSelectedSeverity(e.target.value);
              setPage(1);
            }}
            className="px-2.5 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs font-mono text-slate-300 focus:outline-none focus:border-cyan-500"
          >
            <option value="ALL">All Severities</option>
            <option value="CRITICAL">Critical</option>
            <option value="HIGH">High</option>
            <option value="MEDIUM">Medium</option>
            <option value="LOW">Low</option>
          </select>

          {/* Status Filter */}
          <select
            value={selectedStatus}
            onChange={(e) => {
              setSelectedStatus(e.target.value);
              setPage(1);
            }}
            className="px-2.5 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs font-mono text-slate-300 focus:outline-none focus:border-cyan-500"
          >
            <option value="ALL">All Status</option>
            <option value="new">New</option>
            <option value="acknowledged">Acknowledged</option>
            <option value="resolved">Resolved</option>
          </select>
        </div>
      </div>

      {/* Table */}
      <div className="mt-4 overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id} className="border-b border-slate-800 bg-[#0b101d] text-slate-400 font-mono text-xs">
                {headerGroup.headers.map((header) => (
                  <th key={header.id} className="py-2.5 px-3">
                    {flexRender(header.column.columnDef.header, header.getContext())}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody className="divide-y divide-slate-850 font-mono text-xs">
            {data.length === 0 ? (
              <tr>
                <td colSpan={columns.length} className="py-8 text-center text-slate-500 font-mono">
                  {loading ? "Loading security incidents..." : "No active threats matching current filters."}
                </td>
              </tr>
            ) : (
              table.getRowModel().rows.map((row) => (
                <tr
                  key={row.id}
                  onClick={() => onSelectAlert(row.original)}
                  className="hover:bg-slate-800/40 cursor-pointer transition-colors"
                >
                  {row.getVisibleCells().map((cell) => (
                    <td key={cell.id} className="py-2.5 px-3 whitespace-nowrap">
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs font-mono text-slate-400">
        <div>
          Showing {data.length} of {totalCount} total alerts
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            disabled={page <= 1}
            className="p-1 rounded border border-slate-800 bg-slate-900 disabled:opacity-40 hover:bg-slate-800 text-slate-300"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>
          <span>
            Page {page} of {totalPages}
          </span>
          <button
            onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
            disabled={page >= totalPages}
            className="p-1 rounded border border-slate-800 bg-slate-900 disabled:opacity-40 hover:bg-slate-800 text-slate-300"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};
