import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def clean_table(table, col_widths=None, header_bg="1E293B", zebra=True):
    tblPr = table._tbl.tblPr
    
    # 1. Remove cell spacing (fixes the double borders and cell distortion!)
    for sp in tblPr.findall(qn('w:tblCellSpacing')):
        tblPr.remove(sp)
        
    # 2. Set clean table borders (single solid border)
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
    
    # 3. Set standard cell padding margins
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

    # Format header row
    if len(table.rows) > 0:
        header_tr = table.rows[0]._tr
        trPr = header_tr.get_or_add_trPr()
        if not trPr.findall(qn('w:tblHeader')):
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
            
        for c_idx, cell in enumerate(table.rows[0].cells):
            # remove individual tcBorders to prevent double lines
            tcPr = cell._tc.get_or_add_tcPr()
            for b in tcPr.findall(qn('w:tcBorders')):
                tcPr.remove(b)
            # set header background
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
                    
    # Format data rows
    for r_idx, row in enumerate(table.rows[1:], start=1):
        trPr = row._tr.get_or_add_trPr()
        if not trPr.findall(qn('w:cantSplit')):
            trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
            
        bg_color = "F8FAFC" if (zebra and r_idx % 2 == 1) else "FFFFFF"
        
        for c_idx, cell in enumerate(row.cells):
            tcPr = cell._tc.get_or_add_tcPr()
            # remove individual borders
            for b in tcPr.findall(qn('w:tcBorders')):
                tcPr.remove(b)
            # background shading
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

