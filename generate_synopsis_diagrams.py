import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_DIR = "synopsis_diagrams"
os.makedirs(OUTPUT_DIR, exist_ok=True)

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

# -------------------------------------------------------------
# 1. System Architecture Block Diagram
# -------------------------------------------------------------
def create_architecture_diagram():
    fig, ax = plt.subplots(figsize=(12, 7.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    # Title
    ax.text(50, 96, "AETHERIS SOC: End-to-End Pipeline Architecture", 
            ha='center', va='center', fontsize=15, fontweight='bold', color='#0F172A')
    ax.text(50, 92.5, "Distributed Ingestion, Dual-Engine ML Scoring, In-Memory Deduplication & Real-Time Visualization", 
            ha='center', va='center', fontsize=9.5, color='#475569')

    # Box 1: Traffic Producer (Left)
    rect1 = patches.FancyBboxPatch((3, 50), 22, 32, boxstyle="round,pad=0.8,rounding_size=1.5", 
                                   edgecolor='#0284C7', facecolor='#F0F9FF', linewidth=1.8)
    ax.add_patch(rect1)
    ax.text(14, 78, "TRAFFIC INGESTION", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#0369A1')
    ax.text(14, 72, "• Network TAP / PCAP\n• CIC-IDS-2018 Replay\n• 25 – 300+ EPS Load\n• Attack Burst Injector\n  (DDoS, DoS, Botnet,\n   BruteForce, Infiltration)", 
            ha='center', va='top', fontsize=8.5, color='#1E293B', linespacing=1.35)

    # Box 2: Streaming Buffer Tier
    rect2 = patches.FancyBboxPatch((28, 50), 18, 32, boxstyle="round,pad=0.8,rounding_size=1.5", 
                                   edgecolor='#6366F1', facecolor='#EEF2FF', linewidth=1.8)
    ax.add_patch(rect2)
    ax.text(37, 78, "STREAMING BROKER", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#4338CA')
    ax.text(37, 72, "• Redis Streams / Kafka\n• Ingestion Stream Key\n• Consumer Groups\n• Backpressure Buffer\n• Zero Packet Dropping\n• At-Least-Once Delivery", 
            ha='center', va='top', fontsize=8.5, color='#1E293B', linespacing=1.35)

    # Box 3: FastAPI Inference Consumer & ML Engine (Center)
    rect3 = patches.FancyBboxPatch((49, 44), 26, 44, boxstyle="round,pad=0.8,rounding_size=1.5", 
                                   edgecolor='#059669', facecolor='#ECFDF5', linewidth=1.8)
    ax.add_patch(rect3)
    ax.text(62, 84, "INFERENCE & DEDUP ENGINE", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#047857')
    
    # Sub-boxes inside Engine
    sub1 = patches.FancyBboxPatch((51, 71), 22, 8, boxstyle="round,pad=0.5,rounding_size=1.0", 
                                  edgecolor='#059669', facecolor='#FFFFFF', linewidth=1.2)
    ax.add_patch(sub1)
    ax.text(62, 75, "38-Feature Preprocessor\n(Median Imputation, MinMax Scaling)", 
            ha='center', va='center', fontsize=7.8, fontweight='bold', color='#065F46')

    sub2 = patches.FancyBboxPatch((51, 58), 22, 10, boxstyle="round,pad=0.5,rounding_size=1.0", 
                                  edgecolor='#059669', facecolor='#FFFFFF', linewidth=1.2)
    ax.add_patch(sub2)
    ax.text(62, 63, "Dual-Engine ML Scoring\n• Supervised XGBoost (Multi-Class)\n• Unsupervised Isolation Forest", 
            ha='center', va='center', fontsize=7.8, fontweight='bold', color='#065F46')

    sub3 = patches.FancyBboxPatch((51, 46.5), 22, 8.5, boxstyle="round,pad=0.5,rounding_size=1.0", 
                                  edgecolor='#059669', facecolor='#FFFFFF', linewidth=1.2)
    ax.add_patch(sub3)
    ax.text(62, 50.7, "5s Sliding Deduplicator\n(MD5 Hash Window, 96.4% Suppress)", 
            ha='center', va='center', fontsize=7.8, fontweight='bold', color='#065F46')

    # Output Sinks (Right Side)
    # Sink 1: PostgreSQL
    rect4 = patches.FancyBboxPatch((78, 68), 19, 18, boxstyle="round,pad=0.8,rounding_size=1.5", 
                                   edgecolor='#334155', facecolor='#F8FAFC', linewidth=1.8)
    ax.add_patch(rect4)
    ax.text(87.5, 82, "POSTGRESQL 16", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#1E293B')
    ax.text(87.5, 76, "• network_events\n• security_alerts\n• ml_models audit\n• Relational Queries", 
            ha='center', va='top', fontsize=8.0, color='#334155', linespacing=1.3)

    # Sink 2: SOC Dashboard via WebSocket
    rect5 = patches.FancyBboxPatch((78, 44), 19, 20, boxstyle="round,pad=0.8,rounding_size=1.5", 
                                   edgecolor='#E11D48', facecolor='#FFF1F2', linewidth=1.8)
    ax.add_patch(rect5)
    ax.text(87.5, 60, "NEXT.JS 14 SOC UI", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#BE123C')
    ax.text(87.5, 54.5, "• DEFCON HUD Posture\n• Real-Time WebSockets\n• TanStack Forensics Drawer\n• Recharts ML Telemetry\n• Attack Burst Trigger", 
            ha='center', va='top', fontsize=8.0, color='#1E293B', linespacing=1.3)

    # Active Mitigation Box (Bottom Center)
    rect6 = patches.FancyBboxPatch((35, 14), 52, 22, boxstyle="round,pad=0.8,rounding_size=1.5", 
                                   edgecolor='#D97706', facecolor='#FFFBEB', linewidth=1.8)
    ax.add_patch(rect6)
    ax.text(61, 31.5, "AUTOMATED MITIGATION & ACTIVE DEFENSE ENGINE", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#B45309')
    ax.text(61, 23.5, "• Automated Firewall Policy Sync (POST /api/mitigation/block)\n• Line-Rate eBPF / XDP Kernel Drop Rule Generation\n• Sliding-Window Multi-Class Threshold Tripping\n• SOC Operator One-Click Direct IP Blacklist & Rule Flushes", 
            ha='center', va='center', fontsize=8.2, color='#78350F', linespacing=1.35)

    # Arrows
    arrow_props = dict(arrowstyle="->", lw=2.0, color='#0F172A', mutation_scale=15)
    # Traffic -> Streaming
    ax.annotate("", xy=(28, 66), xytext=(25, 66), arrowprops=arrow_props)
    # Streaming -> Engine
    ax.annotate("", xy=(49, 66), xytext=(46, 66), arrowprops=arrow_props)
    # Engine -> PostgreSQL
    ax.annotate("", xy=(78, 77), xytext=(75, 77), arrowprops=arrow_props)
    # Engine -> WebSocket / SOC UI
    ax.annotate("", xy=(78, 54), xytext=(75, 54), arrowprops=arrow_props)
    # Engine -> Mitigation
    ax.annotate("", xy=(61, 36), xytext=(61, 44), arrowprops=dict(arrowstyle="<->", lw=2.0, color='#D97706', mutation_scale=15))
    # SOC UI -> Mitigation
    ax.annotate("", xy=(78, 25), xytext=(85, 44), arrowprops=dict(arrowstyle="->", lw=1.5, color='#D97706', linestyle='dashed', mutation_scale=12))

    # Flow rate labels
    ax.text(26.5, 68, "Raw Flow", ha='center', va='bottom', fontsize=7.5, color='#475569', fontweight='bold')
    ax.text(47.5, 68, "JSON Event", ha='center', va='bottom', fontsize=7.5, color='#475569', fontweight='bold')
    ax.text(76.5, 79, "Unique DB", ha='center', va='bottom', fontsize=7.5, color='#475569', fontweight='bold')
    ax.text(76.5, 56, "Live WS", ha='center', va='bottom', fontsize=7.5, color='#475569', fontweight='bold')
    ax.text(82, 33, "Operator Override", ha='center', va='bottom', fontsize=7.0, color='#B45309', fontweight='bold')

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig1_system_architecture.png")
    plt.savefig(path, dpi=300)
    plt.close()
    print(f"Saved: {path}")

# -------------------------------------------------------------
# 2. Dual-Engine Decision Flowchart
# -------------------------------------------------------------
def create_dual_engine_decision_flowchart():
    fig, ax = plt.subplots(figsize=(10, 8.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 97, "Dual-Engine Machine Learning Threat Scoring Decision Flowchart", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#0F172A')
    ax.text(50, 93.5, "Consensus Evaluation Combining Supervised XGBoost and Unsupervised Isolation Forest", 
            ha='center', va='center', fontsize=9, color='#475569')

    # Step 1: Input Flow
    p1 = patches.FancyBboxPatch((30, 84), 40, 6, boxstyle="round,pad=0.5,rounding_size=1.0", 
                                edgecolor='#0284C7', facecolor='#F0F9FF', linewidth=1.5)
    ax.add_patch(p1)
    ax.text(50, 87, "Receive NetFlow & Extract 38 Normalized Features", ha='center', va='center', fontsize=9, fontweight='bold', color='#0369A1')

    # Step 2: Parallel Fork
    p2a = patches.FancyBboxPatch((10, 68), 35, 10, boxstyle="round,pad=0.5,rounding_size=1.0", 
                                 edgecolor='#6366F1', facecolor='#EEF2FF', linewidth=1.5)
    ax.add_patch(p2a)
    ax.text(27.5, 74, "Supervised Engine: XGBoost", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#4338CA')
    ax.text(27.5, 69.5, "Multi-Class Probability Distribution\nClass = ArgMax(P), Conf = P_max", ha='center', va='center', fontsize=7.8, color='#312E81')

    p2b = patches.FancyBboxPatch((55, 68), 35, 10, boxstyle="round,pad=0.5,rounding_size=1.0", 
                                 edgecolor='#D97706', facecolor='#FFFBEB', linewidth=1.5)
    ax.add_patch(p2b)
    ax.text(72.5, 74, "Unsupervised Engine: Isolation Forest", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#B45309')
    ax.text(72.5, 69.5, "Anomaly Score s = decision_function(X)\nCalibrated Threshold (s < 0.0)", ha='center', va='center', fontsize=7.8, color='#78350F')

    # Decision 1: XGBoost Known Attack?
    # Diamond 1
    d1_pts = [[50, 58], [72, 50], [50, 42], [28, 50]]
    d1 = patches.Polygon(d1_pts, closed=True, edgecolor='#BE123C', facecolor='#FFF1F2', linewidth=1.8)
    ax.add_patch(d1)
    ax.text(50, 51.5, "Is Class != 'Benign'\nAND Conf >= 0.70?", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#9F1239')

    # Decision 2: Isolation Forest Anomaly?
    # Diamond 2
    d2_pts = [[25, 34], [42, 28], [25, 22], [8, 28]]
    d2 = patches.Polygon(d2_pts, closed=True, edgecolor='#D97706', facecolor='#FEF3C7', linewidth=1.8)
    ax.add_patch(d2)
    ax.text(25, 28, "Is Anomaly Score\ns < 0.0?", ha='center', va='center', fontsize=8.2, fontweight='bold', color='#B45309')

    # Outcomes
    # Outcome 1: Known Attack
    p_out1 = patches.FancyBboxPatch((76, 38), 22, 14, boxstyle="round,pad=0.5,rounding_size=1.0", 
                                    edgecolor='#E11D48', facecolor='#FFE4E6', linewidth=1.8)
    ax.add_patch(p_out1)
    ax.text(87, 47, "KNOWN ATTACK", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#BE123C')
    ax.text(87, 41.5, "DDoS / DoS / Botnet\nBruteForce / Infiltration\nSeverity: CRITICAL / HIGH", ha='center', va='center', fontsize=7.5, color='#881337')

    # Outcome 2: Zero-Day Anomaly
    p_out2 = patches.FancyBboxPatch((48, 16), 24, 13, boxstyle="round,pad=0.5,rounding_size=1.0", 
                                    edgecolor='#7C3AED', facecolor='#F5F3FF', linewidth=1.8)
    ax.add_patch(p_out2)
    ax.text(60, 24.5, "ZERO-DAY / NOVEL", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#6D28D9')
    ax.text(60, 19.5, "Unsupervised Outlier\nUnseen Attack Signature\nSeverity: HIGH (Alert)", ha='center', va='center', fontsize=7.5, color='#4C1D95')

    # Outcome 3: Normal Benign
    p_out3 = patches.FancyBboxPatch((8, 6), 34, 10, boxstyle="round,pad=0.5,rounding_size=1.0", 
                                    edgecolor='#059669', facecolor='#ECFDF5', linewidth=1.8)
    ax.add_patch(p_out3)
    ax.text(25, 12.5, "BENIGN NORMAL TRAFFIC", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#047857')
    ax.text(25, 8.5, "Normal Telemetry Stream | Severity: LOW", ha='center', va='center', fontsize=7.8, color='#065F46')

    # Final Stage: Alert Deduplicator & Dispatch
    p_dedup = patches.FancyBboxPatch((76, 12), 22, 18, boxstyle="round,pad=0.5,rounding_size=1.0", 
                                     edgecolor='#0F172A', facecolor='#F1F5F9', linewidth=1.8)
    ax.add_patch(p_dedup)
    ax.text(87, 24, "IN-MEMORY DEDUP", ha='center', va='center', fontsize=9.0, fontweight='bold', color='#0F172A')
    ax.text(87, 17, "5-Second Hash Window\nPostgreSQL Write / WS\nActive eBPF Rule Drop", ha='center', va='center', fontsize=7.5, color='#334155')

    # Arrows
    arr = dict(arrowstyle="->", lw=1.6, color='#0F172A', mutation_scale=12)
    # Input to Engines
    ax.annotate("", xy=(27.5, 78), xytext=(40, 84), arrowprops=arr)
    ax.annotate("", xy=(72.5, 78), xytext=(60, 84), arrowprops=arr)
    # Engines to Decision 1
    ax.annotate("", xy=(42, 55), xytext=(27.5, 68), arrowprops=arr)
    ax.annotate("", xy=(58, 55), xytext=(72.5, 68), arrowprops=arr)
    # D1 -> YES (Known Attack)
    ax.annotate("", xy=(76, 48), xytext=(72, 50), arrowprops=arr)
    ax.text(73.5, 51, "YES", fontsize=8.0, fontweight='bold', color='#BE123C')
    # D1 -> NO (Check Isolation Forest)
    ax.annotate("", xy=(25, 34), xytext=(50, 42), arrowprops=arr)
    ax.text(39, 39, "NO (Benign / Unsure)", fontsize=7.5, fontweight='bold', color='#475569')
    # D2 -> YES (Zero-Day Anomaly)
    ax.annotate("", xy=(48, 24), xytext=(42, 28), arrowprops=arr)
    ax.text(44, 28.5, "YES", fontsize=8.0, fontweight='bold', color='#7C3AED')
    # D2 -> NO (Benign Traffic)
    ax.annotate("", xy=(25, 16), xytext=(25, 22), arrowprops=arr)
    ax.text(26.5, 18.5, "NO", fontsize=8.0, fontweight='bold', color='#059669')
    # Threats -> Dedup Engine
    ax.annotate("", xy=(87, 30), xytext=(87, 38), arrowprops=arr)
    ax.annotate("", xy=(76, 21), xytext=(72, 22), arrowprops=arr)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig2_dual_engine_decision.png")
    plt.savefig(path, dpi=300)
    plt.close()
    print(f"Saved: {path}")

# -------------------------------------------------------------
# 3. 8-Phase Methodology Lifecycle
# -------------------------------------------------------------
def create_methodology_lifecycle():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 96, "AETHERIS SOC: 8-Phase Engineering Methodology Lifecycle", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#0F172A')
    ax.text(50, 92.5, "From Cyber Threat Problem Identification to Containerized High-Throughput Deployment", 
            ha='center', va='center', fontsize=9, color='#475569')

    phases = [
        ("Phase 1: Requirement Analysis", "Identify SOC operational bottlenecks,\nsub-20ms SLA, 100+ EPS throughput,\nand alert fatigue reduction targets.", "#0284C7", "#F0F9FF"),
        ("Phase 2: Benchmark Data Ingestion", "Acquire CIC-IDS-2018 dataset,\nreconstruct multi-vector attacks\n(DDoS, Botnet, Infiltration, BruteForce).", "#0284C7", "#F0F9FF"),
        ("Phase 3: 38-Feature Preprocessing", "Median imputation, Inf clipping,\nmin-max scaling encapsulated in\nunified ml/pipeline/preprocessor.py.", "#6366F1", "#EEF2FF"),
        ("Phase 4: Architecture & Broker Design", "Decoupled microservices with Redis\nStreams/Kafka consumer groups and\nPostgreSQL relational schemas.", "#6366F1", "#EEF2FF"),
        ("Phase 5: Dual ML Model Training", "Supervised XGBoost multi-class and\nIsolation Forest anomaly scoring with\nzero-skew JSON model serialization.", "#059669", "#ECFDF5"),
        ("Phase 6: Full-Stack Implementation", "FastAPI ASGI engine, Next.js 14 SOC\ndashboard, persistent WebSockets,\nand eBPF firewall drop rules.", "#059669", "#ECFDF5"),
        ("Phase 7: Multi-Tier Automated Testing", "Pytest suite for unit preprocessor,\ninference latency, sliding deduplication,\nAPI contracts, and stream pipeline.", "#D97706", "#FFFBEB"),
        ("Phase 8: Benchmarking & Deployment", "Measure P50/P95/P99 latency,\nEPS stress throughput, and 5-service\nDocker Compose containerization.", "#BE123C", "#FFF1F2")
    ]

    # Render as two rows of 4 boxes (left to right, then right to left or zigzag)
    # Row 1: y = 70 to 52
    col_w = 21.5
    gap_x = 3.5
    start_x = 2.0
    
    # Row 1 (Phases 1 to 4)
    for i in range(4):
        x = start_x + i * (col_w + gap_x)
        y = 54
        title, desc, border_c, bg_c = phases[i]
        box = patches.FancyBboxPatch((x, y), col_w, 32, boxstyle="round,pad=0.5,rounding_size=1.2",
                                     edgecolor=border_c, facecolor=bg_c, linewidth=1.6)
        ax.add_patch(box)
        # Phase badge
        badge = patches.FancyBboxPatch((x + 1.5, y + 26), 18.5, 4.5, boxstyle="round,pad=0.3,rounding_size=0.8",
                                      edgecolor=border_c, facecolor=border_c, linewidth=1.0)
        ax.add_patch(badge)
        ax.text(x + 10.75, y + 28.2, f"Phase {i+1}", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#FFFFFF')
        
        ax.text(x + 10.75, y + 21, title.split(": ")[1], ha='center', va='center', fontsize=8.8, fontweight='bold', color=border_c)
        ax.text(x + 10.75, y + 10.5, desc, ha='center', va='center', fontsize=7.5, color='#1E293B', linespacing=1.3)

    # Row 2 (Phases 5 to 8)
    for i in range(4):
        p_idx = 4 + i
        x = start_x + (3 - i) * (col_w + gap_x)
        y = 12
        title, desc, border_c, bg_c = phases[p_idx]
        box = patches.FancyBboxPatch((x, y), col_w, 32, boxstyle="round,pad=0.5,rounding_size=1.2",
                                     edgecolor=border_c, facecolor=bg_c, linewidth=1.6)
        ax.add_patch(box)
        badge = patches.FancyBboxPatch((x + 1.5, y + 26), 18.5, 4.5, boxstyle="round,pad=0.3,rounding_size=0.8",
                                      edgecolor=border_c, facecolor=border_c, linewidth=1.0)
        ax.add_patch(badge)
        ax.text(x + 10.75, y + 28.2, f"Phase {p_idx+1}", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#FFFFFF')
        
        ax.text(x + 10.75, y + 21, title.split(": ")[1], ha='center', va='center', fontsize=8.8, fontweight='bold', color=border_c)
        ax.text(x + 10.75, y + 10.5, desc, ha='center', va='center', fontsize=7.5, color='#1E293B', linespacing=1.3)

    # Connecting Arrows
    arr = dict(arrowstyle="->", lw=2.0, color='#0F172A', mutation_scale=14)
    # Row 1 forward arrows
    for i in range(3):
        x_from = start_x + (i + 1) * col_w + i * gap_x
        x_to = x_from + gap_x
        ax.annotate("", xy=(x_to, 70), xytext=(x_from, 70), arrowprops=arr)
    
    # Drop down arrow from Phase 4 to Phase 5
    ax.annotate("", xy=(start_x + 3 * (col_w + gap_x) + col_w / 2, 44), 
                xytext=(start_x + 3 * (col_w + gap_x) + col_w / 2, 54), arrowprops=arr)

    # Row 2 backward arrows (Phase 5 -> 6 -> 7 -> 8)
    for i in range(3):
        x_from = start_x + (3 - i) * (col_w + gap_x)
        x_to = x_from - gap_x
        ax.annotate("", xy=(x_to, 28), xytext=(x_from, 28), arrowprops=arr)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig3_methodology_lifecycle.png")
    plt.savefig(path, dpi=300)
    plt.close()
    print(f"Saved: {path}")

# -------------------------------------------------------------
# 4. Feature Extraction & Preprocessing Pipeline
# -------------------------------------------------------------
def create_preprocessing_pipeline():
    fig, ax = plt.subplots(figsize=(10.5, 6.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 95, "NetFlow Telemetry 38-Feature Preprocessing Pipeline", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#0F172A')
    ax.text(50, 91.5, "Deterministic Normalization Shared Identically Between Training and Production Inference", 
            ha='center', va='center', fontsize=9, color='#475569')

    stages = [
        ("Raw Network Capture", "• CIC-IDS-2018 CSV/PCAP\n• 80 NetFlow Attributes\n• Timestamps, IPs, Ports,\n  Lengths, Flags, Windows", "#0284C7", "#F0F9FF"),
        ("Identity Masking", "• Strip src_ip, dst_ip\n• Drop timestamp, port\n• Prevents memorization\n• Generalizes to any subnet", "#6366F1", "#EEF2FF"),
        ("Statistical Selection", "• 38 high-salience features\n• Flow duration, inter-arrival,\n  packet size mean/std,\n  TCP flags (SYN, ACK, RST)", "#059669", "#ECFDF5"),
        ("Imputation & Clipping", "• Missing value median fill\n• Clip Inf floats to [-10^6, 10^6]\n• Zero-division defense\n• Runtime NaN resilience", "#D97706", "#FFFBEB"),
        ("MinMax Scaler [0, 1]", "• Pre-fitted train scaler\n• Standardized range [0, 1]\n• Exported preprocessor.pkl\n• 38-float inference array", "#BE123C", "#FFF1F2")
    ]

    w = 17.5
    gap = 2.5
    sx = 1.0
    y = 20
    h = 60

    for idx, (title, desc, border_c, bg_c) in enumerate(stages):
        x = sx + idx * (w + gap)
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5,rounding_size=1.2",
                                     edgecolor=border_c, facecolor=bg_c, linewidth=1.6)
        ax.add_patch(box)
        
        # Step Circle Number
        circ = patches.Circle((x + w/2, y + h - 6), 3.5, edgecolor=border_c, facecolor=border_c)
        ax.add_patch(circ)
        ax.text(x + w/2, y + h - 6, str(idx + 1), ha='center', va='center', fontsize=9, fontweight='bold', color='#FFFFFF')

        ax.text(x + w/2, y + h - 14, title, ha='center', va='center', fontsize=8.8, fontweight='bold', color=border_c)
        ax.text(x + w/2, y + 20, desc, ha='center', va='center', fontsize=7.8, color='#1E293B', linespacing=1.35)

    # Arrows between boxes
    arr = dict(arrowstyle="->", lw=2.0, color='#0F172A', mutation_scale=14)
    for idx in range(4):
        x_from = sx + (idx + 1) * w + idx * gap
        x_to = x_from + gap
        ax.annotate("", xy=(x_to, y + h/2), xytext=(x_from, y + h/2), arrowprops=arr)

    # Bottom Callout: Train-Serve Skew Prevention
    callout = patches.FancyBboxPatch((15, 4), 70, 11, boxstyle="round,pad=0.5,rounding_size=1.0",
                                    edgecolor='#047857', facecolor='#F0FDF4', linewidth=1.2)
    ax.add_patch(callout)
    ax.text(50, 9.5, "GUARANTEE: ZERO TRAIN-SERVE SKEW\nThe identical preprocessor module (ml/pipeline/preprocessor.py) is imported directly by both the\noffline training pipeline and the online FastAPI inference worker, ensuring 100% mathematical consistency.", 
            ha='center', va='center', fontsize=7.8, color='#065F46', linespacing=1.25)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig4_preprocessing_pipeline.png")
    plt.savefig(path, dpi=300)
    plt.close()
    print(f"Saved: {path}")

# -------------------------------------------------------------
# 5. Alert Deduplication Flowchart
# -------------------------------------------------------------
def create_alert_deduplication_flowchart():
    fig, ax = plt.subplots(figsize=(10.5, 8.0), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 97, "In-Memory 5-Second Sliding-Window Alert Deduplication Flowchart", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#0F172A')
    ax.text(50, 93.5, "Eliminates SOC Alert Fatigue and Database I/O Bottlenecks with 96.4% Suppression Ratio", 
            ha='center', va='center', fontsize=9, color='#475569')

    # Step 1: Malicious Flow Detected
    b1 = patches.FancyBboxPatch((28, 83), 44, 7, boxstyle="round,pad=0.5,rounding_size=1.0", 
                                edgecolor='#BE123C', facecolor='#FFF1F2', linewidth=1.5)
    ax.add_patch(b1)
    ax.text(50, 86.5, "Malicious Network Flow Detected\n(Attack Type != Benign, e.g. DDoS, Botnet)", 
            ha='center', va='center', fontsize=8.8, fontweight='bold', color='#9F1239')

    # Step 2: Hash Generation
    b2 = patches.FancyBboxPatch((24, 70), 52, 8, boxstyle="round,pad=0.5,rounding_size=1.0", 
                                edgecolor='#6366F1', facecolor='#EEF2FF', linewidth=1.5)
    ax.add_patch(b2)
    ax.text(50, 74, "Generate Ingestion Fingerprint Hash Key:\nKey = MD5(src_ip + '_' + dst_ip + '_' + attack_type)", 
            ha='center', va='center', fontsize=8.8, fontweight='bold', color='#4338CA')

    # Step 3: Decision Diamond
    d_pts = [[50, 62], [76, 52], [50, 42], [24, 52]]
    d = patches.Polygon(d_pts, closed=True, edgecolor='#0F172A', facecolor='#F1F5F9', linewidth=1.8)
    ax.add_patch(d)
    ax.text(50, 52, "Does Key Exist in Sliding Cache\nAND (T_now - T_first) <= 5.0s?", 
            ha='center', va='center', fontsize=8.5, fontweight='bold', color='#0F172A')

    # Branch A: YES (Volumetric Flood Duplicate) -> Left Side
    b_dup = patches.FancyBboxPatch((4, 24), 38, 20, boxstyle="round,pad=0.5,rounding_size=1.2", 
                                   edgecolor='#D97706', facecolor='#FEF3C7', linewidth=1.8)
    ax.add_patch(b_dup)
    ax.text(23, 40.5, "DUPLICATE ATTACK BURST", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#B45309')
    ax.text(23, 31.5, "• Increment in-memory counter: count += 1\n• Update last_seen timestamp\n• SUPPRESS PostgreSQL database write\n• Broadcast throttled delta via WebSocket\n• Zero alert spam in SOC triage queue", 
            ha='center', va='center', fontsize=7.8, color='#78350F', linespacing=1.3)

    # Branch B: NO (New Incident / Window Expired) -> Right Side
    b_new = patches.FancyBboxPatch((58, 24), 38, 20, boxstyle="round,pad=0.5,rounding_size=1.2", 
                                   edgecolor='#059669', facecolor='#ECFDF5', linewidth=1.8)
    ax.add_patch(b_new)
    ax.text(77, 40.5, "NEW SECURITY INCIDENT", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#047857')
    ax.text(77, 31.5, "• Initialize window: Key, count = 1, T_start\n• INSERT persistent row into PostgreSQL alerts\n• Emit high-priority audio-visual SOC alert\n• Evaluate DEFCON threat posture level\n• Dispatch eBPF auto-block if Critical", 
            ha='center', va='center', fontsize=7.8, color='#065F46', linespacing=1.3)

    # Bottom Summary Badge
    b_sum = patches.FancyBboxPatch((20, 5), 60, 11, boxstyle="round,pad=0.5,rounding_size=1.0", 
                                   edgecolor='#0284C7', facecolor='#F0F9FF', linewidth=1.5)
    ax.add_patch(b_sum)
    ax.text(50, 10.5, "BENCHMARK PERFORMANCE VERIFICATION\nSliding Deduplication eliminates 96.4% of redundant database writes during multi-thousand\npacket floods while guaranteeing sub-second notification of newly emerging attack origins.", 
            ha='center', va='center', fontsize=8.0, fontweight='bold', color='#0369A1', linespacing=1.3)

    # Arrows
    arr = dict(arrowstyle="->", lw=1.8, color='#0F172A', mutation_scale=13)
    ax.annotate("", xy=(50, 78), xytext=(50, 83), arrowprops=arr)
    ax.annotate("", xy=(50, 62), xytext=(50, 70), arrowprops=arr)
    
    # Diamond to Left (YES)
    ax.annotate("", xy=(23, 44), xytext=(24, 52), arrowprops=arr)
    ax.text(18, 50, "YES (Duplicate)", fontsize=8.0, fontweight='bold', color='#B45309')
    
    # Diamond to Right (NO)
    ax.annotate("", xy=(77, 44), xytext=(76, 52), arrowprops=arr)
    ax.text(78, 50, "NO (New Incident)", fontsize=8.0, fontweight='bold', color='#047857')

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig5_alert_deduplication.png")
    plt.savefig(path, dpi=300)
    plt.close()
    print(f"Saved: {path}")

# -------------------------------------------------------------
# 6. Multi-Tier Testing Pyramid
# -------------------------------------------------------------
def create_testing_pyramid():
    fig, ax = plt.subplots(figsize=(10.5, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 96, "AETHERIS SOC: Multi-Tier Quality Assurance & Testing Pyramid", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#0F172A')
    ax.text(50, 92.5, "Systematic Automated Verification Covering Units, Models, Deduplication, APIs, and Streams", 
            ha='center', va='center', fontsize=9, color='#475569')

    tiers = [
        ("Tier 5: Load & Stress Testing", "load_test.py — Sustained 100+ EPS throughput, P50/P95/P99 latency percentiles SLA < 20ms", 40, 18, 76, "#BE123C", "#FFE4E6"),
        ("Tier 4: End-to-End Pipeline Testing", "test_stream_flow.py — Full message lifecycle: Producer -> Redis Streams -> FastAPI Consumer -> PostgreSQL", 52, 32, 60, "#D97706", "#FEF3C7"),
        ("Tier 3: REST & WebSocket API Testing", "test_api.py — REST health, alert pagination, model governance, WebSocket frame delivery", 64, 46, 44, "#059669", "#ECFDF5"),
        ("Tier 2: Alert & Inference Logic Testing", "test_alert_logic.py & test_inference.py — XGBoost + Isolation Forest dual scoring, 5s deduplication", 76, 60, 28, "#6366F1", "#EEF2FF"),
        ("Tier 1: Unit & Preprocessing Testing", "test_preprocessor.py — 38-feature extraction, NaN median imputation, Inf clipping, MinMax scaling", 88, 74, 12, "#0284C7", "#F0F9FF")
    ]

    for title, desc, width, y_pos, height_offset, border_c, bg_c in tiers:
        x_pos = (100 - width) / 2
        box = patches.FancyBboxPatch((x_pos, y_pos), width, 11, boxstyle="round,pad=0.4,rounding_size=1.0",
                                     edgecolor=border_c, facecolor=bg_c, linewidth=1.6)
        ax.add_patch(box)
        ax.text(50, y_pos + 7.5, title, ha='center', va='center', fontsize=9.2, fontweight='bold', color=border_c)
        ax.text(50, y_pos + 3.2, desc, ha='center', va='center', fontsize=7.6, color='#1E293B')

    # Side Indicators
    ax.annotate("", xy=(8, 86), xytext=(8, 14), 
                arrowprops=dict(arrowstyle="->", lw=2.0, color='#64748B', mutation_scale=14))
    ax.text(6.5, 50, "Scope & Execution Depth", rotation=90, ha='center', va='center', fontsize=9, fontweight='bold', color='#475569')

    ax.annotate("", xy=(92, 14), xytext=(92, 86), 
                arrowprops=dict(arrowstyle="->", lw=2.0, color='#64748B', mutation_scale=14))
    ax.text(93.5, 50, "Execution Speed & Frequency", rotation=-90, ha='center', va='center', fontsize=9, fontweight='bold', color='#475569')

    # Bottom Pass Rate Banner
    banner = patches.FancyBboxPatch((15, 3), 70, 7.5, boxstyle="round,pad=0.4,rounding_size=0.8",
                                    edgecolor='#059669', facecolor='#ECFDF5', linewidth=1.2)
    ax.add_patch(banner)
    ax.text(50, 6.75, "VERIFIED RESULT: 100% PYTEST TEST SUITE PASS RATE ACROSS ALL 5 TIERS", 
            ha='center', va='center', fontsize=8.5, fontweight='bold', color='#047857')

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig6_testing_pyramid.png")
    plt.savefig(path, dpi=300)
    plt.close()
    print(f"Saved: {path}")

if __name__ == "__main__":
    create_architecture_diagram()
    create_dual_engine_decision_flowchart()
    create_methodology_lifecycle()
    create_preprocessing_pipeline()
    create_alert_deduplication_flowchart()
    create_testing_pyramid()
    print("All 6 diagrams generated successfully!")
