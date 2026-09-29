#!/usr/bin/env python3
"""Build a styled DOCX report and 17-slide PPTX from the enterprise submission sources."""
from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_ROW_HEIGHT_RULE, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from pptx import Presentation
from pptx.dml.color import RGBColor as SlideColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches as SlideInches, Pt as SlidePt

BASE = Path(__file__).resolve().parent
REPORT_MD = BASE / "enterprise_project_report.md"
REPORT_DOCX = BASE / "UC007_Claims_Processing_Project_Report.docx"
PRESENTATION = BASE / "UC007_Claims_Processing_Enterprise_Presentation.pptx"

INK = "17324D"
TEAL = "087E8B"
PALE = "EAF2F5"
MUTED = "526575"


def _shade(cell, fill):
    props = cell._tc.get_or_add_tcPr()
    shade = OxmlElement("w:shd")
    shade.set(qn("w:fill"), fill)
    props.append(shade)


def _inline(paragraph, text):
    for token in re.split(r"(`[^`]+`|\*\*[^*]+\*\*)", text):
        if not token:
            continue
        if token.startswith("**"):
            paragraph.add_run(token[2:-2]).bold = True
        elif token.startswith("`"):
            run = paragraph.add_run(token[1:-1])
            run.font.name = "Aptos Mono"
            run.font.size = Pt(8.5)
            run.font.color.rgb = RGBColor.from_string(TEAL)
        else:
            paragraph.add_run(token)


def _word_table(document, rows):
    if not rows:
        return
    table = document.add_table(rows=1, cols=len(rows[0]))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for ri, row in enumerate(rows):
        cells = table.rows[0].cells if ri == 0 else table.add_row().cells
        for ci, value in enumerate(row):
            cell = cells[ci]
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if ri == 0:
                _shade(cell, INK)
            elif ri % 2 == 0:
                _shade(cell, "F2F6F7")
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            _inline(p, value)
            for run in p.runs:
                run.font.size = Pt(8.5)
                if ri == 0:
                    run.bold = True
                    run.font.color.rgb = RGBColor(255, 255, 255)


def _screenshot_placeholder(document, label, height):
    table = document.add_table(rows=1, cols=1)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(6.7)
    row = table.rows[0]
    row.height = Inches(height)
    row.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
    cell = row.cells[0]
    cell.width = Inches(6.7)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    _shade(cell, "F6F9FA")
    paragraph = cell.paragraphs[0]
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run(f"PASTE SCREENSHOT HERE\n{label}")
    run.font.name = "Aptos"
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = RGBColor.from_string(MUTED)