def process_synopsis_doc(input_file, output_file):
    doc = Document(input_file)
    
    # 1. Update Title and Fill blanks on Cover Page
    for p in doc.paragraphs[:20]:
        if "____________________________________________" in p.text:
            p.text = "“AI-BASED INTRUSION DETECTION & CYBERSECURITY MONITORING SYSTEM”"
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(14)
                r.font.bold = True
                r.font.color.rgb = RGBColor(15, 23, 42)
        elif "Designation: ______________________________" in p.text:
            p.text = "Designation: Assistant Professor"
        elif "School of _____________________________" in p.text:
            p.text = "Department of Information Technology"
            
    # Clean text in all paragraphs (replace non-breaking space \xa0 with space)
    for p in doc.paragraphs:
        if '\xa0' in p.text:
            for r in p.runs:
                r.text = r.text.replace('\xa0', ' ')

    # 2. Table Column Widths (for 6.9 inches available width)
    # Table 1: Team Members (S. No., Name, Enrollment No.)
    col_w1 = [Inches(1.0), Inches(3.2), Inches(2.7)]
    clean_table(doc.tables[0], col_widths=col_w1)
    
    # Table 2: 5.2 Comparative Literature Survey (S. No., Author, Year, Method, Key Finding, Limitation)
    col_w2 = [Inches(0.5), Inches(1.2), Inches(0.7), Inches(1.3), Inches(1.6), Inches(1.6)]
    clean_table(doc.tables[1], col_widths=col_w2)
    
    # Table 3: Expected Improvements (Metric, Traditional, Proposed, Advantage)
    col_w3 = [Inches(1.3), Inches(1.8), Inches(2.0), Inches(1.8)]
    clean_table(doc.tables[2], col_widths=col_w3)
    
    # Table 4: 8.1 Hardware Requirements (Component, Min, Recommended)
    col_w4 = [Inches(1.8), Inches(2.55), Inches(2.55)]
    clean_table(doc.tables[3], col_widths=col_w4)
    
    # Table 5: 8.2 Software Requirements (Software/Tech, Version/Details)
    col_w5 = [Inches(2.3), Inches(4.6)]
    clean_table(doc.tables[4], col_widths=col_w5)
    
    # Table 6: 12 Team Member Contribution (Update with Gaurav & Kushagra)
    # The original table has 5 rows (Header + 4 members). Let's update rows for 2 members!
    t6 = doc.tables[5]
    if len(t6.rows) >= 5:
        # Row 1: Gaurav Chauhan
        t6.rows[1].cells[0].paragraphs[0].text = "Gaurav Chauhan (Team Lead)"
        t6.rows[1].cells[1].paragraphs[0].text = "BTIT24O1054"
        t6.rows[1].cells[2].paragraphs[0].text = (
            "System Architecture & Streaming Pipeline: Designed decoupled microservices architecture; "
            "built FastAPI ASGI server, WebSocket broadcast manager, streaming consumer group adapters "
            "(Redis Streams / Kafka), sliding-window deduplication engine, and Docker Compose orchestration."
        )
        # Row 2: Kushagra Sahu
        t6.rows[2].cells[0].paragraphs[0].text = "Kushagra Sahu"
        t6.rows[2].cells[1].paragraphs[0].text = "BTIT24O1078"
        t6.rows[2].cells[2].paragraphs[0].text = (
            "Machine Learning & SOC Dashboard: Built shared 38-feature preprocessing module (preprocessor.py); "
            "trained and tuned supervised XGBoost classifier and unsupervised Isolation Forest; developed Next.js 14 "
            "SOC Dashboard with live telemetry, TanStack table triage, Recharts metrics, and automated Pytest test suite."
        )
        # Remove extra rows 3 and 4 if only 2 team members
        t6._tbl.remove(t6.rows[4]._tr)
        t6._tbl.remove(t6.rows[3]._tr)
        
    col_w6 = [Inches(1.8), Inches(1.3), Inches(3.8)]
    clean_table(doc.tables[5], col_widths=col_w6)
    
    # 3. Replace ASCII Box in Testing Section (paragraphs 445-468) with a real Word Table
    # Let's find the ASCII table paragraph range
    ascii_start = -1
    ascii_end = -1
    for idx, p in enumerate(doc.paragraphs):
        if "MULTI-TIER TESTING PYRAMID" in p.text:
            ascii_start = idx - 1  # top border
        if ascii_start != -1 and "load_test.py: Measures sustained" in p.text:
            ascii_end = idx + 2
            break
            
    if ascii_start != -1 and ascii_end != -1:
        # Clear the ASCII text from those paragraphs
        for idx in range(ascii_start, ascii_end):
            p = doc.paragraphs[idx]
            p.text = ""
        # In the first paragraph, insert a real table!
        target_p = doc.paragraphs[ascii_start]
        target_p.text = "Table: Multi-Tier Testing Pyramid"
        target_p.runs[0].font.bold = True
        target_p.runs[0].font.size = Pt(11)
        target_p.paragraph_format.space_before = Pt(8)
        target_p.paragraph_format.space_after = Pt(4)
        
        # Add table after target paragraph
        test_table = doc.add_table(rows=1, cols=2)
        # Move table right after target_p
        target_p._p.addnext(test_table._tbl)
        
        test_headers = ["Testing Tier", "Scope, Test Suite & Objective"]
        for c_idx, h in enumerate(test_headers):
            test_table.rows[0].cells[c_idx].text = h
            
        test_data = [
            ("Unit Testing", "test_preprocessor.py: Verifies 38-feature extraction, missing value median imputation, and runtime NaN/Inf resilience."),
            ("Inference Testing", "test_inference.py: Validates model loading, memory warmup, class probability outputs, and sub-20ms latency."),
            ("Alert Logic Testing", "test_alert_logic.py: Evaluates dynamic severity tier assignments and sliding-window deduplication (aggregates flood packets into single incident)."),
            ("API & WS Testing", "test_api.py: Validates REST endpoints (/health, /alerts, /metrics) and bi-directional WebSocket ping/pong frame broadcast."),
            ("End-to-End Testing", "test_stream_flow.py: Verifies complete asynchronous message lifecycle (Producer -> Redis Streams -> Consumer -> Database)."),
            ("Load / Stress Testing", "load_test.py: Measures sustained EPS throughput (100+ EPS), queue drain performance, and P50/P95/P99 latency under volumetric floods.")
        ]
        for tier, desc in test_data:
            r = test_table.add_row()
            r.cells[0].text = tier
            r.cells[1].text = desc
            
        clean_table(test_table, col_widths=[Inches(2.0), Inches(4.9)])

    # 4. Insert Section 11 Gantt Timeline Table if missing
    for idx, p in enumerate(doc.paragraphs):
        if p.text.strip() == "11. Project Timeline":
            # Add table right after paragraph
            timeline_table = doc.add_table(rows=1, cols=6)
            p._p.addnext(timeline_table._tbl)
            
            tl_headers = ["Activity", "Week 1–2", "Week 3–4", "Week 5–6", "Week 7–8", "Week 9–10"]
            for c_idx, h in enumerate(tl_headers):
                timeline_table.rows[0].cells[c_idx].text = h
                
            tl_rows = [
                ("Problem Identification", "✓", "", "", "", ""),
                ("Literature Survey", "✓", "✓", "", "", ""),
                ("Requirement Analysis", "", "✓", "", "", ""),
                ("System Design", "", "✓", "✓", "", ""),
                ("Implementation", "", "", "✓", "✓", ""),
                ("Testing & Benchmarking", "", "", "", "✓", ""),
                ("Documentation & PPT", "", "", "", "", "✓")
            ]
            for act, w1, w2, w3, w4, w5 in tl_rows:
                r = timeline_table.add_row()
                r.cells[0].text = act
                r.cells[1].text = w1
                r.cells[2].text = w2
                r.cells[3].text = w3
                r.cells[4].text = w4
                r.cells[5].text = w5
                
            tl_col_w = [Inches(2.4), Inches(0.9), Inches(0.9), Inches(0.9), Inches(0.9), Inches(0.9)]
            clean_table(timeline_table, col_widths=tl_col_w)
            break

    doc.save(output_file)
    print(f"Successfully processed and formatted: {output_file}")

if __name__ == "__main__":
    process_synopsis_doc(
        "MITS_Cornerstone_Project_Synopsis_Format.docx", 
        "MITS_Cornerstone_Project_Synopsis_Formatted.docx"
    )
