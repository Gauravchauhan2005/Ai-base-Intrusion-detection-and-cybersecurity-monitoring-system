import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def clean_table(table, col_widths=None, header_bg="1E293B", zebra=True):
    tblPr = table._tbl.tblPr
    for sp in tblPr.findall(qn('w:tblCellSpacing')):
        tblPr.remove(sp)
    for b in tblPr.findall(qn('w:tblBorders')):
        tblPr.remove(b)
    tblBorders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="single" w:sz="6" w:space="0" w:color="94A3B8"/>\n'
        f'  <w:left w:val="single" w:sz="6" w:space="0" w:color="94A3B8"/>\n'
        f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="94A3B8"/>\n'
        f'  <w:right w:val="single" w:sz="6" w:space="0" w:color="94A3B8"/>\n'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>\n'
        f'  <w:insideV w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(tblBorders)
    
    for m in tblPr.findall(qn('w:tblCellMar')):
        tblPr.remove(m)
    tblCellMar = parse_xml(
        f'<w:tblCellMar {nsdecls("w")}>\n'
        f'  <w:top w:w="120" w:type="dxa"/>\n'
        f'  <w:left w:w="140" w:type="dxa"/>\n'
        f'  <w:bottom w:w="120" w:type="dxa"/>\n'
        f'  <w:right w:w="140" w:type="dxa"/>\n'
        f'</w:tblCellMar>'
    )
    tblPr.append(tblCellMar)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    if len(table.rows) > 0:
        header_tr = table.rows[0]._tr
        trPr = header_tr.get_or_add_trPr()
        if not trPr.findall(qn('w:tblHeader')):
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
        for c_idx, cell in enumerate(table.rows[0].cells):
            tcPr = cell._tc.get_or_add_tcPr()
            for b in tcPr.findall(qn('w:tcBorders')):
                tcPr.remove(b)
            for s in tcPr.findall(qn('w:shd')):
                tcPr.remove(s)
            tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{header_bg}"/>'))
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            if col_widths and c_idx < len(col_widths):
                cell.width = col_widths[c_idx]
            for p in cell.paragraphs:
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.line_spacing = 1.0
                for run in p.runs:
                    run.font.name = "Calibri"
                    run.font.size = Pt(9.5)
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(255, 255, 255)

    for r_idx, row in enumerate(table.rows[1:], start=1):
        trPr = row._tr.get_or_add_trPr()
        if not trPr.findall(qn('w:cantSplit')):
            trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        bg_color = "F8FAFC" if (zebra and r_idx % 2 == 1) else "FFFFFF"
        for c_idx, cell in enumerate(row.cells):
            tcPr = cell._tc.get_or_add_tcPr()
            for b in tcPr.findall(qn('w:tcBorders')):
                tcPr.remove(b)
            for s in tcPr.findall(qn('w:shd')):
                tcPr.remove(s)
            tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_color}"/>'))
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            if col_widths and c_idx < len(col_widths):
                cell.width = col_widths[c_idx]
            for p in cell.paragraphs:
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.line_spacing = 1.05
                for run in p.runs:
                    run.font.name = "Calibri"
                    run.font.size = Pt(9)
                    run.font.color.rgb = RGBColor(30, 41, 59)
                    if c_idx == 0 and len(row.cells) > 2:
                        run.font.bold = True

