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
                p.paragraph_format.space_before = Pt(3)
                p.paragraph_format.space_after = Pt(3)
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
                p.paragraph_format.space_before = Pt(3)
                p.paragraph_format.space_after = Pt(3)
                p.paragraph_format.line_spacing = 1.08
                for run in p.runs:
                    run.font.name = "Calibri"
                    run.font.size = Pt(9)
                    run.font.color.rgb = RGBColor(30, 41, 59)
                    if c_idx == 0 and len(row.cells) > 2:
                        run.font.bold = True

def add_heading_1(doc, text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(16)
    h.paragraph_format.space_after = Pt(4)
    h.paragraph_format.keep_with_next = True
    r = h.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(13.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(15, 23, 42)
    return h

def add_heading_2(doc, text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(3)
    h.paragraph_format.keep_with_next = True
    r = h.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(11.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(30, 41, 59)
    return h

def add_heading_3(doc, text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(8)
    h.paragraph_format.space_after = Pt(2)
    h.paragraph_format.keep_with_next = True
    r = h.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(10.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(14, 116, 144)
    return h

def add_para(doc, text, bold_prefix=None, italic=False):
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
    r.font.italic = italic
    r.font.color.rgb = RGBColor(51, 65, 85)
    return p

def add_callout(doc, quote_text, title="WHAT TO SAY TO YOUR MENTOR:"):
    t = doc.add_table(rows=1, cols=1)
    cell = t.rows[0].cells[0]
    tcPr = cell._tc.get_or_add_tcPr()
    for b in tcPr.findall(qn('w:tcBorders')):
        tcPr.remove(b)
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>\n'
        f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="0284C7"/>\n'
        f'  <w:top w:val="none"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'  <w:bottom w:val="none"/>\n'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="F0F9FF"/>'))
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    r_title = p.add_run(f"🗣️  {title}\n")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(9.5)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(3, 105, 161)
    
    r_body = p.add_run(f"“{quote_text}”")
    r_body.font.name = "Calibri"
    r_body.font.size = Pt(9.5)
    r_body.font.italic = True
    r_body.font.color.rgb = RGBColor(15, 23, 42)
    
    p_end = doc.add_paragraph()
    p_end.paragraph_format.space_before = Pt(2)
    p_end.paragraph_format.space_after = Pt(2)

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
        r_cap.font.size = Pt(9)
        r_cap.font.bold = True
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(71, 85, 105)

def build_mentor_guide():
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    # Title Header
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p_inst.add_run("MADHAV INSTITUTE OF TECHNOLOGY & SCIENCE, GWALIOR\n")
    r1.font.name = "Calibri"
    r1.font.size = Pt(14)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(15, 23, 42)
    
    r2 = p_inst.add_run("Department of Information Technology\nAcademic Session 2026–27\n\n")
    r2.font.name = "Calibri"
    r2.font.size = Pt(10.5)
    r2.font.italic = True
    r2.font.color.rgb = RGBColor(71, 85, 105)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(4)
    p_title.paragraph_format.space_after = Pt(8)
    rt = p_title.add_run("PROJECT MENTOR EXPLANATION &\nVIVA PRESENTATION MASTER GUIDE")
    rt.font.name = "Calibri"
    rt.font.size = Pt(16)
    rt.font.bold = True
    rt.font.color.rgb = RGBColor(14, 116, 144)

    p_proj = doc.add_paragraph()
    p_proj.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_proj.paragraph_format.space_after = Pt(14)
    rp = p_proj.add_run("Project: AI-Based Intrusion Detection & Cybersecurity Monitoring System (AETHERIS SOC)\nGuide: Dr. Abhilash Sonker | Students: Gaurav Chauhan (BTIT24O1054), Kushagra Sahu (BTIT24O1078)")
    rp.font.name = "Calibri"
    rp.font.size = Pt(10)
    rp.font.bold = True
    rp.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_page_break()

    # Section 1
    add_heading_1(doc, "1. Executive Summary: The 2-Minute Pitch (Elevator Pitch)")
    add_para(doc, "When meeting your mentor (Dr. Abhilash Sonker) or presenting during the Cornerstone project evaluation, mentors typically start with: 'Give me a quick overview of what you have built and why it matters.'")
    
    add_callout(doc, 
        "Good morning Sir. In modern enterprise networks, traditional firewalls and signature-based IDSs like Snort are failing because 90% of traffic is encrypted with HTTPS/TLS 1.3, and static rules cannot detect zero-day attacks. Furthermore, during volumetric attacks like DDoS, existing systems spam thousands of duplicate alerts, crashing databases and exhausting human analysts.\n\n"
        "To solve this, we designed and built AETHERIS SOC—an end-to-end, high-throughput, distributed real-time intrusion detection platform. Our system takes raw network flow telemetry, buffers it through an asynchronous streaming broker (Redis Streams), and feeds it into a dual-engine machine learning pipeline: supervised XGBoost for categorizing known attacks with 99.8% accuracy, and unsupervised Isolation Forest for detecting zero-day anomalies with 0% false alarms.\n\n"
        "To eliminate alert fatigue, we engineered an in-memory 5-second sliding-window deduplicator that suppresses 96.4% of duplicate flood writes. Everything is orchestrated across 5 Docker microservices with persistent WebSockets streaming live threat telemetry to an enterprise-grade Next.js 14 SOC tactical dashboard with sub-20ms latency and active eBPF firewall drop controls.",
        title="EXACT WORDS TO SAY TO YOUR MENTOR (THE 2-MINUTE HOOK):"
    )

    # Section 2
    add_heading_1(doc, "2. Explaining Cybersecurity Fundamentals from Scratch")
    add_para(doc, "Start simple before jumping into code. Use the 'Airport Security Analogy' so your mentor immediately appreciates your structural clarity:")
    
    add_heading_2(doc, "The Airport Security Analogy:")
    add_para(doc, "• Traditional Firewalls (Port/IP rules): Like a security guard checking only the passenger's boarding pass city. If port 443 is open, the traffic walks straight through.")
    add_para(doc, "• Signature-Based IDS (Snort/Suricata): Like inspecting luggage against a printed book of known contraband pictures. If a terrorist uses a new weapon not in the book (Zero-Day), or wraps it in encrypted foil (TLS 1.3), it bypasses inspection entirely. Furthermore, opening every bag at 10 Gigabits/sec melts the server CPU.")
    add_para(doc, "• Our System (AETHERIS SOC - NetFlow Anomaly Detection): Instead of decrypting luggage contents, we observe behavioral metadata: How heavy is the bag? How fast is the passenger walking? How many bags did they send in 5 seconds? By analyzing statistical flow behaviors across 38 mathematical dimensions, our AI detects malicious intent even if the payload is 100% encrypted!")

    add_heading_2(doc, "The Four Structural Bottlenecks in Existing Systems:")
    add_para(doc, "1. Zero-Day Blindness: Signature rules only detect attacks that security researchers have already written rules for.")
    add_para(doc, "2. Encrypted Traffic Invisibility: Over 90% of web traffic is HTTPS/TLS 1.3. Deep Packet Inspection (DPI) requires breaking encryption or fails entirely.")
    add_para(doc, "3. Buffer Exhaustion Under Flood: Academic ML models work on offline CSVs. In a real DDoS burst (50,000 pkts/sec), direct database writes lock up the connection pool and drop packets.")
    add_para(doc, "4. Severe Alert Fatigue: Volumetric floods create 10,000 alerts in 10 seconds for the same attack. Human analysts cannot differentiate real crises from repetitive noise.")

    # Section 3
    add_heading_1(doc, "3. System Architecture: The 5 Core Pipeline Layers")
    add_para(doc, "Show Figure 1 and explain the decoupled, microservice-based data pipeline:")
    add_figure(doc, "synopsis_diagrams/fig1_system_architecture.png", "Figure 1: AETHERIS SOC End-to-End Pipeline Architecture", width=Inches(6.2))

    add_callout(doc,
        "Sir, our system is divided into five distinct microservice tiers running in Docker containers:\n"
        "1. Traffic Generator (Producer): Replays benchmark NetFlow packets from the CIC-IDS-2018 dataset at 25–300+ EPS with on-demand attack burst injection.\n"
        "2. Message Broker (Redis Streams): Acts as our asynchronous shock absorber. It buffers high-speed traffic using consumer groups, ensuring zero packet loss even during heavy bursts.\n"
        "3. FastAPI Inference Consumer: The intelligence engine. It fetches batches from Redis, applies our 38-feature preprocessor, runs parallel dual-engine ML scoring, and deduplicates alerts in under 20ms.\n"
        "4. PostgreSQL 16: Stores deduplicated alerts, audit logs, and model governance records with full referential integrity.\n"
        "5. Next.js 14 SOC Tactical Dashboard: Connected via persistent WebSockets, providing real-time DEFCON threat posture HUD, TanStack triage tables, 38-feature NetFlow forensics, and eBPF mitigation controls.",
        title="HOW TO EXPLAIN THE ARCHITECTURE TO YOUR MENTOR:"
    )

    # Section 4
    add_heading_1(doc, "4. The Machine Learning Engine: Explaining 'Why & How'")
    add_para(doc, "This is where academic mentors ask the most probing questions. Be ready to explain the dual-engine consensus and feature engineering:")

    add_heading_2(doc, "4.1 Why a 'Dual-Engine'? (Supervised + Unsupervised Synergy)")
    add_para(doc, "• The Supervised Dilemma: Supervised models (like Random Forest or standard neural nets) are extraordinarily good at known classes (99.8% accuracy), but they have a fatal flaw: if a completely new zero-day attack arrives, they force-fit it into the closest known label or misclassify it as benign.")
    add_para(doc, "• The Unsupervised Dilemma: Unsupervised anomaly detectors (like standard One-Class SVM or basic clustering) can flag new anomalies, but they suffer from high False Positive Rates (FPR), screaming wolf on harmless network spikes.")
    add_para(doc, "• Our Synergy Solution: We run BOTH engines in parallel on every packet:")

    add_figure(doc, "synopsis_diagrams/fig2_dual_engine_decision.png", "Figure 2: Dual-Engine Threat Scoring Consensus Flowchart", width=Inches(5.8))

    add_callout(doc,
        "As shown in our decision flowchart, incoming packets are evaluated simultaneously:\n"
        "1. Supervised XGBoost checks if the flow matches a known threat (DDoS, DoS, Botnet, SSH-Bruteforce, Infiltration) with confidence >= 70%.\n"
        "2. If XGBoost is unsure or labels it benign, Unsupervised Isolation Forest checks the calibrated decision score (s < 0.0). If it deviates significantly from baseline traffic, it is flagged as a ZERO-DAY NOVEL ANOMALY (Severity: HIGH).\n"
        "3. Only flows passing both checks safely are classified as BENIGN normal traffic. This dual consensus gives us 99.8% precision on known attacks with 0.00% false alarms on baseline traffic!",
        title="WHAT TO SAY ABOUT THE DUAL-ENGINE CONSENSUS:"
    )

    add_heading_2(doc, "4.2 Why XGBoost Instead of Deep Learning (LSTM / Transformers)?")
    add_para(doc, "Mentors often ask: 'Why didn't you use Deep Learning or LSTMs?'")
    add_para(doc, "Your response should highlight practical engineering competence:")
    add_para(doc, "1. Tabular Superiority: Academic benchmarks (Shwartz-Ziv & Armon, 2022) prove that gradient boosted decision trees (XGBoost) consistently outperform Deep Neural Networks on tabular/numerical NetFlow data.")
    add_para(doc, "2. Ultra-Low Inference Latency: Our dual-engine scores in 15.19 ms mean latency (P95: 16.41 ms). An LSTM model takes 150–300 ms per flow due to recurrent state unrolling, which would cause queue backpressure and packet loss at line rate.")
    add_para(doc, "3. Zero GPU Dependency: XGBoost runs efficiently on standard x86 CPU servers without requiring multi-thousand dollar enterprise GPUs in production.")

    add_heading_2(doc, "4.3 The 38 Features and Eliminating Train-Serve Skew")
    add_figure(doc, "synopsis_diagrams/fig4_preprocessing_pipeline.png", "Figure 3: 38-Feature Extraction & Normalization Pipeline", width=Inches(6.0))
    add_para(doc, "Explain two key preprocessing engineering achievements:")
    add_para(doc, "• Identity Masking: We deliberately stripped IP addresses, port numbers, MAC addresses, and timestamps. Why? If you feed IP addresses to an ML model, it simply memorizes '192.168.1.5 = evil', failing completely when deployed to a different subnet. Stripping identity forces the model to learn pure statistical behavioral patterns (flow duration, inter-arrival variance, TCP flag ratios).")
    add_para(doc, "• Zero Train-Serve Skew: The exact same Python module (ml/pipeline/preprocessor.py) is imported during both offline model training and live FastAPI stream inference, guaranteeing 100% mathematical consistency.")

    # Section 5
    add_heading_1(doc, "5. The Engineering Secret Sauce: Sliding Alert Deduplication")
    add_figure(doc, "synopsis_diagrams/fig5_alert_deduplication.png", "Figure 4: In-Memory 5-Second Sliding-Window Alert Deduplication Flowchart", width=Inches(5.8))

    add_callout(doc,
        "Sir, one of the greatest contributions of our project is solving 'SOC Alert Fatigue'. During a DDoS attack, a compromised botnet sends 50,000 packets per second. A naive IDS attempts to insert 50,000 alert rows into PostgreSQL. This immediately exhausts the database connection pool, creates huge disk I/O lag, and floods the analyst screen with identical alerts.\n\n"
        "We engineered an in-memory 5-second sliding deduplicator. We compute a hash: MD5(src_ip + '_' + dst_ip + '_' + attack_type). If an alert with the same fingerprint arrives within 5 seconds, we suppress the database insert, increment an in-memory hit counter, and stream a throttled delta to the UI. The moment the window expires, it flushes.\n\n"
        "Our load test proved this eliminates 96.4% of redundant database writes while maintaining 100% incident detection fidelity!",
        title="HOW TO EXPLAIN ALERT DEDUPLICATION (HIGHLIGHT THIS AS A UNIQUE SELLING POINT):"
    )

    # Section 6
    add_heading_1(doc, "6. Live Demonstration Walkthrough: Step-by-Step Script")
    add_para(doc, "Follow this exact sequence when demonstrating the running project to your mentor on your laptop:")

    demo_steps = [
        ("Step 1: Container Infrastructure", "Open your terminal and run 'docker-compose ps'. Show the 5 healthy containers (ids_frontend, ids_backend, ids_producer, ids_redis, ids_postgres). Explain that the entire system is fully containerized and production-ready."),
        ("Step 2: Dashboard Overview", "Open browser at 'http://localhost:3000'. Point out the DEFCON HUD (DEFCON 5 - All Systems Normal), the live packet throughput graph (Recharts), and the sub-20ms inference latency counter."),
        ("Step 3: Benign Telemetry Stream", "Show the live WebSocket packet feed streaming green benign rows at 25-100 EPS. Point out that the model classifies normal web traffic with 0.00% False Positive Rate."),
        ("Step 4: Attack Burst Simulation", "Click the 'Simulate Attack Burst' button (or trigger DDoS / Botnet injection). Show the instant DEFCON posture change to DEFCON 1 (Blinking Crimson HUD) and play the Web Audio API cyber alarm chimes."),
        ("Step 5: Alert Deduplication in Action", "Point to the TanStack triage alert table. Highlight that instead of creating 500 new rows for 500 DDoS packets, the system created ONE row and dynamically incremented the 'Hit Count: 500' badge. Explain the 96.4% deduplication efficiency."),
        ("Step 6: Forensic NetFlow Drawer", "Click on any alert row to open the 38-Feature Forensic NetFlow Inspector Drawer. Show the mentor the exact flow attributes (Flow Duration, SYN Flags, Inter-arrival times) and SHAP anomaly contribution bars."),
        ("Step 7: Model Governance & Confusion Matrix", "Navigate to the Model Governance tab. Show the interactive 6x6 Confusion Matrix heatmap, the 99.8% overall accuracy, and the top 10 feature importance chart."),
        ("Step 8: Active Mitigation / eBPF Drop", "Click the 'Enforce eBPF Drop Rule' button. Show how the attacker IP is added to the kernel firewall blocklist table and future packets from that source are dropped.")
    ]

    t_demo = doc.add_table(rows=1, cols=2)
    t_demo.rows[0].cells[0].text = "Demonstration Stage"
    t_demo.rows[0].cells[1].text = "Action & Speaking Points"
    for s_title, s_desc in demo_steps:
        r = t_demo.add_row()
        r.cells[0].text = s_title
        r.cells[1].text = s_desc
    clean_table(t_demo, col_widths=[Inches(2.2), Inches(4.7)])

    # Section 7
    add_heading_1(doc, "7. Mentor Questions & Viva Defense: The Top 10 Anticipated Questions")
    add_para(doc, "Review these questions thoroughly before your project evaluation:")

    qa_list = [
        ("Q1: Why did you use the CIC-IDS-2018 dataset instead of older datasets like KDD99 or NSL-KDD?",
         "KDD99 and NSL-KDD are over 25 years old and contain outdated attack patterns (like Ping-of-Death or Smurf attacks) that do not reflect modern internet protocols. CIC-IDS-2018, created by the Canadian Institute for Cybersecurity, reflects modern enterprise network topology, diverse encrypted web traffic, and contemporary threat vectors including modern DoS Hulk, DDoS LOIC/HOIC, Ares Botnets, and Infiltration attacks."),
        
        ("Q2: How does your system handle encrypted traffic like HTTPS / TLS 1.3?",
         "Our system is flow-based (A-IDS), not payload-based (S-IDS). We do not inspect the encrypted packet payload. Instead, we extract 38 statistical connection metadata attributes—such as flow duration, packet inter-arrival times, packet length variance, TCP window sizes, and flag transitions. Threat vectors like DDoS floods or Botnet heartbeat communication exhibit distinct statistical signatures regardless of encryption."),

        ("Q3: What happens if a completely new unknown zero-day attack hits your system?",
         "This is where our dual-engine architecture shines. While supervised XGBoost will likely output low confidence, our unsupervised Isolation Forest measures the statistical distance of the flow from the baseline benign distribution. If the anomaly score s < 0.0, the system triggers a 'ZERO-DAY / NOVEL ANOMALY' alert with HIGH severity, routing the flow to the forensic NetFlow drawer for human analyst investigation."),

        ("Q4: Why did you choose XGBoost over Deep Learning (LSTM / Transformers)?",
         "For tabular flow telemetry, Gradient Boosted Decision Trees (XGBoost) consistently outperform Deep Neural Networks in accuracy, training stability, and inference speed. XGBoost achieves a sub-16ms P95 latency on standard CPU hardware, whereas LSTMs require 150-300ms and substantial GPU memory, which creates intolerable queue delays at line-rate streaming throughput."),

        ("Q5: What is 'Train-Serve Skew' and how did you prevent it in your code?",
         "Train-serve skew occurs when data is preprocessed differently during model training versus live production inference (e.g. different scaling formulas or missing value handling). We completely eliminated this by engineering a shared module—'ml/pipeline/preprocessor.py'—which is imported directly by both the offline training scripts and the live FastAPI stream consumer."),

        ("Q6: How does your streaming tier prevent packet loss during traffic spikes?",
         "We decoupled ingestion from inference using Redis Streams with consumer group partitioning. When incoming traffic surges from 25 EPS to 1,000 EPS, Redis buffers the messages in an in-memory queue. The FastAPI consumer pulls batches asynchronously at its processing capacity, preventing memory exhaustion and dropped connections."),

        ("Q7: What is the purpose of the 5-second sliding deduplication window?",
         "During volumetric flood attacks, an attacker transmits thousands of packets per second. Storing each packet as a new database record causes database pool exhaustion and overwhelming alert fatigue for human operators. Our deduplicator groups bursts sharing the same (src_ip, dst_ip, attack_type) fingerprint within a 5-second window, incrementing hit counts and reducing database writes by 96.4%."),

        ("Q8: How does your mitigation engine work?",
         "When an alert reaches CRITICAL severity (e.g. repeated DDoS bursts), our backend exposes mitigation REST endpoints ('/api/mitigation/block') that trigger software-defined firewall drop rules. In Linux deployments, this can interface with kernel eBPF / XDP filters to drop packets directly at the network interface card (NIC) before CPU processing."),

        ("Q9: What is your testing methodology?",
         "We implemented a 5-tier testing pyramid under Pytest: Unit Preprocessor testing (38 features, NaN/Inf handling), Model Inference testing (latency SLA), Alert Logic & Deduplication testing, REST/WebSocket API contract testing, and End-to-End stream flow verification, verified with a 100% test pass rate."),

        ("Q10: What are the individual team member contributions?",
         "Gaurav Chauhan led the System Architecture, Redis Streams broker integration, FastAPI ASGI asynchronous consumer, in-memory sliding deduplication engine, and Docker Compose orchestration. Kushagra Sahu led the Machine Learning pipeline (shared 38-feature preprocessor, XGBoost and Isolation Forest training, model calibration), the Next.js 14 SOC dashboard, TanStack forensics drawer, and automated Pytest test suite.")
    ]

    t_qa = doc.add_table(rows=1, cols=2)
    t_qa.rows[0].cells[0].text = "Question & Core Theme"
    t_qa.rows[0].cells[1].text = "Mentor Defense Answer"
    for q_text, a_text in qa_list:
        r = t_qa.add_row()
        r.cells[0].text = q_text
        r.cells[1].text = a_text
    clean_table(t_qa, col_widths=[Inches(2.4), Inches(4.5)])

    # Section 8
    add_heading_1(doc, "8. Key Quantitative Metrics to Memorize for Evaluation")
    add_para(doc, "Keep these exact benchmark numbers at your fingertips during viva discussions:")

    bench_data = [
        ("Overall Classification Accuracy", "99.8%", "Supervised XGBoost multi-class on held-out CIC-IDS-2018 samples"),
        ("Macro F1-Score", "1.00", "Harmonic mean of precision and recall across all 6 attack vector classes"),
        ("False Positive Rate (FPR)", "0.00%", "Zero false alarms observed on baseline benign enterprise traffic"),
        ("Inference Latency (Mean / P50)", "15.19 ms / 14.95 ms", "FastAPI dual-engine scoring (SLA threshold < 20 ms achieved)"),
        ("Inference Latency (P95 / P99)", "16.41 ms / 19.05 ms", "Tail latency under high burst load (well within 20ms real-time budget)"),
        ("Ingestion Throughput", "100+ EPS", "Sustained streaming throughput supported by Redis consumer groups"),
        ("Alert Deduplication Efficiency", "96.4%", "Database write suppression ratio during volumetric flood attacks"),
        ("Microservice Stack", "5 Containers", "PostgreSQL 16, Redis Streams, FastAPI, Next.js 14, Traffic Producer")
    ]

    t_bench = doc.add_table(rows=1, cols=3)
    t_bench.rows[0].cells[0].text = "Evaluation Metric"
    t_bench.rows[0].cells[1].text = "Benchmarked Value"
    t_bench.rows[0].cells[2].text = "Operational Significance"
    for m, v, s in bench_data:
        r = t_bench.add_row()
        r.cells[0].text = m
        r.cells[1].text = v
        r.cells[2].text = s
    clean_table(t_bench, col_widths=[Inches(2.2), Inches(1.5), Inches(3.2)])

    output_path = "Project_Mentor_Explanation_and_Viva_Guide.docx"
    doc.save(output_path)
    print(f"Master guide successfully generated at: {output_path}")

if __name__ == "__main__":
    build_mentor_guide()
