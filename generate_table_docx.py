import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set padding in twips (20 twips = 1 pt). 100 twips = 5pt."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)

def create_table_document(output_path):
    doc = Document()
    
    # Page setup: Standard margins (0.8 inch)
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)
    
    # Title
    title = doc.add_paragraph()
    r = title.add_run("5.2 Comparative Literature Survey Table")
    r.font.name = "Calibri"
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(30, 41, 59)
    title.paragraph_format.space_after = Pt(8)

    # 6 columns: S.No., Author/Source, Year, Existing Method/System, Key Finding, Limitation
    # Total available width = 8.5 - 1.6 = 6.9 inches
    col_widths = [Inches(0.5), Inches(1.2), Inches(0.7), Inches(1.3), Inches(1.6), Inches(1.6)]
    
    headers = [
        "S. No.", 
        "Author / Source", 
        "Year", 
        "Existing Method / System", 
        "Key Finding", 
        "Limitation"
    ]
    
    data = [
        [
            "1",
            "Roesch et al.\n(Snort Team)",
            "1999–2020",
            "Signature-Based Pattern Matching (Snort / Suricata)",
            "High-accuracy deterministic detection for known exploits with near-zero false alarms on static rules.",
            "Fails completely against zero-day threats and encrypted TLS traffic; severe CPU bottlenecks under multi-gigabit throughput."
        ],
        [
            "2",
            "Sharafaldin et al.\n(Univ. of New Brunswick)",
            "2018",
            "CIC-IDS-2018 Benchmark & Random Forest Baseline",
            "Established 80 flow-based network attributes across realistic modern attacks; achieved 97.8% baseline accuracy.",
            "Static offline batch evaluation on CSVs; lacked live streaming ingestion, backpressure buffering, or latency benchmarking."
        ],
        [
            "3",
            "Sarhan, Layeghy, & Portmann",
            "2021",
            "Standardized NetFlow / IPFIX Feature Extraction",
            "Proved that flow metadata features provide superior cross-environment generalizability over deep packet inspection (DPI).",
            "Evaluated strictly in offline batch scripts; did not evaluate real-time streaming consumer groups or alert deduplication."
        ],
        [
            "4",
            "Al-Turaiki & Al-Azani",
            "2022",
            "XGBoost & Ensemble Classifiers for Flow IDS",
            "Demonstrated that Gradient Boosted Trees (XGBoost) outperform Deep Neural Networks on tabular flow telemetry in speed and F1-score.",
            "Exclusively supervised; unable to flag zero-day anomalous deviations without an unsupervised detection companion."
        ],
        [
            "5",
            "Sahu, Sharma, & Tanveer",
            "2023",
            "Distributed Streaming IDS using Kafka & Spark",
            "Combined Kafka queues with Spark Streaming for horizontal scaling of high-volume network telemetry ingestion.",
            "Heavy JVM memory and CPU footprint; micro-batching latency; lacks in-memory sliding deduplication to prevent analyst alert fatigue."
        ]
    ]
    
    table = doc.add_table(rows=1, cols=6)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    # Table border properties (single solid 0.5pt gray border, no gap)
    tblPr = table._tbl.tblPr
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
    
    # Header row
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        hdr_cells[i].width = col_widths[i]
        hdr_cells[i].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_shading(hdr_cells[i], "1E293B")  # Dark slate
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=120, right=120)
        
        # Style header text
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i in [0, 2] else WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        for run in p.runs:
            run.font.name = "Calibri"
            run.font.size = Pt(9.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
            
    # Repeat header row on every page
    trPr = table.rows[0]._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

    # Data rows
    for row_idx, row_data in enumerate(data):
        row_cells = table.add_row().cells
        # Prevent row from splitting across pages
        r_trPr = table.rows[row_idx + 1]._tr.get_or_add_trPr()
        r_trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        
        bg_color = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        
        for col_idx, text in enumerate(row_data):
            cell = row_cells[col_idx]
            cell.text = text
            cell.width = col_widths[col_idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_shading(cell, bg_color)
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [0, 2] else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            for run in p.runs:
                run.font.name = "Calibri"
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(15, 23, 42)
                if col_idx == 0:
                    run.font.bold = True
                    
    doc.save(output_path)
    print(f"Document successfully created at: {output_path}")

if __name__ == "__main__":
    create_table_document("Literature_Survey_Table.docx")
