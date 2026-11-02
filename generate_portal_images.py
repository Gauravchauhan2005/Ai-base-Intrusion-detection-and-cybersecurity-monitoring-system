import os
import shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

OUTPUT_DIR = "portal_diagrams"
os.makedirs(OUTPUT_DIR, exist_ok=True)

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

# ----------------------------------------------------------------------
# 1. DATA FLOW DESIGN DIAGRAM
# ----------------------------------------------------------------------
def generate_data_flow_design():
    fig, ax = plt.subplots(figsize=(13, 8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Header
    ax.text(50, 96.5, "AETHERIS SOC: End-to-End Data Flow Design & Pipeline Architecture",
            ha='center', va='center', fontsize=15, fontweight='bold', color='#0F172A')
    ax.text(50, 93, "Continuous Ingestion, Message Buffering, Dual ML Inference, Deduplication, and Multi-Sink Output",
            ha='center', va='center', fontsize=9.5, color='#475569')

    # Step 1: Traffic Producer (Left)
    b1 = patches.FancyBboxPatch((3, 44), 18, 42, boxstyle="round,pad=0.8,rounding_size=1.5",
                                edgecolor='#0284C7', facecolor='#F0F9FF', linewidth=1.8)
    ax.add_patch(b1)
    ax.text(12, 82, "1. INGESTION TIER", ha='center', va='center', fontsize=10, fontweight='bold', color='#0369A1')
    ax.text(12, 75, "Traffic Producer\n& Replay Engine", ha='center', va='center', fontsize=9, fontweight='bold', color='#0F172A')
    ax.text(12, 60, "• CIC-IDS-2018 NetFlow\n• Continuous 25-300+ EPS\n• On-Demand Attack Bursts:\n  - DDoS LOIC/HOIC\n  - DoS Hulk Flood\n  - Botnet Ares C2\n  - SSH-Bruteforce\n  - Infiltration\n• Serializes JSON flows",
            ha='center', va='center', fontsize=7.8, color='#1E293B', linespacing=1.3)

    # Step 2: Redis Streams Broker
    b2 = patches.FancyBboxPatch((24.5, 44), 16.5, 42, boxstyle="round,pad=0.8,rounding_size=1.5",
                                edgecolor='#6366F1', facecolor='#EEF2FF', linewidth=1.8)
    ax.add_patch(b2)
    ax.text(32.75, 82, "2. STREAMING TIER", ha='center', va='center', fontsize=10, fontweight='bold', color='#4338CA')
    ax.text(32.75, 75, "Redis Streams Broker\n(Key: network_flows)", ha='center', va='center', fontsize=9, fontweight='bold', color='#0F172A')
    ax.text(32.75, 60, "• Decoupled Ingestion\n• Consumer Groups:\n  'ids_inference_group'\n• Backpressure Shock\n  Absorption Buffer\n• Zero Packet Dropping\n• At-Least-Once Delivery\n• Acknowledged: XACK",
            ha='center', va='center', fontsize=7.8, color='#1E293B', linespacing=1.3)

    # Step 3: FastAPI Inference & Dual ML Engine (Center)
    b3 = patches.FancyBboxPatch((44.5, 40), 28, 48, boxstyle="round,pad=0.8,rounding_size=1.5",
                                edgecolor='#059669', facecolor='#ECFDF5', linewidth=1.8)
    ax.add_patch(b3)
    ax.text(58.5, 84.5, "3. INFERENCE & INTELLIGENCE TIER", ha='center', va='center', fontsize=10, fontweight='bold', color='#047857')
    ax.text(58.5, 80.5, "FastAPI Asynchronous Consumer Engine", ha='center', va='center', fontsize=8.8, fontweight='bold', color='#065F46')

    # Sub-box 3.1: Preprocessor
    sub1 = patches.FancyBboxPatch((46.5, 68), 24, 9, boxstyle="round,pad=0.5,rounding_size=1.0",
                                  edgecolor='#059669', facecolor='#FFFFFF', linewidth=1.2)
    ax.add_patch(sub1)
    ax.text(58.5, 74, "38-Feature Preprocessing Pipeline", ha='center', va='center', fontsize=8.2, fontweight='bold', color='#065F46')
    ax.text(58.5, 70, "Strip IPs/Ports | Median Impute | MinMax Scaler", ha='center', va='center', fontsize=7.2, color='#334155')

    # Sub-box 3.2: Dual ML Scoring
    sub2 = patches.FancyBboxPatch((46.5, 52), 24, 13.5, boxstyle="round,pad=0.5,rounding_size=1.0",
                                  edgecolor='#059669', facecolor='#FFFFFF', linewidth=1.2)
    ax.add_patch(sub2)
    ax.text(58.5, 62, "Dual-Engine Machine Learning Scoring", ha='center', va='center', fontsize=8.2, fontweight='bold', color='#065F46')
    ax.text(58.5, 56.5, "• Supervised XGBoost (Multi-Class 6 labels)\n• Unsupervised Isolation Forest (Score s < 0.0)\n• Severity Mapping: CRITICAL / HIGH / MED / LOW",
            ha='center', va='center', fontsize=7.2, color='#1E293B', linespacing=1.25)

    # Sub-box 3.3: In-Memory Deduplication
    sub3 = patches.FancyBboxPatch((46.5, 42), 24, 7.5, boxstyle="round,pad=0.5,rounding_size=1.0",
                                  edgecolor='#D97706', facecolor='#FFFBEB', linewidth=1.2)
    ax.add_patch(sub3)
    ax.text(58.5, 45.75, "5s In-Memory Sliding Deduplicator\nMD5(src_ip + dst_ip + attack_type) -> 96.4% Suppress",
            ha='center', va='center', fontsize=7.2, fontweight='bold', color='#B45309')

    # Step 4: Sinks & Outputs (Right)
    # Sink A: PostgreSQL Database
    b4a = patches.FancyBboxPatch((76, 67), 21, 21, boxstyle="round,pad=0.8,rounding_size=1.5",
                                 edgecolor='#334155', facecolor='#F8FAFC', linewidth=1.8)
    ax.add_patch(b4a)
    ax.text(86.5, 84, "4. PERSISTENCE SINK", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1E293B')
    ax.text(86.5, 79.5, "PostgreSQL 16 Database", ha='center', va='center', fontsize=8.8, fontweight='bold', color='#0284C7')
    ax.text(86.5, 72.5, "• 'security_alerts' Table (Deduped)\n• 'network_events' Table (Auditing)\n• 'ml_models' Table (Governance)\n• JSONB Raw Feature Forensics",
            ha='center', va='center', fontsize=7.5, color='#334155', linespacing=1.3)

    # Sink B: WebSocket & Next.js SOC Dashboard
    b4b = patches.FancyBboxPatch((76, 40), 21, 23, boxstyle="round,pad=0.8,rounding_size=1.5",
                                 edgecolor='#BE123C', facecolor='#FFF1F2', linewidth=1.8)
    ax.add_patch(b4b)
    ax.text(86.5, 59, "5. VISUALIZATION SINK", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#9F1239')
    ax.text(86.5, 54.5, "Next.js 14 SOC Dashboard", ha='center', va='center', fontsize=8.8, fontweight='bold', color='#BE123C')
    ax.text(86.5, 46.5, "• Persistent WebSockets (wss://)\n• DEFCON Threat Posture HUD (5-1)\n• TanStack Table Real-Time Triage\n• 38-Feature Forensic Drawer\n• Recharts Live Throughput & P95",
            ha='center', va='center', fontsize=7.5, color='#881337', linespacing=1.3)

    # Step 5: Active Defense & eBPF Engine (Bottom Banner)
    b5 = patches.FancyBboxPatch((15, 12), 70, 20, boxstyle="round,pad=0.8,rounding_size=1.5",
                                edgecolor='#D97706', facecolor='#FEF3C7', linewidth=1.8)
    ax.add_patch(b5)
    ax.text(50, 28, "6. ACTIVE MITIGATION & HARDWARE DEFENSE FEEDBACK LOOP", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#B45309')
    ax.text(50, 23.5, "• Automated Firewall Policy Synchronization: POST /api/mitigation/block", ha='center', va='center', fontsize=8.5, color='#78350F')
    ax.text(50, 19.5, "• Software-Defined eBPF / XDP Line-Rate Packet Drop Rules Applied at NIC Driver Layer", ha='center', va='center', fontsize=8.5, color='#78350F')
    ax.text(50, 15.5, "• Operator Override: 1-Click IP Unblock and Manual Rule Flush Controls", ha='center', va='center', fontsize=8.5, color='#78350F')

    # Connective Arrows
    arr = dict(arrowstyle="->", lw=2.0, color='#0F172A', mutation_scale=15)
    # P1 -> P2
    ax.annotate("", xy=(24.5, 65), xytext=(21, 65), arrowprops=arr)
    ax.text(22.75, 67, "Flow JSON", ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#475569')

    # P2 -> P3
    ax.annotate("", xy=(44.5, 65), xytext=(41, 65), arrowprops=arr)
    ax.text(42.75, 67, "XREADGROUP", ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#475569')

    # P3 -> DB
    ax.annotate("", xy=(76, 76), xytext=(72.5, 70), arrowprops=arr)
    ax.text(74.5, 75, "SQL INSERT", ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#0284C7')

    # P3 -> WS / Dashboard
    ax.annotate("", xy=(76, 52), xytext=(72.5, 52), arrowprops=arr)
    ax.text(74.5, 54, "WebSocket", ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#BE123C')

    # P3 -> Mitigation Loop
    ax.annotate("", xy=(50, 32), xytext=(50, 40), arrowprops=dict(arrowstyle="->", lw=1.8, color='#B45309', mutation_scale=13))
    ax.annotate("", xy=(86.5, 32), xytext=(86.5, 40), arrowprops=dict(arrowstyle="->", lw=1.5, color='#B45309', linestyle='dashed', mutation_scale=12))
    ax.text(86.5, 36, "Manual Block", ha='left', va='center', fontsize=7.5, color='#B45309', fontweight='bold')

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "1_data_flow_design.png")
    plt.savefig(path, dpi=300)
    plt.close()
    print(f"Generated: {path}")

# ----------------------------------------------------------------------
# 2. TESTING METHODOLOGY DIAGRAM
# ----------------------------------------------------------------------
def generate_testing_methodology():
    fig, ax = plt.subplots(figsize=(13, 8.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(50, 97, "AETHERIS SOC: Quality Assurance & Testing Methodology Framework",
            ha='center', va='center', fontsize=15, fontweight='bold', color='#0F172A')
    ax.text(50, 93.5, "Multi-Tier Automated Test Pyramid, CI/CD Gateways, and Continuous Benchmark Verification",
            ha='center', va='center', fontsize=9.5, color='#475569')

    # 5 Tiers of Pyramid (Left to Right / Vertical Stack)
    tiers = [
        ("Tier 5: Load & Stress Benchmarking", "load_test.py — Sustained 100+ EPS throughput, P50/P95/P99 latency SLA verification", 48, 18, "#BE123C", "#FFE4E6"),
        ("Tier 4: End-to-End Pipeline Integration", "test_stream_flow.py — Producer -> Redis Streams -> FastAPI Consumer -> PostgreSQL", 60, 32, "#D97706", "#FEF3C7"),
        ("Tier 3: REST & WebSocket API Testing", "test_api.py — Health status, alert pagination, model governance, WebSocket frame schemas", 72, 46, "#059669", "#ECFDF5"),
        ("Tier 2: Model Inference & Alert Logic Testing", "test_inference.py & test_alert_logic.py — Pre-warming, dual scoring, 5s deduplication logic", 84, 60, "#6366F1", "#EEF2FF"),
        ("Tier 1: Unit & Preprocessing Testing", "test_preprocessor.py — 38-feature dimensions, NaN median fill, Inf clipping, identity masking", 96, 74, "#0284C7", "#F0F9FF")
    ]

    for title, desc, width, y_pos, border_c, bg_c in tiers:
        x_pos = (100 - width) / 2
        box = patches.FancyBboxPatch((x_pos, y_pos), width, 10.5, boxstyle="round,pad=0.4,rounding_size=1.0",
                                     edgecolor=border_c, facecolor=bg_c, linewidth=1.6)
        ax.add_patch(box)
        ax.text(50, y_pos + 7.2, title, ha='center', va='center', fontsize=9.2, fontweight='bold', color=border_c)
        ax.text(50, y_pos + 3.2, desc, ha='center', va='center', fontsize=7.8, color='#1E293B')

    # Quality Gate Indicators on Left & Right
    ax.annotate("", xy=(1.5, 84), xytext=(1.5, 18),
                arrowprops=dict(arrowstyle="->", lw=2.2, color='#475569', mutation_scale=15))
    ax.text(3.5, 51, "Testing Scope & Execution Realism", rotation=90, ha='center', va='center', fontsize=9.0, fontweight='bold', color='#334155')

    ax.annotate("", xy=(98.5, 18), xytext=(98.5, 84),
                arrowprops=dict(arrowstyle="->", lw=2.2, color='#475569', mutation_scale=15))
    ax.text(96.5, 51, "Execution Velocity & Frequency", rotation=-90, ha='center', va='center', fontsize=9.0, fontweight='bold', color='#334155')

    # Methodology Lifecycle Process Flow (Bottom Ribbon)
    b_proc = patches.FancyBboxPatch((8, 3.5), 84, 10.5, boxstyle="round,pad=0.5,rounding_size=1.0",
                                   edgecolor='#059669', facecolor='#F0FDF4', linewidth=1.5)
    ax.add_patch(b_proc)
    ax.text(50, 11, "AUTOMATED CI/CD VERIFICATION GATEWAY & VALIDATION PIPELINE", ha='center', va='center', fontsize=9.2, fontweight='bold', color='#047857')
    ax.text(50, 6.5, "Code Commit ──► Pytest Unit Suite ──► ML Inference Benchmark ──► End-to-End Stream Test ──► 100% Pass Required for Production Deploy",
            ha='center', va='center', fontsize=7.8, color='#065F46', fontweight='bold')

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "2_testing_methodology.png")
    plt.savefig(path, dpi=300)
    plt.close()
    print(f"Generated: {path}")

# ----------------------------------------------------------------------
# 3. TEST CASES RESULTS & OUTPUTS (MULTI-PANEL DASHBOARD)
# ----------------------------------------------------------------------
def generate_test_cases_results_and_outputs():
    fig = plt.figure(figsize=(14, 9), dpi=300)
    gs = fig.add_gridspec(2, 2, hspace=0.32, wspace=0.25, left=0.06, right=0.94, top=0.91, bottom=0.06)

    fig.suptitle("AETHERIS SOC: Comprehensive Test Cases Results & Quantitative Benchmark Outputs",
                 fontsize=15, fontweight='bold', color='#0F172A', y=0.97)

    # ------------------------------------------------------------------
    # Panel 1: Per-Class Classification Performance (Top Left)
    # ------------------------------------------------------------------
    ax1 = fig.add_subplot(gs[0, 0])
    classes = ["Benign", "Botnet", "DDoS-LOIC", "DoS-Hulk", "Infiltration", "SSH-Bruteforce"]
    f1_scores = [1.00, 0.99, 1.00, 0.99, 0.98, 1.00]
    accuracy = [0.999, 0.997, 0.999, 0.998, 0.985, 0.999]

    x = np.arange(len(classes))
    width = 0.35

    rects1 = ax1.bar(x - width/2, f1_scores, width, label='F1-Score', color='#0284C7', edgecolor='#0369A1')
    rects2 = ax1.bar(x + width/2, accuracy, width, label='Accuracy', color='#10B981', edgecolor='#059669')

    ax1.set_title("Panel A: Per-Class Classification Metrics (Held-out Test Set)", fontsize=10.5, fontweight='bold', color='#1E293B', pad=10)
    ax1.set_ylabel("Score Ratio", fontsize=9, fontweight='bold', color='#334155')
    ax1.set_xticks(x)
    ax1.set_xticklabels(classes, rotation=25, ha='right', fontsize=8.5)
    ax1.set_ylim(0.95, 1.01)
    ax1.legend(loc='lower left', fontsize=8.5, framealpha=0.9)
    ax1.grid(axis='y', linestyle='--', alpha=0.5)

    # Highlight Overall Badge
    ax1.text(0.98, 0.08, "Overall Accuracy: 99.80%\nMacro F1: 1.00 | FPR: 0.00%",
             transform=ax1.transAxes, ha='right', va='bottom', fontsize=8.2, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#ECFDF5', edgecolor='#059669', lw=1.2))

    # ------------------------------------------------------------------
    # Panel 2: Inference Latency Percentiles Curve (Top Right)
    # ------------------------------------------------------------------
    ax2 = fig.add_subplot(gs[0, 1])
    percentiles = ["P10", "P25", "P50\n(Median)", "P75", "P90", "P95", "P99"]
    latencies = [13.2, 14.1, 14.95, 15.6, 16.1, 16.41, 19.05]

    ax2.plot(percentiles, latencies, marker='o', linewidth=2.4, color='#6366F1', markersize=6.5, label='Measured Latency')
    ax2.axhline(y=20.0, color='#EF4444', linestyle='--', linewidth=1.8, label='Real-Time SLA Budget (<20ms)')

    for i, (p, lat) in enumerate(zip(percentiles, latencies)):
        ax2.annotate(f"{lat:.1f}ms", (p, lat), textcoords="offset points", xytext=(0, 7),
                     ha='center', fontsize=8, fontweight='bold', color='#312E81')

    ax2.set_title("Panel B: Inference Latency Percentiles (tests/load_test.py)", fontsize=10.5, fontweight='bold', color='#1E293B', pad=10)
    ax2.set_ylabel("Latency (milliseconds)", fontsize=9, fontweight='bold', color='#334155')
    ax2.set_ylim(11, 22)
    ax2.legend(loc='upper left', fontsize=8.5, framealpha=0.9)
    ax2.grid(True, linestyle='--', alpha=0.5)

    ax2.text(0.98, 0.08, "Mean Latency: 15.19 ms\nP95: 16.41 ms (SLA Passed)",
             transform=ax2.transAxes, ha='right', va='bottom', fontsize=8.2, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#EEF2FF', edgecolor='#4338CA', lw=1.2))

    # ------------------------------------------------------------------
    # Panel 3: In-Memory Alert Deduplication Suppression Ratio (Bottom Left)
    # ------------------------------------------------------------------
    ax3 = fig.add_subplot(gs[1, 0])
    scenarios = ["Without Deduplication\n(Legacy S-IDS / Naive)", "With 5s Sliding Deduplication\n(AETHERIS SOC)"]
    db_writes = [500, 18] # 96.4% reduction
    colors = ['#F43F5E', '#10B981']

    bars = ax3.bar(scenarios, db_writes, color=colors, width=0.45, edgecolor=['#BE123C', '#047857'], lw=1.5)
    ax3.set_title("Panel C: Database Write Pressure During 500-Packet Flood", fontsize=10.5, fontweight='bold', color='#1E293B', pad=10)
    ax3.set_ylabel("PostgreSQL Database Writes", fontsize=9, fontweight='bold', color='#334155')
    ax3.set_ylim(0, 560)
    ax3.grid(axis='y', linestyle='--', alpha=0.5)

    for bar, val in zip(bars, db_writes):
        yval = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2.0, yval + 14, f"{val} writes", ha='center', va='bottom', fontsize=8.8, fontweight='bold')

    ax3.annotate("96.4% Write Reduction\nSuppresses Alert Fatigue!",
                 xy=(1, 30), xytext=(0.48, 280),
                 arrowprops=dict(facecolor='#059669', shrink=0.08, width=1.5, headwidth=6),
                 fontsize=8.5, fontweight='bold', color='#047857',
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#ECFDF5', edgecolor='#059669'))

    # ------------------------------------------------------------------
    # Panel 4: Automated Pytest Test Suite Verification Matrix (Bottom Right)
    # ------------------------------------------------------------------
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.axis('off')
    ax4.set_title("Panel D: Automated Pytest Suite Verification Summary (100% Pass)", fontsize=10.5, fontweight='bold', color='#1E293B', pad=10)

    test_data = [
        ["Test Module", "Focus Scope", "Passed / Total", "Status"],
        ["test_preprocessor.py", "38 features, NaN/Inf fill", "3 / 3", "PASS [100%]"],
        ["test_inference.py", "Dual model loading & SLA", "2 / 2", "PASS [100%]"],
        ["test_alert_logic.py", "5s Sliding deduplication", "3 / 3", "PASS [100%]"],
        ["test_api.py", "REST health & WebSocket", "6 / 6", "PASS [100%]"],
        ["test_stream_flow.py", "Full pipeline integration", "2 / 2", "PASS [100%]"],
        ["load_test.py", "100+ EPS stress test", "1,000 cycles", "PASS [100%]"]
    ]

    table = ax4.table(cellText=test_data, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(8.2)
    table.scale(1.0, 1.45)

    # Style table headers and cells
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_facecolor('#1E293B')
            cell.set_text_props(color='#FFFFFF', fontweight='bold')
        else:
            if col == 3:
                cell.set_facecolor('#DCFCE7')
                cell.set_text_props(color='#166534', fontweight='bold')
            elif row % 2 == 1:
                cell.set_facecolor('#F8FAFC')
            else:
                cell.set_facecolor('#FFFFFF')
        cell.set_edgecolor('#CBD5E1')

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "3_test_cases_results_and_outputs.png")
    plt.savefig(path, dpi=300)
    plt.close()
    print(f"Generated: {path}")

def copy_to_desktop():
    desktop = "C:\\Users\\LOQ\\Desktop"
    if os.path.exists(desktop):
        for fname in ["1_data_flow_design.png", "2_testing_methodology.png", "3_test_cases_results_and_outputs.png"]:
            src = os.path.join(OUTPUT_DIR, fname)
            dst = os.path.join(desktop, fname)
            shutil.copy(src, dst)
            print(f"Copied to Desktop: {dst}")

if __name__ == "__main__":
    generate_data_flow_design()
    generate_testing_methodology()
    generate_test_cases_results_and_outputs()
    copy_to_desktop()
    print("All 3 requested diagrams generated and saved successfully!")
