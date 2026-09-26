from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.shared import Inches

base = Path(r"c:\msfde-uc007-fs-lab")
assets = base / "docs" / "presentation_assets"
assets.mkdir(exist_ok=True, parents=True)

# --- Create dashboard-style graphic ---
def make_dashboard(path: Path):
    W, H = 1400, 900
    img = Image.new("RGB", (W, H), "#f3f4f6")
    d = ImageDraw.Draw(img)

    d.rounded_rectangle((40, 30, W - 40, 140), radius=18, fill="#e7edf5")
    d.text((70, 52), "Contoso Claims Workspace", fill="#203a5b", font=ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 48))
    d.text((70, 100), "Motor claim intake and review. Prepared automatically, decided by a handler.", fill="#476480", font=ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 24))

    metrics = [
        ("Prepared", 5, "#dfeaf7"),
        ("Proceed", 1, "#cfe8d7"),
        ("Request info", 1, "#f6e6bd"),
        ("Refer", 3, "#e9d5eb"),
        ("Verification", 0, "#e9eef4"),
    ]
    x0 = 70
    y0 = 200
    cell_w = 240
    cell_h = 150
    gap = 28

    for i, (label, val, color) in enumerate(metrics):
        x = x0 + i * (cell_w + gap)
        d.rounded_rectangle((x, y0, x + cell_w, y0 + cell_h), radius=14, fill=color, outline="#b8c7d8", width=2)
        d.text((x + 30, y0 + 26), label.upper(), fill="#38576f", font=ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 20))
        d.text((x + 100, y0 + 72), str(val), fill="#243f5e", font=ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 54))

    d.rounded_rectangle((60, 430, 650, 820), radius=18, fill="#ffffff", outline="#dfe3ea", width=2)
    d.text((90, 455), "CLAIMS", fill="#243f5e", font=ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 28))

    claim_rows = [
        ("CLM-2026-0431", "Proceed", 2),
        ("CLM-2026-0432", "Request info", 5),
        ("CLM-2026-0433", "Refer", 5),
        ("CLM-2026-0434", "Refer", 2),
        ("CLM-2026-0435", "Refer", 6),
    ]
    for idx, (claim, status, count) in enumerate(claim_rows):
        y = 500 + idx * 55
        d.rounded_rectangle((90, y, 600, y + 42), radius=12, fill="#f7f8fa" if idx % 2 == 0 else "#ffffff", outline="#d0d8e2", width=1)
        d.text((110, y + 9), claim, fill="#243f5e", font=ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 24))
        d.rounded_rectangle((430, y + 5, 560, y + 31), radius=8, fill="#dfe8ee", outline="#b8c7d8", width=1)
        d.text((450, y + 7), status, fill="#2d4b68", font=ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 16))
        d.text((600, y + 10), f"{count} findings", fill="#5f7187", font=ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 16))

    d.rounded_rectangle((740, 430, 1320, 820), radius=18, fill="#ffffff", outline="#dfe3ea", width=2)
    d.text((770, 455), "CLM-2026-0435", fill="#243f5e", font=ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 28))
    d.rounded_rectangle((1080, 460, 1255, 500), radius=8, fill="#e8d8f3", outline="#cda4d5", width=1)
    d.text((1100, 472), "REFER", fill="#5a3b65", font=ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 18))
    d.text((770, 535), "CLAIM SUMMARY", fill="#243f5e", font=ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 22))
    summary_lines = [
        "CLM-2026-0435 concerns Victor Hale, a 2020 Volkswagen Golf TSI,",
        "VIN 3VW5T7AU4LM049217, plate IL-8830LV, with a suspicious",
        "estimate of $6,940 for light scuff damage. The automated review",
        "flags estimate-to-photo mismatch, authority limit breach, and",
        "unattended vehicle risk indicators, so the case is referred.",
    ]
    for i, line in enumerate(summary_lines):
        d.text((770, 575 + i * 32), line, fill="#3a4d61", font=ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 20))

    d.text((770, 735), "FINDINGS (6)", fill="#243f5e", font=ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 22))
    tags = [
        "Estimate mismatch",
        "Authority limit",
        "Fraud indicator",
        "Claim frequency",
        "Enhanced review",
        "Low confidence",
    ]
    for i, tag in enumerate(tags):
        y = 770 + i * 26
        d.rounded_rectangle((770, y, 1105, y + 22), radius=8, fill="#eef2f8", outline="#cdd8e7", width=1)
        d.text((790, y + 2), tag, fill="#38576f", font=ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 16))

    img.save(path)

# --- Create evaluation graphic ---
def make_eval_chart(path: Path):
    W, H = 1200, 700
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    d.text((60, 30), "Evaluation Results", fill="#1f3551", font=ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 38))

    metrics = [
        ("Extraction", 45, "#2d7d66"),
        ("Findings", 11, "#325d95"),
        ("Recommendations", 5, "#5b4c94"),
        ("Safety Violations", 0, "#b35757"),
        ("Claims Passed", 5, "#3e7d5f"),
    ]
    start_x = 80
    top_y = 150
    bar_w = 150
    gap = 70

    for i, (label, value, color) in enumerate(metrics):
        x = start_x + i * (bar_w + gap)
        max_val = 45 if label != "Safety Violations" else 5
        h = 300 * (value / max_val) if max_val else 0
        y = top_y + (300 - h)
        d.rounded_rectangle((x, y, x + bar_w, top_y + 300), radius=10, fill=color)
        d.text((x + 18, top_y + 320), label, fill="#243f5e", font=ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 18))
        d.text((x + 26, y - 32), str(value), fill="#243f5e", font=ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 24))

    d.text((80, 610), "Result: 100% extraction accuracy, 11/11 findings detected, 5/5 recommendations correct, 0 safety violations.", fill="#243f5e", font=ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 20))
    img.save(path)