def build_docx():
    lines = REPORT_MD.read_text(encoding="utf-8").splitlines()
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Inches(0.72)
    section.bottom_margin = Inches(0.72)
    section.left_margin = Inches(0.78)
    section.right_margin = Inches(0.78)
    normal = doc.styles["Normal"]
    normal.font.name = "Aptos"
    normal.font.size = Pt(9.5)
    normal.font.color.rgb = RGBColor.from_string(INK)
    normal.paragraph_format.space_after = Pt(5)
    normal.paragraph_format.line_spacing = 1.08
    for name, size, color in (("Title", 26, INK), ("Heading 1", 17, INK), ("Heading 2", 12, TEAL), ("Heading 3", 10, INK)):
        style = doc.styles[name]
        style.font.name = "Aptos Display"
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor.from_string(color)
        style.paragraph_format.keep_with_next = True
    header = section.header.paragraphs[0]
    header.text = "UC007  /  CLAIMS PROCESSING AGENT                                        PROJECT REPORT"
    for run in header.runs:
        run.font.size = Pt(8)
        run.font.color.rgb = RGBColor.from_string(MUTED)
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    footer.add_run("Fictional training environment  |  ").font.size = Pt(8)
    field = OxmlElement("w:fldSimple")
    field.set(qn("w:instr"), "PAGE")
    footer._p.append(field)

    i = 0
    in_code = False
    code = []
    while i < len(lines):
        raw = lines[i]
        text = raw.strip()
        if text.startswith("```"):
            if in_code:
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Inches(0.15)
                run = p.add_run("\n".join(code))
                run.font.name = "Aptos Mono"
                run.font.size = Pt(8)
                code = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue
        if in_code:
            code.append(raw)
            i += 1
            continue
        if not text or text == "---":
            i += 1
            continue
        screenshot = re.fullmatch(r"\[\[SCREENSHOT:\s*(.*?)\s*\|\s*([\d.]+)\]\]", text)
        if screenshot:
            _screenshot_placeholder(doc, screenshot.group(1), float(screenshot.group(2)))
            doc.add_paragraph().paragraph_format.space_after = Pt(0)
            i += 1
            continue
        if text.startswith("|"):
            gathered = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                gathered.append([v.strip() for v in lines[i].strip().strip("|").split("|")])
                i += 1
            parsed = [row for row in gathered if not all(re.fullmatch(r":?-{3,}:?", v.replace(" ", "")) for v in row)]
            _word_table(doc, parsed)
            doc.add_paragraph().paragraph_format.space_after = Pt(0)
            continue
        if text.startswith("> "):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.18)
            p.paragraph_format.right_indent = Inches(0.12)
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(8)
            sh = OxmlElement("w:shd")
            sh.set(qn("w:fill"), PALE)
            p._p.get_or_add_pPr().append(sh)
            _inline(p, text[2:])
            i += 1
            continue
        heading = re.match(r"^(#{1,3})\s+(.+)$", text)
        if heading:
            level = len(heading.group(1))
            title = heading.group(2)
            style = "Title" if level == 1 and i < 4 else f"Heading {max(1, level - 1)}"
            _inline(doc.add_paragraph(style=style), title)
            i += 1
            continue
        match = re.match(r"^[-*]\s+(.+)$", text)
        numbered = re.match(r"^\d+\.\s+(.+)$", text)
        if match or numbered:
            p = doc.add_paragraph(style="List Bullet" if match else "List Number")
            _inline(p, (match or numbered).group(1))
            p.paragraph_format.space_after = Pt(2)
            i += 1
            continue
        p = doc.add_paragraph()
        _inline(p, text)
        i += 1
    doc.core_properties.title = "UC007 Claims Processing Agent - Project Report"
    doc.core_properties.subject = "AI-assisted motor claims review and decision support"
    doc.core_properties.author = "Manoj Deepak (FDE user 42) <bolleddu.deepak@wipro.com>"
    doc.save(REPORT_DOCX)
    print(f"Created: {REPORT_DOCX}")


# Presentation theme
C = {
    "ink": SlideColor(23, 50, 77), "blue": SlideColor(34, 103, 155),
    "teal": SlideColor(8, 126, 139), "green": SlideColor(40, 125, 101),
    "amber": SlideColor(196, 128, 36), "red": SlideColor(174, 73, 66),
    "muted": SlideColor(83, 103, 120), "pale": SlideColor(239, 245, 247),
    "pale_blue": SlideColor(232, 241, 247), "pale_teal": SlideColor(229, 243, 242),
    "pale_amber": SlideColor(250, 243, 229), "pale_red": SlideColor(248, 237, 235),
    "white": SlideColor(255, 255, 255), "line": SlideColor(205, 218, 225),
}
SW, SH = 13.333, 7.5


def _in(v):
    return SlideInches(v)


def _box(slide, x, y, w, h, text="", size=13, color=None, bold=False, align=PP_ALIGN.LEFT,
         font="Aptos", valign=MSO_ANCHOR.TOP, margin=0.03):
    shape = slide.shapes.add_textbox(_in(x), _in(y), _in(w), _in(h))
    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = _in(margin)
    tf.margin_right = _in(margin)
    tf.margin_top = _in(margin)
    tf.margin_bottom = _in(margin)
    tf.vertical_anchor = valign
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = align
    p.font.name = font
    p.font.size = SlidePt(size)
    p.font.bold = bold
    p.font.color.rgb = color or C["ink"]
    return shape


