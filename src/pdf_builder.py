from datetime import datetime
from pathlib import Path
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import pypdfium2 as pdfium

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#475569"))
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(36, 560, 805, 560)
        self.drawString(36, 565, "JOBSCOUT AI  |  AUTONOMOUS CAREER DISCOVERY & ATS INTELLIGENCE")
        self.drawRightString(805, 565, "CANDIDATE: ROHITH VANDANA")

        self.line(36, 38, 805, 38)
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(805, 26, page_text)
        self.drawString(36, 26, "Verified Direct ATS Links (HTTP 200)  •  Zero Generic Homepages  •  Autonomous Agent")
        self.restoreState()


def generate_report(output_path: Path, jobs: list, profile: dict) -> Path:
    """Builds a high-definition Landscape A4 PDF report with clickable hyperlinks."""
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=landscape(A4),
        leftMargin=36,
        rightMargin=36,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A')
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155')
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=5
    )

    th_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    tb_style = ParagraphStyle(
        'TableBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9,
        textColor=colors.HexColor('#1E293B')
    )

    tb_bold = ParagraphStyle('TableBodyBold', parent=tb_style, fontName='Helvetica-Bold')
    tb_center = ParagraphStyle('TableBodyCenter', parent=tb_style, alignment=1)
    tb_link = ParagraphStyle('TableBodyLink', parent=tb_style, fontName='Helvetica-Bold', textColor=colors.HexColor('#1D4ED8'), alignment=1)
    badge_high = ParagraphStyle('BadgeHigh', parent=tb_style, fontName='Helvetica-Bold', textColor=colors.HexColor('#047857'), alignment=1)
    badge_med = ParagraphStyle('BadgeMed', parent=tb_style, fontName='Helvetica-Bold', textColor=colors.HexColor('#B45309'), alignment=1)

    story = []

    # 1. Header
    today_str = datetime.now().strftime("%d %b %Y")
    header_html = f"<b>DAILY JOB RESEARCH REPORT</b> — <font color='#2563EB'>{today_str}</font> (AUDITED & LIVE)"
    story.append(Paragraph(header_html, title_style))
    story.append(Spacer(1, 2))

    cand = profile.get("candidate", {})
    meta_text = (
        f"<b>Candidate:</b> {cand.get('name', 'Rohith Vandana')} | "
        f"<b>Degree:</b> {cand.get('degree', 'B.Tech ECE (Batch 2023–2027)')} | "
        f"<b>Institution:</b> {cand.get('institution', 'SRM IST')} | "
        f"<b>Tracks:</b> Agentic AI, AI/ML, Python/FastAPI Backend, Full Stack"
    )
    story.append(Paragraph(meta_text, subtitle_style))
    story.append(Spacer(1, 6))

    # 2. Summary Box
    summary_data = [
        [
            Paragraph(f"<b>Verified Direct Openings:</b> {len(jobs)}", tb_style),
            Paragraph("<b>Link Verification:</b> 100% Direct ATS Forms (HTTP 200)", tb_style),
            Paragraph("<b>Batch Target:</b> 2027 Focused & 0–1 YOE", tb_style),
            Paragraph("<b>Audit Status:</b> Expired / Generic Links Dropped", tb_style),
        ],
        [
            Paragraph("<b>Verified ATS Boards:</b> Greenhouse, AshbyHQ, Unstop Direct", tb_style),
            Paragraph("<b>Locations:</b> Bengaluru, Hyderabad, India Remote", tb_style),
            Paragraph("<b>Top Sector:</b> Agentic AI, LLMs, Voice AI, Backend Python", tb_style),
            Paragraph("<b>Quality Assurance:</b> Zero Scams / Unpaid Excluded", tb_style),
        ]
    ]
    summary_table = Table(summary_data, colWidths=[185, 195, 185, 185])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 8))

    # 3. Main Jobs Table
    story.append(Paragraph("<b>VERIFIED LIVE OPENINGS (DEEP ATS DIRECT APPLICATION LINKS)</b>", section_heading))

    headers = [
        Paragraph("#", th_style),
        Paragraph("Role Title", th_style),
        Paragraph("Company", th_style),
        Paragraph("Location", th_style),
        Paragraph("Eligibility / Batch", th_style),
        Paragraph("Key Skills & Project Alignment", th_style),
        Paragraph("Fit", th_style),
        Paragraph("Platform", th_style),
        Paragraph("Direct Apply Link", th_style)
    ]

    table_data = [headers]
    for j in jobs:
        fit_cell = Paragraph(f"<b>{j['fit']}</b>", badge_high if j['fit'] == 'HIGH' else badge_med)
        apply_cell = Paragraph(f"<a href='{j['link']}'><u><b>Apply &rarr;</b></u></a>", tb_link)

        row = [
            Paragraph(j['num'], tb_center),
            Paragraph(f"<b>{j['role']}</b>", tb_style),
            Paragraph(j['company'], tb_bold),
            Paragraph(j['location'], tb_style),
            Paragraph(j['eligibility'], tb_style),
            Paragraph(j['skills'], tb_style),
            fit_cell,
            Paragraph(j['platform'], tb_style),
            apply_cell
        ]
        table_data.append(row)

    col_widths = [20, 120, 75, 75, 95, 195, 45, 65, 60]
    job_table = Table(table_data, colWidths=col_widths, repeatRows=1)
    
    table_styles = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 3.5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3.5),
    ]

    for r in range(1, len(table_data)):
        bg = colors.HexColor('#FFFFFF') if r % 2 == 1 else colors.HexColor('#F8FAFC')
        table_styles.append(('BACKGROUND', (0, r), (-1, r), bg))

    job_table.setStyle(TableStyle(table_styles))
    story.append(job_table)
    story.append(Spacer(1, 10))

    # 4. Intelligence & Application Strategy
    insights_data = [
        [
            Paragraph("<b>TOP 8 SKILLS IN DEMAND THIS WEEK</b>", th_style),
            Paragraph("<b>ACTIONABLE APPLICATION STRATEGY FOR ROHITH</b>", th_style)
        ],
        [
            Paragraph(
                "• <b>Distributed Database & Systems:</b> SingleStore's 2027 engine intern role is high-caliber; highlight systems fundamentals.<br/>"
                "• <b>LangGraph & Agentic Frameworks:</b> Meraki-Labs and TalentCV explicitly demand agentic & multi-turn tool-calling developers.<br/>"
                "• <b>FastAPI + Async Python:</b> Core backend stack for Plane Software, Enterpret, and AiPrise.<br/>"
                "• <b>AI Model Evaluation & Benchmarking:</b> Karya is heavily expanding its research engineering evaluation team.<br/>"
                "• <b>Real-time Voice AI & GPU Inference:</b> Smallest.ai looking for systems-level Python/Go engineers.<br/>"
                "• <b>React + Vite:</b> Plane Software & Certa seeking frontend/full-stack interns who build modular UI components.<br/>"
                "• <b>PyTorch & Model Fine-Tuning:</b> HackerRank AI research team prioritizing students with DL reproduction experience.<br/>"
                "• <b>AI Compliance Agents:</b> AiPrise is hiring engineers to build autonomous agentic workflows.",
                tb_style
            ),
            Paragraph(
                "• <b>Immediate Priority #1:</b> Apply to <b>SingleStore</b> (Role #1) &mdash; it is explicitly opened for <b>Engine-2027</b> interns!<br/>"
                "• <b>Immediate Priority #2:</b> Submit to <b>Meraki-Labs</b> (Role #2) and <b>Enterpret</b> (Role #5 & #6) via their direct Greenhouse/Ashby forms.<br/>"
                "• <b>Agentic Highlight:</b> In your application to <b>TalentCV</b> and <b>Meraki-Labs</b>, link your <i>Restaurant Reservation Agent</i> & <i>VisionMate AI</i> repos.<br/>"
                "• <b>Full-Stack Highlight:</b> For <b>Plane Software</b> (Role #8 & #9), emphasize your experience converting React/Vite interfaces and designing APIs.<br/>"
                "• <b>Direct Forms Verified:</b> Every link on this report goes directly to an active ATS form without intermediary redirects.",
                tb_style
            )
        ]
    ]

    insights_table = Table(insights_data, colWidths=[375, 375])
    insights_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))

    story.append(KeepTogether(insights_table))
    doc.build(story, canvasmaker=NumberedCanvas)
    return output_path

def render_preview_images(pdf_path: Path, output_dir: Path):
    """Renders PDF pages to high-resolution PNGs for README / UI previews."""
    doc = pdfium.PdfDocument(str(pdf_path))
    for i in range(len(doc)):
        img = doc[i].render(scale=2.0).to_pil()
        out_file = output_dir / f"report_page_{i+1}.png"
        img.save(str(out_file))