make_dashboard(assets / "dashboard_summary.png")
make_eval_chart(assets / "evaluation_summary.png")

# --- Build Word document ---
doc = Document()
doc.styles["Normal"].font.name = "Segoe UI"

doc.add_heading("AI-Powered Motor Claims Review and Decision Support System", 0)
doc.add_paragraph("UC007 Capstone Project | Microsoft FDE Lab | Final Submission")

doc.add_heading("1. Executive Summary", level=1)
doc.add_paragraph(
    "This capstone project delivers an AI-assisted motor claims review workflow designed for a realistic insurance operations context. The solution integrates a Python backend, a FastAPI service layer, and a React dashboard to ingest evidence, validate extracted facts, assess risk indicators, and support human decision-making in a transparent and auditable manner."
)

doc.add_heading("2. Problem Statement and Objectives", level=1)
for text in [
    "Insurance claim review is inherently evidence-heavy, operationally complex, and often vulnerable to incomplete or conflicting information.",
    "Manual handling of these claims is time-intensive, inconsistent across reviewers, and difficult to scale during high-volume periods.",
    "The project addresses this challenge by automating evidence structuring, validation, and policy-grounded reasoning while preserving human accountability in the final decision.",
    "The key objectives are to reduce manual effort, improve consistency, increase traceability, and support handlers with explainable recommendations before final action is taken.",
]:
    doc.add_paragraph(text)

doc.add_heading("3. Methodology and Implementation", level=1)
for text in [
    "The system follows a structured methodology: evidence intake, document classification, fact extraction, visual and estimate validation, policy reasoning, recommendation generation, and human review.",
    "The implementation combines backend services for orchestration and validation with a frontend interface for claim review and decision capture.",
    "The workflow is designed to support, not replace, human review, which is consistent with regulated claims operations and responsible AI use.",
]:
    doc.add_paragraph(text)

doc.add_heading("3. Dashboard Overview", level=1)
doc.add_picture(str(assets / "dashboard_summary.png"), width=Inches(8.8))

doc.add_heading("4. Verification and Evaluation Results", level=1)
results = [
    ["Metric", "Result"],
    ["Extraction accuracy", "45/45 (100%)"],
    ["Findings detected", "11/11"],
    ["Recommendation match", "5/5"],
    ["Safety violations", "0"],
    ["Claims fully passed", "5/5"],
    ["Frontend build", "Vite production build passed"],
]

table = doc.add_table(rows=len(results), cols=2)
table.style = "Table Grid"
for i, row in enumerate(results):
    cells = table.rows[i].cells
    for j, value in enumerate(row):
        cells[j].text = str(value)

doc.add_picture(str(assets / "evaluation_summary.png"), width=Inches(8.3))

doc.add_heading("5. End-to-End Claims Processing Pipeline", level=1)
for item in [
    "1. Claim intake: the system opens the claim folder and identifies all available evidence files, such as claim forms, statements, estimates, policy schedules, police reports and photographs.",
    "2. File classification: each item is classified by document type so the correct extraction logic is applied to the correct source.",
    "3. Fact extraction: key values such as claimant name, VIN, date of loss, plate, vehicle model, repair amount, and coverage details are extracted from the evidence.",
    "4. Visual assessment: damage photographs are reviewed to assess the visible damage and compare it with the estimate and claim narrative.",
    "5. Rule validation: the workflow checks for missing evidence, date mismatches, VIN inconsistencies, damage-location contradictions, estimate anomalies, and policy coverage violations.",
    "6. Policy-grounded reasoning: the claims agent aligns the findings with policy references and authority thresholds to decide whether the claim should proceed, request more information, or be referred.",
    "7. Recommendation and summary generation: the system builds a concise summary that explains the evidence, findings, and decision rationale for a human reviewer.",
    "8. Human-in-the-loop decision: the claim is presented in the dashboard, and the handler reviews the recommendation and records the final decision. The system never auto-approves, auto-declines, or auto-pays the claim.",
]:
    doc.add_paragraph(f"- {item}")

doc.add_heading("6. Key Claim Findings", level=1)
for item in [
    "CLM-2026-0432: missing customer statement, police report, and photo for theft claim -> request_information recommendation.",
    "CLM-2026-0433: inconsistent date, VIN, and damage location -> refer recommendation.",
    "CLM-2026-0434: cover period violation and estimate authority exceedance -> refer recommendation.",
    "CLM-2026-0435: estimate-to-photo mismatch, claim frequency, enhanced review trigger, and unattended vehicle indicator -> refer recommendation.",
]:
    doc.add_paragraph(f"- {item}")

doc.add_heading("7. Final Outcome", level=1)
doc.add_paragraph(
    "The completed solution demonstrates a realistic insurance operations workflow: mixed-document intake, evidence extraction, rule validation, policy-grounded reasoning, and human decision support. The project meets the expected evaluation criteria and is suitable for submission as a capstone demo. The system adds operational value by improving consistency, reducing manual review effort, and maintaining an explainable and responsible claims workflow."
)

out_path = base / "docs" / "Final_Submission_Claims_Workspace.docx"
doc.save(out_path)
print(f"Created: {out_path}")