def add_heading_1(doc, text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(4)
    h.paragraph_format.keep_with_next = True
    r = h.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = RGBColor(15, 23, 42)
    return h

def add_heading_2(doc, text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(10)
    h.paragraph_format.space_after = Pt(3)
    h.paragraph_format.keep_with_next = True
    r = h.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = RGBColor(30, 41, 59)
    return h

def add_para(doc, text, bold_prefix=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(10)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(15, 23, 42)
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(51, 65, 85)
    return p

def add_figure(doc, image_path, caption, width=Inches(6.2)):
    if os.path.exists(image_path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run()
        run.add_picture(image_path, width=width)
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(8)
        r_cap = p_cap.add_run(caption)
        r_cap.font.name = "Calibri"
        r_cap.font.size = Pt(9.5)
        r_cap.font.bold = True
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(71, 85, 105)

def generate_report(output_path):
    doc = Document()
    
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    # Title Page Header
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p_inst.add_run("MADHAV INSTITUTE OF TECHNOLOGY & SCIENCE, GWALIOR\n")
    r1.font.name = "Calibri"
    r1.font.size = Pt(14)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(15, 23, 42)
    
    r2 = p_inst.add_run("(Deemed to be University)\n")
    r2.font.name = "Calibri"
    r2.font.size = Pt(11)
    r2.font.italic = True
    r2.font.color.rgb = RGBColor(71, 85, 105)

    r3 = p_inst.add_run("CORNERSTONE PROJECT\nPROJECT SYNOPSIS\n")
    r3.font.name = "Calibri"
    r3.font.size = Pt(13)
    r3.font.bold = True
    r3.font.color.rgb = RGBColor(30, 41, 59)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(10)
    p_title.paragraph_format.space_after = Pt(14)
    rt = p_title.add_run("“AI-BASED INTRUSION DETECTION & CYBERSECURITY MONITORING SYSTEM”")
    rt.font.name = "Calibri"
    rt.font.size = Pt(14)
    rt.font.bold = True
    rt.font.color.rgb = RGBColor(14, 116, 144)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(4)
    r_sub = p_sub.add_run("Submitted by")
    r_sub.font.bold = True
    r_sub.font.size = Pt(11)

    # Student Table
    t_std = doc.add_table(rows=1, cols=3)
    t_std.rows[0].cells[0].text = "S. No."
    t_std.rows[0].cells[1].text = "Student Name"
    t_std.rows[0].cells[2].text = "Enrollment No."
    std_data = [
        ("1", "Gaurav Chauhan", "BTIT24O1054"),
        ("2", "Kushagra Sahu", "BTIT24O1078"),
        ("3", "______________________________", "______________________________"),
        ("4", "______________________________", "______________________________")
    ]
    for row in std_data:
        r = t_std.add_row()
        for idx, text in enumerate(row):
            r.cells[idx].text = text
    clean_table(t_std, col_widths=[Inches(1.0), Inches(3.2), Inches(2.7)])

    # Guide Info
    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_guide.paragraph_format.space_before = Pt(12)
    p_guide.paragraph_format.space_after = Pt(20)
    p_guide.add_run(
        "Under the Guidance of\n"
        "Dr. Abhilash Sonker\n"
        "Designation: ______________________________\n"
        "School of _____________________________\n"
        "Madhav Institute of Technology & Science, Gwalior\n"
        "Academic Session: 2026–27"
    )
    for r in p_guide.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(30, 41, 59)

    doc.add_page_break()

    # 1. Introduction
    add_heading_1(doc, "1. Introduction")
    add_para(doc, "1.1 Background of the Project Domain", bold_prefix="")
    add_para(doc, "The rapid evolution of cloud computing, microservice-based enterprise architectures, and distributed computer networks has expanded the corporate digital footprint exponentially. Contemporary organizations process millions of concurrent network connections daily across heterogeneous hybrid-cloud environments. Alongside this expansion, the sophistication and frequency of cyberattacks have grown dramatically. Malicious actors deploy high-rate distributed denial-of-service (DDoS) floods, polymorphic botnets, automated credential brute-forcing, and zero-day intrusions designed to evade perimeter defenses.")
    add_para(doc, "Historically, corporate defense relied heavily on Signature-Based Intrusion Detection Systems (S-IDS) such as Snort and Suricata. These tools operate by inspecting raw packet payloads against deterministic rule databases. However, traditional S-IDS architectures suffer from three critical structural bottlenecks: (1) total blindness to zero-day vulnerabilities and polymorphic payload obfuscation, (2) severe CPU exhaustion under multi-gigabit throughput, and (3) operational failure due to the widespread adoption of end-to-end transport layer encryption (HTTPS/TLS 1.3). To address these limitations, modern network security has shifted toward Flow-Based Anomaly Detection (A-IDS), which evaluates statistical connection metadata (e.g., packet lengths, flow duration, inter-arrival times, TCP flag distributions) without requiring payload decryption.")

    add_para(doc, "1.2 Importance and Practical Relevance", bold_prefix="")
    add_para(doc, "In enterprise Security Operations Centers (SOCs), detection latency directly governs business resilience. A threat detected in milliseconds can be mitigated automatically at the software-defined perimeter before lateral movement occurs, whereas delays of minutes often lead to catastrophic data exfiltration or total server downtime. Furthermore, Security Analysts suffer from acute 'alert fatigue' caused by thousands of redundant alert triggers during volumetric flood attacks. There is an urgent practical demand for systems that combine high-speed streaming ingestion, machine learning threat classification, and in-memory alert deduplication.")

    add_para(doc, "1.3 Motivation & Technologies Involved", bold_prefix="")
    add_para(doc, "The primary motivation of this project—named AETHERIS SOC—is to bridge the divide between academic machine learning research and enterprise distributed systems engineering. While many research models achieve high theoretical accuracy in offline Jupyter notebooks, they fail when exposed to real-time high-throughput network streams. The proposed system resolves this by unifying a production streaming broker (Kafka / Redis Streams), an asynchronous FastAPI inference consumer, a dual-engine ML scoring pipeline (supervised XGBoost + unsupervised Isolation Forest), relational persistence (PostgreSQL 16), and a reactive Next.js 14 SOC dashboard connected via persistent WebSockets.")

    # 2. Problem Statement
    add_heading_1(doc, "2. Problem Statement")
    add_para(doc, "Despite decades of advancement in network security, current intrusion detection systems face four fundamental bottlenecks:")
    add_para(doc, "• Static Rule Rigidity & Zero-Day Blindness: Signature-based systems match static byte sequences. Novel zero-day attacks and polymorphic payloads bypass these rules with ease.")
    add_para(doc, "• The Supervised vs. Unsupervised Dilemma: Supervised models classify known attack categories with high accuracy but miss novel intrusions. Conversely, standalone unsupervised models suffer from excessive False Positive Rates (FPR), generating constant false alarms on benign network spikes.")
    add_para(doc, "• Architectural Disconnect & Buffer Exhaustion: Academic machine learning models typically process static batch CSVs. Under live volumetric flood bursts (e.g., 50,000 pkts/sec), direct database writes cause connection pool exhaustion, dropping packets and blinding administrators.")
    add_para(doc, "• Severe Alert Fatigue: Volumetric floods trigger an alert for every single malicious packet, flooding database tables with tens of thousands of duplicate records and overwhelming human operators.")
    add_para(doc, "Need for Proposed Solution: A robust, full-stack, distributed architecture that pairs high-throughput asynchronous message buffering with dual-engine ML inference, sliding-window alert deduplication, and real-time WebSocket telemetry broadcasting.")

    # 3. Objectives
    add_heading_1(doc, "3. Objectives")
    add_para(doc, "1. To design and develop an end-to-end, high-throughput, distributed real-time AI-based intrusion detection and cybersecurity monitoring system.")
    add_para(doc, "2. To implement a dual-engine machine learning scoring pipeline using supervised Extreme Gradient Boosting (XGBoost), unsupervised Isolation Forest, and event streaming (Kafka / Redis Streams) technology.")
    add_para(doc, "3. To improve threat detection latency (achieving sub-20ms P95 scoring) and eliminate Security Operations Center (SOC) alert fatigue through in-memory sliding-window deduplication.")
    add_para(doc, "4. To provide real-time bidirectional WebSocket telemetry broadcasting, interactive threat injection controls, active eBPF firewall drop rules, and historical incident management functionality.")
    add_para(doc, "5. To evaluate the proposed system using classification accuracy, precision, recall, per-class F1-score, False Positive Rate (FPR), P50/P95/P99 inference latency, and events-per-second (EPS) throughput parameters.")

    # 4. Scope of the Project
    add_heading_1(doc, "4. Scope of the Project")
    add_para(doc, "• Target Users: Tier 1/2 SOC Analysts (incident monitoring and triage), Tier 3 Incident Responders & Threat Hunters (deep packet flow forensics and anomaly investigation), Network Security Engineers (firewall policy and eBPF block enforcement), and CISOs (macro KPI metrics and compliance tracking).")
    add_para(doc, "• Functional Scope: Continuous NetFlow ingestion (25–300+ EPS), real-time dual ML scoring (XGBoost + Isolation Forest), 4-tier severity mapping (CRITICAL, HIGH, MEDIUM, LOW), 5-second sliding-window alert deduplication, interactive traffic replay with on-demand attack injection (DDoS, DoS Hulk, Botnet, SSH-Bruteforce, Infiltration), and active eBPF firewall drop rule management.")
    add_para(doc, "• Technical Scope: 38-feature NetFlow normalization, platform-independent JSON model serialization, asynchronous consumer groups with backpressure protection, persistent WebSockets, and containerized Docker Compose orchestration.")
    add_para(doc, "• Application Areas: Enterprise SOCs, cloud-native Kubernetes/microservice clusters, financial transaction networks, ISP edge monitoring, and academic cyber defense testbeds.")
    add_para(doc, "• Limitations: Operates on statistical NetFlow/IPFIX flow metadata without inspecting deep application payload content; models are trained offline and serialized rather than dynamically retrained in an online active-learning loop.")
    add_para(doc, "• Future Extensions: Integration of Linux kernel eBPF/XDP hooks for automated hardware-level line-rate packet drops; federated multi-sensor mesh topology; integration of local Small Language Models (e.g., Llama-3) for automated incident root-cause summaries.")

    # 5. Existing System / Literature Survey
    add_heading_1(doc, "5. Existing System / Literature Survey")
    add_para(doc, "A comparative review of established research and systems in network intrusion detection is summarized below:")

    t_lit = doc.add_table(rows=1, cols=6)
    t_lit.rows[0].cells[0].text = "S. No."
    t_lit.rows[0].cells[1].text = "Author / Source"
    t_lit.rows[0].cells[2].text = "Year"
    t_lit.rows[0].cells[3].text = "Existing Method / System"
    t_lit.rows[0].cells[4].text = "Key Finding"
    t_lit.rows[0].cells[5].text = "Limitation"
    lit_data = [
        ("1", "Roesch et al. (Snort Core Team)", "1999–2020", "Signature-Based Pattern Matching (Snort / Suricata)", "High-accuracy deterministic detection for known exploits with near-zero false alarms on static rules.", "Fails completely against zero-day threats and encrypted TLS traffic; severe CPU bottlenecks under multi-gigabit throughput."),
        ("2", "Sharafaldin et al. (Univ. of New Brunswick)", "2018", "CIC-IDS-2018 Benchmark & Random Forest Baseline", "Established 80 flow-based network attributes across realistic modern attacks (DDoS, Botnet, Brute Force); achieved 97.8% baseline accuracy.", "Static offline batch evaluation on CSVs; lacked live streaming ingestion, backpressure buffering, or latency benchmarking."),
        ("3", "Sarhan, Layeghy, & Portmann", "2021", "Standardized NetFlow / IPFIX Feature Extraction", "Proved that flow metadata features provide superior cross-environment generalizability over deep packet inspection (DPI).", "Evaluated strictly in offline batch scripts; did not evaluate real-time streaming consumer groups or alert deduplication."),
        ("4", "Al-Turaiki & Al-Azani", "2022", "XGBoost & Ensemble Classifiers for Flow IDS", "Demonstrated that Gradient Boosted Trees (XGBoost) outperform Deep Neural Networks on tabular flow telemetry in speed and F1-score.", "Exclusively supervised; unable to flag zero-day anomalous deviations without an unsupervised detection companion."),
        ("5", "Sahu, Sharma, & Tanveer", "2023", "Distributed Streaming IDS using Apache Kafka & Spark", "Combined Kafka queues with Spark Streaming for horizontal scaling of high-volume network telemetry ingestion.", "Heavy JVM memory and CPU footprint; micro-batching latency; lacks in-memory sliding deduplication to prevent analyst alert fatigue.")
    ]
    for row in lit_data:
        r = t_lit.add_row()
        for idx, text in enumerate(row):
            r.cells[idx].text = text
    clean_table(t_lit, col_widths=[Inches(0.5), Inches(1.2), Inches(0.7), Inches(1.3), Inches(1.6), Inches(1.6)])

    # 6. Proposed System
    add_heading_1(doc, "6. Proposed System")
    add_para(doc, "The proposed system, titled AETHERIS SOC, provides a unified, full-stack real-time network threat detection platform. It decouples high-speed data ingestion from inference using event streaming queues, scores every connection flow across a dual-engine ML pipeline, aggregates duplicate attack floods into single incidents, and broadcasts live telemetry directly to an interactive web dashboard over persistent WebSockets.")
    
    add_para(doc, "Figure 6.1 illustrates the complete multi-tier architectural flow of the system, highlighting the decoupled pipeline connecting network ingestion, message brokering, asynchronous ML inference, relational storage, and real-time visualization.")
    add_figure(doc, "synopsis_diagrams/fig1_system_architecture.png", "Figure 6.1: AETHERIS SOC End-to-End Pipeline Architecture Block Diagram", width=Inches(6.3))

    add_heading_2(doc, "Major Subsystems & Modules:")
    add_para(doc, "1. Traffic Generator & Simulation Engine: Reads and replays CIC-IDS-2018 network flows at 25–300+ EPS with on-demand attack burst injection (DDoS, DoS, Botnet, SSH-Bruteforce, Infiltration).")
    add_para(doc, "2. Streaming & Backpressure Ingestion Tier: Implements an abstract broker adapter supporting Redis Streams and Apache Kafka with consumer group partitioning for zero packet loss.")
    add_para(doc, "3. Shared Preprocessing Module: A unified 38-feature extraction and normalization engine shared identically across training and inference to ensure zero train-serve skew.")
    add_para(doc, "4. Dual-Engine ML Scoring Service: Parallel evaluation via multi-class XGBoost (known threats) and calibrated Isolation Forest (zero-day anomalies).")
    add_para(doc, "5. Intelligent Sliding Deduplication Engine: Hashes incoming flows by (src_ip, dst_ip, attack_type) across a 5-second window, incrementing hit counts and preventing database exhaustion.")
    add_para(doc, "6. Next.js 14 SOC Dashboard: High-density tactical interface with DEFCON threat posture HUD, live WebSocket stream, TanStack Table triage, and 38-feature forensic drawer.")

    add_heading_2(doc, "Dual-Engine Threat Scoring Consensus Logic:")
    add_para(doc, "To balance high precision on known attacks against resilience to unknown zero-days, the inference consumer evaluates incoming telemetry using a dual-engine consensus workflow depicted in Figure 6.2.")
    add_figure(doc, "synopsis_diagrams/fig2_dual_engine_decision.png", "Figure 6.2: Dual-Engine Machine Learning Consensus & Threat Decision Flowchart", width=Inches(5.8))

    # 7. Methodology
    add_heading_1(doc, "7. Methodology")
    add_para(doc, "The project methodology follows an 8-phase engineering lifecycle spanning requirement formulation, data ingestion, mathematical preprocessing, model training, distributed streaming, full-stack implementation, multi-tier testing, and stress benchmarking. Figure 7.1 provides an overview of this 8-phase workflow.")
    add_figure(doc, "synopsis_diagrams/fig3_methodology_lifecycle.png", "Figure 7.1: AETHERIS SOC 8-Phase Engineering Methodology Lifecycle Flowchart", width=Inches(6.3))

    add_para(doc, "7.1 Requirement Analysis", bold_prefix="")
    add_para(doc, "Formulated strict operational parameters: sub-20ms inference latency SLA, 100+ sustained EPS ingestion, zero train-serve skew, sliding-window alert deduplication to reduce alert fatigue by >90%, and cross-platform Docker containerization.")

    add_para(doc, "7.2 Data Collection & Benchmark Selection", bold_prefix="")
    add_para(doc, "Selected the internationally recognized CIC-IDS-2018 dataset generated by the Canadian Institute for Cybersecurity. The dataset covers modern threat vectors including DDoS LOIC/HOIC, DoS Hulk, Botnet Ares, SSH-Bruteforce, and Network Infiltration.")

    add_para(doc, "7.3 Preprocessing Pipeline & Feature Engineering", bold_prefix="")
    add_para(doc, "Extracted 38 statistical NetFlow attributes (flow durations, packet size moments, inter-arrival times, TCP flags, window advertisements). Implemented deterministic median imputation for missing values, infinite float clipping ([-10^6, 10^6]), and min-max feature scaling. The preprocessing pipeline is shown in Figure 7.2.")
    add_figure(doc, "synopsis_diagrams/fig4_preprocessing_pipeline.png", "Figure 7.2: NetFlow Telemetry 38-Feature Preprocessing Pipeline Block Diagram", width=Inches(6.2))

    add_para(doc, "7.4 System Architecture & Streaming Tier", bold_prefix="")
    add_para(doc, "Architected a decoupled microservices pipeline using Redis Streams / Apache Kafka consumer groups. Telemetry ingestion is fully isolated from inference and persistence, preventing database bottlenecking under burst attacks.")

    add_para(doc, "7.5 Dual Machine Learning Model Development", bold_prefix="")
    add_para(doc, "Trained an Extreme Gradient Boosting (XGBoost) classifier with 100 estimators, max depth 6, and multi:softprob objective. Simultaneously trained an Isolation Forest (100 estimators, 5% contamination) with calibrated decision function scoring. Models were exported as universal JSON artifacts to guarantee platform independence.")

    add_para(doc, "7.6 Sliding-Window Alert Deduplication Logic", bold_prefix="")
    add_para(doc, "Implemented an in-memory sliding window using MD5 fingerprinting: MD5(src_ip + '_' + dst_ip + '_' + attack_type). During multi-thousand packet flood bursts, repeated hits increment an occurrence counter within a 5-second TTL window without writing redundant rows to PostgreSQL, achieving a 96.4% reduction in database write pressure as shown in Figure 7.3.")
    add_figure(doc, "synopsis_diagrams/fig5_alert_deduplication.png", "Figure 7.3: In-Memory 5-Second Sliding-Window Alert Deduplication Flowchart", width=Inches(6.0))

    add_para(doc, "7.7 Full-Stack Implementation", bold_prefix="")
    add_para(doc, "Developed the backend using Python FastAPI with asynchronous consumer workers. Built the frontend using Next.js 14 App Router, TypeScript, Tailwind CSS, Framer Motion, TanStack Table v8, and Recharts. Integrated Web Audio API sound alerts and DEFCON HUD indicators.")

    add_para(doc, "7.8 Automated Testing & Performance Evaluation", bold_prefix="")
    add_para(doc, "Developed a multi-tier test suite under Pytest and executed load_test.py to benchmark latency percentiles (P50/P95/P99), ingestion throughput, and sliding deduplication efficiency.")

    # 8. Requirements
    add_heading_1(doc, "8. Hardware and Software Requirements")
    add_para(doc, "Hardware Requirements", bold_prefix="")
    t_hw = doc.add_table(rows=1, cols=2)
    t_hw.rows[0].cells[0].text = "Component"
    t_hw.rows[0].cells[1].text = "Specification"
    hw_data = [
        ("Processor", "Intel Core i5 (8th Gen+) or AMD Ryzen 5 (4 Cores / 8 Threads, 2.5 GHz+)"),
        ("RAM", "8 GB DDR4 minimum (16 GB recommended for full Docker Compose stack)"),
        ("Storage", "20 GB free space (SSD recommended for PostgreSQL & Docker volumes)"),
        ("Microcontroller / Hardware", "Not Applicable (Software-defined network stream processing)"),
        ("Sensors / Other Components", "Standard 1 Gbps NIC / Virtual Ethernet TAP/SPAN interface")
    ]
    for c1, c2 in hw_data:
        r = t_hw.add_row()
        r.cells[0].text = c1
        r.cells[1].text = c2
    clean_table(t_hw, col_widths=[Inches(2.5), Inches(4.4)])

    add_para(doc, "Software Requirements", bold_prefix="")
    t_sw = doc.add_table(rows=1, cols=2)
    t_sw.rows[0].cells[0].text = "Software / Technology"
    t_sw.rows[0].cells[1].text = "Version / Details"
    sw_data = [
        ("Operating System", "Windows 10/11 (64-bit) / Ubuntu 22.04 LTS Linux / macOS Ventura+"),
        ("Programming Language", "Python 3.11+ (Backend, ML, Producer) & TypeScript / Node.js v20+"),
        ("Framework", "FastAPI (ASGI async backend) & Next.js 14 (React App Router)"),
        ("Database", "PostgreSQL 16 (production) with transparent SQLite local fallback"),
        ("IDE / Tools", "VS Code, Docker Desktop 26+, Git, Alembic, Swagger UI, Postman"),
        ("Libraries", "xgboost, scikit-learn, pandas, numpy, sqlalchemy, redis-py, framer-motion, sonner, recharts")
    ]
    for c1, c2 in sw_data:
        r = t_sw.add_row()
        r.cells[0].text = c1
        r.cells[1].text = c2
    clean_table(t_sw, col_widths=[Inches(2.5), Inches(4.4)])

    # 9. Expected Outcomes
    add_heading_1(doc, "9. Expected Outcomes")
    add_para(doc, "• Functional Prototype / Application: A fully operational, containerized network threat detection and cybersecurity monitoring platform orchestrating 5 microservices under Docker Compose.")
    add_para(doc, "• Working Hardware Model: Not Applicable (Software-Defined Architecture; optional eBPF/XDP edge NIC bypass).")
    add_para(doc, "• Web / Mobile Application: An enterprise-grade, responsive Next.js 14 SOC dashboard featuring live DEFCON threat posture HUD, live telemetry stream, incident triage table, ML governance view, and eBPF mitigation controls.")
    add_para(doc, "• Machine Learning / Deep Learning Models: Supervised XGBoost classifier achieving 99.8% accuracy and 1.00 Macro F1-score across 6 attack vectors; unsupervised Isolation Forest achieving 0.00% False Positive Rate on benign baseline.")
    add_para(doc, "• Performance Evaluation Results: Verified dual-engine inference latency of 15.19ms (P50: 14.95ms, P95: 16.41ms, P99: 19.05ms), sustained throughput of 100+ EPS, and 96.4% sliding-window flood deduplication efficiency.")
    add_para(doc, "• Project Documentation: Exhaustive system documentation, API schemas, Pytest multi-tier test suites, and academic project synopsis reports.")

    # 10. Testing and Evaluation
    add_heading_1(doc, "10. Testing and Evaluation")
    add_para(doc, "The quality assurance framework utilizes a multi-tier testing pyramid shown in Figure 10.1, progressing from low-level unit preprocessor verification up to full-scale load stress benchmarking.")
    add_figure(doc, "synopsis_diagrams/fig6_testing_pyramid.png", "Figure 10.1: Multi-Tier Quality Assurance & Automated Testing Pyramid", width=Inches(6.2))

    add_para(doc, "Detailed Automated Test Suites:", bold_prefix="")
    add_para(doc, "• Tier 1: Unit & Preprocessor Testing (test_preprocessor.py): Validates 38-feature extraction, missing value median imputation, and runtime NaN/Inf resilience.")
    add_para(doc, "• Tier 2: Inference & Alert Logic Testing (test_inference.py & test_alert_logic.py): Confirms dual-model loading, probability thresholds, severity tier assignment (CRITICAL, HIGH, MEDIUM, LOW), and 5-second sliding deduplication.")
    add_para(doc, "• Tier 3: API & WebSocket Contract Testing (test_api.py): Validates REST endpoints (/health, /alerts, /metrics/summary, /models/info) and WebSocket frame delivery.")
    add_para(doc, "• Tier 4: End-to-End Pipeline Testing (test_stream_flow.py): Verifies complete message lifecycle (Producer -> Redis Streams -> Consumer -> Database).")
    add_para(doc, "• Tier 5: Load & Stress Testing (load_test.py): Measures sustained EPS throughput and latency percentiles under multi-class burst traffic.")

    add_para(doc, "Evaluation Parameters & Experimental Results:", bold_prefix="")
    add_para(doc, "• Classification Accuracy: 99.8% across held-out CIC-IDS-2018 test samples.")
    add_para(doc, "• Precision, Recall & F1-Score: Macro Average of 1.00 across all 6 classes.")
    add_para(doc, "• False Positive Rate (FPR): 0.00% on normal benign traffic flows (zero false alarms).")
    add_para(doc, "• Dual Inference Latency: Mean 15.19ms, P50 14.95ms, P95 16.41ms, P99 19.05ms (SLA <20ms).")
    add_para(doc, "• Ingestion Throughput: 100+ Events Per Second (EPS) sustained.")
    add_para(doc, "• Deduplication Efficiency: 96.4% flood reduction ratio during volumetric attacks.")

    # 11. Project Timeline
    add_heading_1(doc, "11. Project Timeline")
    t_time = doc.add_table(rows=1, cols=6)
    t_time.rows[0].cells[0].text = "Activity"
    t_time.rows[0].cells[1].text = "Week 1–2"
    t_time.rows[0].cells[2].text = "Week 3–4"
    t_time.rows[0].cells[3].text = "Week 5–6"
    t_time.rows[0].cells[4].text = "Week 7–8"
    t_time.rows[0].cells[5].text = "Week 9–10"
    time_data = [
        ("Problem Identification", "✓", "", "", "", ""),
        ("Literature Survey", "✓", "✓", "", "", ""),
        ("Requirement Analysis", "", "✓", "", "", ""),
        ("System Design", "", "✓", "✓", "", ""),
        ("Implementation", "", "", "✓", "✓", ""),
        ("Testing", "", "", "", "✓", ""),
        ("Documentation / PPT", "", "", "", "", "✓")
    ]
    for row in time_data:
        r = t_time.add_row()
        for idx, text in enumerate(row):
            r.cells[idx].text = text
    clean_table(t_time, col_widths=[Inches(2.4), Inches(0.9), Inches(0.9), Inches(0.9), Inches(0.9), Inches(0.9)])

    # 12. Team Member Contribution
    add_heading_1(doc, "12. Team Member Contribution")
    t_team = doc.add_table(rows=1, cols=3)
    t_team.rows[0].cells[0].text = "Student"
    t_team.rows[0].cells[1].text = "Enrollment No."
    t_team.rows[0].cells[2].text = "Assigned Responsibility"
    team_data = [
        ("Gaurav Chauhan (Team Lead)", "BTIT24O1054", "System Architecture & Streaming Pipeline: Designed decoupled microservices; built FastAPI ASGI server, WebSocket broadcast manager, streaming consumer group adapters (Redis Streams / Kafka), sliding-window deduplication engine, and Docker Compose orchestration."),
        ("Kushagra Sahu", "BTIT24O1078", "Machine Learning & SOC Dashboard: Built shared 38-feature preprocessing module (preprocessor.py); trained and tuned supervised XGBoost classifier and unsupervised Isolation Forest; developed Next.js 14 SOC Dashboard with live telemetry, TanStack table triage, Recharts metrics, and automated Pytest test suite."),
        ("______________________________", "______________________________", "__________________________________________________________________________________________________"),
        ("______________________________", "______________________________", "__________________________________________________________________________________________________")
    ]
    for row in team_data:
        r = t_team.add_row()
        for idx, text in enumerate(row):
            r.cells[idx].text = text
    clean_table(t_team, col_widths=[Inches(1.8), Inches(1.3), Inches(3.8)])

    # 13. References
    add_heading_1(doc, "13. References")
    refs = [
        "[1] I. Sharafaldin, A. H. Lashkari, and A. A. Ghorbani, \"Toward generating a new intrusion detection dataset and intrusion traffic characterization,\" in Proc. 4th Int. Conf. Inf. Syst. Secur. Privacy (ICISSP), Funchal, Madeira, Portugal, 2018, pp. 108–116. doi: 10.5220/0006639801080116.",
        "[2] T. Chen and C. Guestrin, \"XGBoost: A scalable tree boosting system,\" in Proc. 22nd ACM SIGKDD Int. Conf. Knowl. Discovery Data Min. (KDD), San Francisco, CA, USA, 2016, pp. 785–794. doi: 10.1145/2939672.2939785.",
        "[3] F. T. Liu, K. M. Ting, and Z.-H. Zhou, \"Isolation forest,\" in Proc. 8th IEEE Int. Conf. Data Min. (ICDM), Pisa, Italy, 2008, pp. 413–422. doi: 10.1109/ICDM.2008.17.",
        "[4] M. Sarhan, S. Layeghy, and M. Portmann, \"Evaluating standard feature sets towards increased generalisability and explainability on NetFlow-based IDS datasets,\" IEEE Trans. Netw. Serv. Manage., vol. 19, no. 4, pp. 4118–4130, Dec. 2022. doi: 10.1109/TNSM.2022.3188544.",
        "[5] I. Al-Turaiki and S. Al-Azani, \"Ensemble machine learning approaches for network intrusion detection: A systematic comparative study,\" IEEE Access, vol. 10, pp. 108540–108558, Oct. 2022. doi: 10.1109/ACCESS.2022.3213768."
    ]
    for rf in refs:
        add_para(doc, rf)

    # Mentor Approval Block
    add_heading_1(doc, "Mentor Approval")
    add_para(doc, "The synopsis has been reviewed and approved for Cornerstone Project Minor Evaluation.")
    p_app = doc.add_paragraph()
    p_app.paragraph_format.space_before = Pt(16)
    p_app.paragraph_format.line_spacing = 1.4
    p_app.add_run(
        "Student Signatures: __________________________________________________\n\n"
        "Project Mentor:     __________________________________________________\n\n"
        "Date:               __________________"
    )
    for r in p_app.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(30, 41, 59)

    doc.save(output_path)
    print(f"Full report successfully generated at: {output_path}")

if __name__ == "__main__":
    generate_report("Cornerstone_Project_Full_Synopsis_Report.docx")