def _rect(slide, x, y, w, h, fill, outline=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, _in(x), _in(y), _in(w), _in(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = outline or fill
    shape.line.width = SlidePt(0.8)
    return shape


def _line(slide, x1, y1, x2, y2, color=None, width=1.1, arrow=False):
    shape = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, _in(x1), _in(y1), _in(x2), _in(y2))
    shape.line.color.rgb = color or C["line"]
    shape.line.width = SlidePt(width)
    if arrow:
        shape.line.end_arrowhead = True
    return shape


def _footer(slide, number, dark=False):
    col = SlideColor(195, 211, 222) if dark else C["muted"]
    _line(slide, 0.55, 7.08, 12.78, 7.08, SlideColor(64, 91, 112) if dark else C["line"], 0.7)
    _box(slide, 0.62, 7.15, 7.5, 0.2, "UC007  /  FICTIONAL TRAINING ENVIRONMENT", 8, col)
    _box(slide, 11.9, 7.13, 0.7, 0.22, f"{number:02d}", 9, col, True, align=PP_ALIGN.RIGHT)


def _slide(prs, title, subtitle=""):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = C["white"]
    _rect(s, 0, 0, SW, 0.09, C["teal"])
    _box(s, 0.62, 0.32, 11.9, 0.22, "CLAIMS PROCESSING AGENT", 9, C["teal"], True)
    _box(s, 0.62, 0.65, 12, 0.5, title, 25, C["ink"], True, font="Aptos Display")
    if subtitle:
        _box(s, 0.64, 1.2, 12, 0.36, subtitle, 11, C["muted"])
    _footer(s, len(prs.slides))
    return s


def _table(slide, x, y, widths, rows, row_h=0.58, font=10):
    for ri, row in enumerate(rows):
        xx = x
        for ci, val in enumerate(row):
            fill = C["ink"] if ri == 0 else (C["pale"] if ri % 2 else C["white"])
            _rect(slide, xx, y + ri * row_h, widths[ci], row_h, fill, C["line"])
            _box(slide, xx + 0.07, y + ri * row_h + 0.05, widths[ci] - 0.14, row_h - 0.08,
                 val, font, C["white"] if ri == 0 else C["ink"], ri == 0 or ci == 0,
                 valign=MSO_ANCHOR.MIDDLE)
            xx += widths[ci]


def _bullets(slide, x, y, w, items, gap=0.52, size=12, color=None):
    for i, item in enumerate(items):
        yy = y + i * gap
        _rect(slide, x, yy + 0.09, 0.08, 0.08, color or C["teal"])
        _box(slide, x + 0.2, yy, w - 0.2, gap - 0.02, item, size, C["ink"])


def _metric(slide, x, y, w, value, label, note, color):
    _box(slide, x, y, w, 0.52, value, 27, color, True, font="Aptos Display")
    _box(slide, x, y + 0.57, w, 0.32, label, 11, C["ink"], True)
    _box(slide, x, y + 0.96, w, 0.47, note, 9, C["muted"])


def build_pptx():
    prs = Presentation()
    prs.slide_width, prs.slide_height = _in(SW), _in(SH)

    # 1 Cover
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid(); s.background.fill.fore_color.rgb = C["ink"]
    _rect(s, 0, 0, 0.16, SH, C["teal"])
    _box(s, 0.82, 0.78, 10.8, 0.3, "UC007  /  MICROSOFT FDE CAPSTONE", 10, SlideColor(116, 207, 204), True)
    _box(s, 0.82, 1.43, 11.2, 1.35, "AI-assisted motor\nclaims review", 34, C["white"], True, font="Aptos Display")
    _box(s, 0.86, 3.12, 9.7, 0.72, "Evidence in. Explainable preparation out.\nA human handler remains accountable.", 17, SlideColor(216, 229, 236))
    _line(s, 0.86, 4.32, 8.7, 4.32, SlideColor(76, 110, 132))
    _box(s, 0.86, 4.62, 4.5, 0.32, "CONTOSO CLAIMS WORKSPACE", 11, C["white"], True)
    _box(s, 0.86, 5.02, 6.3, 0.55, "Capstone project presentation  |  2026", 12, SlideColor(188, 207, 218))
    _box(s, 0.86, 5.7, 8.3, 0.36, "Manoj Deepak  |  FDE user 42  |  bolleddu.deepak@wipro.com", 10, SlideColor(188, 207, 218))
    _rect(s, 9.55, 1.44, 2.5, 3.72, SlideColor(29, 67, 91), SlideColor(63, 109, 132))
    _box(s, 9.82, 1.78, 2.0, 0.35, "THE BOUNDARY", 10, SlideColor(116, 207, 204), True)
    _box(s, 9.82, 2.35, 1.92, 1.7, "Prepare\nExplain\nRecommend", 19, C["white"], True, font="Aptos Display")
    _line(s, 9.82, 4.26, 11.7, 4.26, SlideColor(63, 109, 132))
    _box(s, 9.82, 4.47, 1.95, 0.46, "Human decides", 13, C["white"], True)
    _footer(s, 1, True)

    # 2 Snapshot
    s = _slide(prs, "Executive snapshot", "A focused capstone prototype for evidence-heavy motor-claim preparation")
    for x, val, label, note, color in [
        (0.82, "5", "Synthetic claims", "Normal, missing, conflict, policy, risk", C["teal"]),
        (3.28, "45/45", "Extraction matches", "Reported sample result", C["blue"]),
        (5.74, "11/11", "Expected findings", "Zero spurious distinct codes", C["green"]),
        (8.20, "5/5", "Recommendations", "Agent and rules match expected", C["amber"]),
        (10.66, "0", "Safety phrases", "Reported evaluator violations", C["red"]),
    ]:
        _rect(s, x, 2.05, 1.86, 2.05, C["white"], C["line"])
        _rect(s, x, 2.05, 1.86, 0.07, color)
        _metric(s, x + 0.12, 2.35, 1.62, val, label, note, color)
    _rect(s, 0.95, 4.75, 11.4, 0.82, C["pale_amber"], C["amber"])
    _box(s, 1.15, 4.93, 11.0, 0.4, "Reported prior results; raw `out/` JSON is absent from this checkout, so the run could not be replayed.", 12, C["ink"], True, align=PP_ALIGN.CENTER)
    _box(s, 1.05, 5.9, 11.2, 0.38, "Five synthetic scenarios demonstrate workflow behavior, not production accuracy or business impact.", 11, C["muted"], align=PP_ALIGN.CENTER)

    # 3 Problem
    s = _slide(prs, "Why claims preparation is hard", "Evidence is fragmented; facts and decision authority are not")
    blocks = [
        (0.82, "Evidence fragmentation", "Forms, statements, police reports, schedules, estimates, and photographs arrive in different formats.", C["blue"]),
        (4.84, "Cross-source uncertainty", "Dates, VINs, damage areas, required items, and costs can be missing or contradictory.", C["amber"]),
        (8.86, "Decision sensitivity", "Coverage, referral, and payment outcomes require accountable authorised staff.", C["red"]),
    ]
    for x, title, body, color in blocks:
        _rect(s, x, 2.0, 3.62, 0.06, color)
        _box(s, x + 0.08, 2.2, 3.45, 0.4, title, 15, C["ink"], True, font="Aptos Display")
        _box(s, x + 0.08, 2.75, 3.42, 1.2, body, 12, C["muted"])
    _box(s, 0.92, 4.45, 11.4, 0.3, "DESIGN OBJECTIVE", 10, C["teal"], True)
    _box(s, 0.92, 4.87, 11.35, 0.9, "Reduce evidence-search effort and improve consistency, while keeping every claim outcome outside the automated decision boundary.", 18, C["ink"], True, font="Aptos Display")

    # 4 Scope
    s = _slide(prs, "What the workspace does", "A review-support workflow, not an insurer core system")
    _box(s, 0.9, 1.9, 5.2, 0.3, "IN SCOPE", 10, C["green"], True)
    _bullets(s, 0.92, 2.32, 5.2, ["Discover and classify sample evidence", "Extract facts and confidence values", "Assess visible damage and compare indicative bands", "Run repeatable policy and consistency checks", "Generate an evidence-backed next-step recommendation", "Record a named preparation-review action"], 0.52, 12, C["green"])
    _line(s, 6.55, 1.9, 6.55, 5.45)
    _box(s, 6.95, 1.9, 5.2, 0.3, "NOT IN SCOPE", 10, C["red"], True)
    _bullets(s, 6.98, 2.32, 5.2, ["Approve, decline, settle, or pay a claim", "Make final coverage or liability decisions", "Allege fraud or assign fraud probability", "Authenticate/authorize production users", "Provide durable distributed processing", "Prove savings on representative volumes"], 0.52, 12, C["red"])

    # 5 Workflow
    s = _slide(prs, "End-to-end preparation flow", "The pipeline turns a claim folder into a human-review package")
    steps = [("01", "Discover", "Files + inferred type", C["blue"]), ("02", "Extract", "Structured facts", C["teal"]), ("03", "Assess", "Visible damage", C["green"]), ("04", "Validate", "Rules + policy", C["amber"]), ("05", "Explain", "Summary + next step", C["blue"]), ("06", "Review", "Named handler", C["ink"])]
    xs = [0.65, 2.78, 4.91, 7.04, 9.17, 11.3]
    for i, (num, title, detail, color) in enumerate(steps):
        x = xs[i]
        _rect(s, x, 2.35, 1.7, 1.55, C["white"], C["line"])
        _rect(s, x, 2.35, 0.07, 1.55, color)
        _box(s, x + 0.16, 2.48, 0.5, 0.25, num, 10, color, True)
        _box(s, x + 0.16, 2.82, 1.4, 0.3, title, 13, C["ink"], True)
        _box(s, x + 0.16, 3.2, 1.42, 0.52, detail, 9, C["muted"])
        if i < 5:
            _line(s, x + 1.73, 3.12, xs[i + 1] - 0.06, 3.12, C["muted"], 1.1, True)
    _rect(s, 0.82, 4.65, 11.7, 0.75, C["pale_teal"], C["teal"])
    _box(s, 1.02, 4.83, 11.3, 0.35, "Human gate: the workspace recommends a safe next step; authorised staff own the claim outcome.", 13, C["ink"], True, align=PP_ALIGN.CENTER)
    _box(s, 0.9, 5.72, 11.5, 0.44, "Azure Content Understanding  •  Azure OpenAI vision  •  Python rules  •  Azure AI Search / MCP  •  Azure Table Storage", 10, C["muted"], True, align=PP_ALIGN.CENTER)

    # 6 Architecture
    s = _slide(prs, "Solution architecture", "Verified components in the current codebase; logical view, not a deployment diagram")
    layers = [(1.9, "React + Vite  |  queue, overview, claim detail, evidence, handler preparation action", C["pale_blue"], C["blue"]),
              (2.9, "FastAPI + Python  |  orchestration, REST endpoints, rules, persistence, background task", C["pale_teal"], C["teal"])]
    for y, label, fill, edge in layers:
        _rect(s, 0.82, y, 11.68, 0.72, fill, edge)
        _box(s, 1.0, y + 0.16, 11.3, 0.38, label, 13, C["ink"], True, align=PP_ALIGN.CENTER)
    services = [(0.86, "Content\nUnderstanding", C["blue"]), (3.25, "Azure OpenAI\nvision", C["teal"]), (5.64, "Python\nvalidation", C["green"]), (8.03, "Azure AI Search\nKB / MCP", C["amber"]), (10.42, "Azure Table\nStorage", C["ink"])]
    for x, label, edge in services:
        _rect(s, x, 4.12, 2.06, 0.9, C["white"], edge)
        _box(s, x + 0.1, 4.28, 1.86, 0.52, label, 10, edge, True, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        _line(s, x + 1.03, 4.08, x + 1.03, 3.66, edge, 1, True)
    _box(s, 0.96, 5.55, 11.3, 0.5, "Claim evidence is read from local repository folders; production identity, networking, and evidence ingestion are not represented.", 10, C["muted"], align=PP_ALIGN.CENTER)

    # 7 Implementation map
    s = _slide(prs, "Implementation map", "Separation of concerns across the repository")
    _table(s, 0.78, 1.9, [2.05, 4.0, 5.55], [
        ["Concern", "Implementation", "Responsibility"],
        ["Orchestration", "backend/pipeline.py", "Discovery, parallel calls, validation, result package"],
        ["Extraction", "backend/analyzers.py + content_understanding.py", "Document schemas and analyzer client"],
        ["Vision", "backend/vision.py", "Structured photo description and indicative repair band"],
        ["Rules", "backend/validation.py + config.py", "Evidence checks, findings, recommendation mapping"],
        ["Policy review", "backend/claims_agent.py", "MCP retrieval, structured summary, wording guardrails"],
        ["API + store", "backend/api.py + store.py", "FastAPI contract and Table Storage records"],
        ["User experience", "frontend/src/", "Queue, claim details, polling, handler panel"],
    ], 0.57, 9)

    # 8 Rules
    s = _slide(prs, "Policy and validation controls", "Deterministic findings give handlers a reason to verify or escalate")
    _table(s, 0.78, 1.88, [2.32, 4.25, 5.03], [
        ["Control", "Examples", "Training reference / action"],
        ["Completeness", "Required document missing", "CIP-CLM-200 §1 / request information"],
        ["Consistency", "Date, VIN, plate, damage location", "CIP-CLM-200 §2 / resolve or refer"],
        ["Coverage / authority", "Loss before cover; estimate over $5,000", "CIP-POL-100 §1.1; CIP-CLM-200 §3"],
        ["Estimate evidence", "Cost above photo band + tolerance", "CIP-CLM-220 §4 / line-item review"],
        ["Pattern / circumstance", "Repairer, frequency, unattended vehicle", "CIP-CLM-210 §§2–4 / indicator only"],
        ["Extraction quality", "Low-confidence value", "Handler verification; informational"],
    ], 0.61, 9)
    _box(s, 0.9, 6.32, 11.4, 0.3, "Fictional policy corpus. Rule mapping and loss-type normalization need broader coverage before production.", 9, C["muted"])

    # 9 Recommendation boundary
    s = _slide(prs, "Recommendation boundary", "Three workflow steps; no final claim outcome")
    cards = [(0.86, "PROCEED", "No higher-priority finding blocks routine preparation. Human review still applies.", C["green"], C["pale_teal"]),
             (4.88, "REQUEST INFORMATION", "Evidence is missing or a resolvable discrepancy needs follow-up.", C["amber"], C["pale_amber"]),
             (8.9, "REFER", "A policy, authority, damage, repairer, frequency, or circumstance indicator needs review.", C["red"], C["pale_red"])]
    for x, title, body, edge, fill in cards:
        _rect(s, x, 2.02, 3.56, 1.9, fill, edge)
        _box(s, x + 0.16, 2.23, 3.2, 0.32, title, 12, edge, True)
        _box(s, x + 0.16, 2.75, 3.2, 0.92, body, 11, C["ink"])
    _rect(s, 0.9, 4.42, 11.5, 0.76, C["ink"])
    _box(s, 1.1, 4.6, 11.1, 0.38, "Accept / amend / reject refers to the preparation package, not acceptance or rejection of the claim.", 12, C["white"], True, align=PP_ALIGN.CENTER)
    _box(s, 1.05, 5.56, 11.2, 0.46, "Rule and agent recommendations are evaluated separately; the handler remains accountable.", 10, C["muted"], align=PP_ALIGN.CENTER)

    # 10 Sample claims
    s = _slide(prs, "Five scenarios, one operating pattern", "Synthetic examples cover routine preparation and exceptions")
    _table(s, 0.8, 1.92, [1.2, 2.7, 6.2, 1.8], [
        ["Claim", "Scenario", "Primary signal", "Next step"],
        ["0431", "Complete", "Baseline evidence", "Proceed"],
        ["0432", "Missing evidence", "Required items absent", "Request info"],
        ["0433", "Inconsistency", "Date, VIN, damage area", "Refer"],
        ["0434", "Policy / authority", "Loss before cover; > $5,000", "Refer"],
        ["0435", "Risk indicators", "$6,940 vs light scuff; pattern signals", "Refer"],
    ], 0.65, 9)
    _box(s, 0.92, 6.2, 11.4, 0.34, "An indicator is a reason to look more closely, never a conclusion that fraud occurred.", 10, C["red"], True, align=PP_ALIGN.CENTER)

    # 11 UI
    s = _slide(prs, "Handler experience", "Queue context and case detail share one review surface")
    _rect(s, 0.8, 1.92, 4.15, 3.85, C["pale"], C["line"])
    _box(s, 1.04, 2.16, 3.6, 0.3, "QUEUE OVERVIEW", 10, C["teal"], True)
    for i, (label, value) in enumerate([("Queue KPIs", "processed + elapsed time"), ("Recommendation", "proceed / request / refer"), ("Finding groups", "common codes + missing files"), ("Estimate bands", "claim-linked cohorts")]):
        y = 2.72 + i * 0.65
        _box(s, 1.06, y, 1.7, 0.3, label, 10, C["ink"], True)
        _box(s, 2.78, y, 1.84, 0.35, value, 9, C["muted"])
        _line(s, 1.04, y + 0.45, 4.68, y + 0.45)
    _rect(s, 5.36, 1.92, 7.15, 3.85, C["white"], C["line"])
    _box(s, 5.67, 2.16, 6.5, 0.3, "CLAIM REVIEW", 10, C["teal"], True)
    _box(s, 5.67, 2.68, 6.3, 0.32, "Cross-claim pattern", 13, C["ink"], True)
    _box(s, 5.67, 3.12, 6.35, 0.58, "Apex Collision Center appears on three dated claim references in the supplied history. The dashboard links the pattern to its source claim.", 10, C["muted"])
    _line(s, 5.68, 3.92, 12.2, 3.92)
    _box(s, 5.68, 4.15, 3.0, 0.28, "NAMED HANDLER ACTION", 10, C["teal"], True)
    for i, label in enumerate(("Accept preparation", "Accept with amendments", "Reject preparation")):
        x = 5.7 + i * 2.18
        _rect(s, x, 4.69, 2.0, 0.48, C["pale_blue"], C["blue"])
        _box(s, x + 0.05, 4.82, 1.9, 0.2, label, 8, C["ink"], True, align=PP_ALIGN.CENTER)
    _box(s, 0.92, 6.08, 11.4, 0.32, "Schematic from source code; not a screenshot from an authenticated production environment.", 9, C["muted"], align=PP_ALIGN.CENTER)

    # 12 Evidence lineage
    s = _slide(prs, "Evidence and data lifecycle", "Document/field traceability exists; source-span retention is a known gap")
    lifecycle = [(0.92, "Source files", "Local claim\nfolders", C["blue"]), (3.25, "Analyzer", "Value + confidence\nsource returned", C["teal"]), (5.58, "Pipeline", "Value + confidence\nsource omitted", C["amber"]), (7.91, "Stored result", "Findings + review\nTable Storage", C["green"]), (10.24, "Handler UI", "Evidence list +\nclaim detail", C["ink"])]
    for i, (x, title, body, edge) in enumerate(lifecycle):
        _rect(s, x, 2.55, 1.95, 1.4, C["white"], edge)
        _box(s, x + 0.1, 2.76, 1.75, 0.3, title, 11, edge, True, align=PP_ALIGN.CENTER)
        _box(s, x + 0.12, 3.18, 1.71, 0.5, body, 9, C["muted"], align=PP_ALIGN.CENTER)
        if i < len(lifecycle) - 1:
            _line(s, x + 1.98, 3.24, lifecycle[i + 1][0] - 0.08, 3.24, C["muted"], 1.1, True)
    _rect(s, 1.12, 4.65, 11.05, 0.75, C["pale_amber"], C["amber"])
    _box(s, 1.3, 4.83, 10.7, 0.38, "Production improvement: preserve document hashes and page/coordinate spans end to end.", 12, C["ink"], True, align=PP_ALIGN.CENTER)

    # 13 Evaluation
    s = _slide(prs, "Evaluation results", "Reported baseline against five synthetic ground-truth claims")
    results = [(0.83, "45 / 45", "Extraction", "Mapped fields", C["blue"]), (3.29, "11 / 11", "Findings", "Zero spurious", C["green"]), (5.75, "5 / 5", "Recommendations", "Agent + rules", C["teal"]), (8.21, "0", "Safety violations", "Configured scan", C["amber"]), (10.67, "5 / 5", "Claims passed", "All conditions", C["ink"])]
    for x, value, label, note, edge in results:
        _rect(s, x, 2.05, 1.87, 2.1, C["white"], C["line"])
        _rect(s, x, 2.05, 1.87, 0.07, edge)
        _metric(s, x + 0.12, 2.34, 1.62, value, label, note, edge)
    _rect(s, 0.95, 4.72, 11.4, 0.82, C["pale_amber"], C["amber"])
    _box(s, 1.15, 4.9, 11.0, 0.4, "Prior submission metrics; `out/` JSON is not present in this checkout, so they could not be replayed.", 11, C["ink"], True, align=PP_ALIGN.CENTER)
    _box(s, 1.02, 5.86, 11.3, 0.42, "Regression evidence only: no production accuracy, fairness, or business-impact claim.", 10, C["muted"], align=PP_ALIGN.CENTER)

    # 14 Governance
    s = _slide(prs, "Responsible AI and governance", "Useful prototype controls; enterprise assurance is still required")
    _box(s, 0.9, 1.9, 5.2, 0.3, "IN THE PROTOTYPE", 10, C["green"], True)
    _bullets(s, 0.92, 2.32, 5.2, ["Structured response schema and recommendation enum", "Instructions prohibit claim outcome and fraud conclusions", "Rule findings identify document and field", "Named handler action with optional note", "Fictional training data and policy corpus"], 0.56, 11, C["green"])
    _line(s, 6.55, 1.9, 6.55, 5.4)
    _box(s, 6.95, 1.9, 5.2, 0.3, "BEFORE REAL DATA", 10, C["red"], True)
    _bullets(s, 6.98, 2.32, 5.2, ["End-user identity, roles, claim authorization", "Managed identity, least privilege, private networking", "Privacy, retention, encryption, audit design", "Prompt-injection, fairness, robustness evaluation", "Human escalation ownership and procedures"], 0.56, 11, C["red"])
    _line(s, 0.92, 5.38, 12.3, 5.38)
    _box(s, 0.95, 5.52, 2.3, 0.3, "DELIVERY GATES", 9, C["teal"], True)
    _box(s, 0.95, 5.9, 11.3, 0.52, "1  Evidence quality     →     2  Secure foundation     →     3  Reliable operations     →     4  Controlled shadow-mode pilot", 12, C["ink"], True, align=PP_ALIGN.CENTER)

    # 15 Enterprise readiness
    s = _slide(prs, "Prototype to enterprise service", "The gap is operational control, not another model call")
    _table(s, 0.82, 1.95, [2.0, 4.32, 5.34], [
        ["Capability", "Current lab pattern", "Enterprise target"],
        ["Identity", "Azure CLI; no user auth shown", "Entra ID, RBAC, managed identity"],
        ["Evidence", "Local repository folders", "Governed upload, scan, encryption, retention"],
        ["Processing", "In-process background task", "Durable queue, retry, idempotency, DLQ"],
        ["Audit", "Prepared record + handler note", "Versioned, immutable events and source lineage"],
        ["Operations", "Basic API; rough cost formula", "SLOs, telemetry, alerting, measured unit cost"],
    ], 0.68, 9)

    # 16 Roadmap (folded into governance slide in the executive deck)
    s = _slide(prs, "Delivery roadmap", "Four gated phases build quality, control, reliability, and evidence of value")
    phases = [(0.82, "01", "Evidence quality", "Source spans; broader tests; versioned rules/models; disagreement monitoring", C["blue"]),
              (3.9, "02", "Secure foundation", "Identity; authorization; evidence storage; privacy and threat review", C["teal"]),
              (6.98, "03", "Reliable operations", "Durable jobs; observability; SLOs; recovery; integrations", C["green"]),
              (10.06, "04", "Controlled pilot", "Shadow mode; expert comparison; fairness; measured value", C["amber"])]
    for x, number, title, detail, edge in phases:
        _rect(s, x, 2.2, 2.45, 2.72, C["white"], C["line"])
        _rect(s, x, 2.2, 2.45, 0.08, edge)
        _box(s, x + 0.16, 2.49, 0.55, 0.3, number, 11, edge, True)
        _box(s, x + 0.16, 2.95, 2.1, 0.55, title, 14, C["ink"], True, font="Aptos Display")
        _box(s, x + 0.16, 3.66, 2.1, 0.96, detail, 9, C["muted"])
    _box(s, 1.0, 5.55, 11.3, 0.5, "Gate each phase on evidence and accountable sign-off; do not introduce real data before controls are approved.", 11, C["ink"], True, align=PP_ALIGN.CENTER)

    # 17 Close
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid(); s.background.fill.fore_color.rgb = C["ink"]
    _rect(s, 0, 0, 0.16, SH, C["teal"])
    _box(s, 0.9, 0.86, 10.8, 0.3, "THE TAKEAWAY", 10, SlideColor(116, 207, 204), True)
    _box(s, 0.9, 1.52, 11.0, 1.0, "AI prepares the claim.\nPeople own the decision.", 30, C["white"], True, font="Aptos Display")
    _box(s, 0.94, 3.5, 10.8, 0.75, "The capstone demonstrates an evidence-led, policy-grounded review workflow and makes the production-readiness work explicit.", 16, SlideColor(216, 229, 236))
    _line(s, 0.94, 4.62, 8.9, 4.62, SlideColor(76, 110, 132))
    _box(s, 0.94, 4.95, 9.4, 0.45, "Questions  |  UC007 Claims Processing Agent", 14, C["white"], True)
    _box(s, 0.94, 5.5, 10.3, 0.52, "Contoso Insurance and all sample claims are fictional training materials.", 11, SlideColor(188, 207, 218))
    _footer(s, 17, True)

    # Keep the concise executive narrative: cover, summary, workflow/architecture,
    # controls, recommendation boundary, scenarios, dashboard, evaluation, governance, close.
    keep_indexes = {0, 1, 4, 7, 8, 9, 10, 12, 13, 16}
    slide_ids = prs.slides._sldIdLst
    for index in reversed(range(len(slide_ids))):
        if index not in keep_indexes:
            slide_id = slide_ids[index]
            prs.part.drop_rel(slide_id.rId)
            slide_ids.remove(slide_id)
    for slide_number, slide in enumerate(prs.slides, start=1):
        for shape in slide.shapes:
            if shape.has_text_frame and shape.left >= _in(11.8):
                value = shape.text_frame.text.strip()
                if value.isdigit() and len(value) == 2:
                    shape.text_frame.paragraphs[0].runs[0].text = f"{slide_number:02d}"

    prs.core_properties.title = "UC007 AI-Assisted Motor Claims Review"
    prs.core_properties.subject = "Enterprise capstone presentation - 10 slides"
    prs.core_properties.author = "Manoj Deepak (FDE user 42) <bolleddu.deepak@wipro.com>"
    prs.save(PRESENTATION)
    print(f"Created: {PRESENTATION} ({len(prs.slides)} slides)")


def main():
    build_docx()
    build_pptx()
    print("Both enterprise submission artifacts are ready.")


if __name__ == "__main__":
    main()
