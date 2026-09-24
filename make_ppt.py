from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

NAVY = RGBColor(12, 34, 69)
BLUE = RGBColor(0, 102, 204)
TEAL = RGBColor(0, 153, 153)
GREY = RGBColor(88, 96, 105)
LIGHT = RGBColor(245, 247, 250)
WHITE = RGBColor(255, 255, 255)
ACCENT = RGBColor(0, 153, 102)


def add_title(slide, title, subtitle=None):
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.35), Inches(12.0), Inches(0.7))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = NAVY
    if subtitle:
        sub = slide.shapes.add_textbox(Inches(0.55), Inches(1.0), Inches(11.5), Inches(0.5))
        st = sub.text_frame
        p2 = st.paragraphs[0]
        p2.text = subtitle
        p2.font.size = Pt(13)
        p2.font.color.rgb = GREY


# Slide 1
slide = prs.slides.add_slide(prs.slide_layouts[6])
slide.background.fill.solid()
slide.background.fill.fore_color.rgb = WHITE
header = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.333), Inches(0.55))
header.fill.solid()
header.fill.fore_color.rgb = NAVY
header.line.fill.background()

box = slide.shapes.add_textbox(Inches(0.7), Inches(1.0), Inches(11.8), Inches(1.0))
tf = box.text_frame
p = tf.paragraphs[0]
p.text = 'UC007 · Claims Processing Agent'
p.font.size = Pt(28)
p.font.bold = True
p.font.color.rgb = NAVY

box2 = slide.shapes.add_textbox(Inches(0.7), Inches(2.0), Inches(11.0), Inches(0.7))
tf2 = box2.text_frame
p2 = tf2.paragraphs[0]
p2.text = 'Capstone presentation | End-to-end evidence, policy checks, and human review'
p2.font.size = Pt(18)
p2.font.color.rgb = GREY

stats = [('5 / 5', 'Claims fully passed'), ('45 / 45', 'Extraction accuracy'), ('0', 'Safety violations'), ('7', 'Key decision stages')]
for i, (v, label) in enumerate(stats):
    x = Inches(0.9 + i * 3.1)
    s = slide.shapes.add_shape(1, x, Inches(3.2), Inches(2.4), Inches(1.3))
    s.fill.solid()
    s.fill.fore_color.rgb = LIGHT
    s.line.color.rgb = BLUE
    tf = s.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = v
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p.alignment = PP_ALIGN.CENTER
    p2 = tf.add_paragraph()
    p2.text = label
    p2.font.size = Pt(11)
    p2.font.color.rgb = GREY
    p2.alignment = PP_ALIGN.CENTER

footer = slide.shapes.add_textbox(Inches(0.8), Inches(6.8), Inches(10.5), Inches(0.4))
ft = footer.text_frame
p3 = ft.paragraphs[0]
p3.text = 'Built for Contoso Insurance motor claims: evidence -> extraction -> rules -> grounded summary -> human decision'
p3.font.size = Pt(11)
p3.font.color.rgb = GREY

# Slide 2
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_title(slide, 'Business problem', 'Claims handlers need audit-ready evidence, not a black-box verdict.')
body = slide.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.6), Inches(3.8))
text = body.text_frame
for i, line in enumerate([
    '• Mixed evidence: claim forms, police reports, repair estimates, customer statements, policy schedules, and photos',
    '• Claims must be checked against policy rules and not decided by guesswork',
    '• A handler needs traceable evidence and a safe recommendation boundary',
    '• Fraud and policy exceptions must be surfaced early without inventing conclusions',
    '• The business goal is faster, more consistent, auditable triage'
]):
    p = text.paragraphs[0] if i == 0 else text.add_paragraph()
    p.text = line
    p.font.size = Pt(18)
    p.font.color.rgb = NAVY

box = slide.shapes.add_shape(1, Inches(7.1), Inches(1.6), Inches(4.8), Inches(2.8))
box.fill.solid()
box.fill.fore_color.rgb = LIGHT
box.line.color.rgb = BLUE
box_tf = box.text_frame
box_tf.word_wrap = True
sample = ['Outcome delivered', '• Human-safe workflow', '• Auditable source links', '• Policy-grounded explanations', '• Recommendations: proceed / request_information / refer', '• No unsafe approve/decline/payment decisions']
for j, s in enumerate(sample):
    p = box_tf.paragraphs[0] if j == 0 else box_tf.add_paragraph()
    p.text = s
    p.font.size = Pt(20 if j == 0 else 15)
    p.font.bold = (j == 0)
    p.font.color.rgb = NAVY if j == 0 else GREY

# Slide 3
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_title(slide, 'Solution architecture', 'Evidence in -> structured findings out')
boxes = [('1. Intake', 'Claim PDFs + photos', BLUE), ('2. Extraction', 'Content Understanding analyzers', TEAL), ('3. Photo analysis', 'Visible damage + repair band', ACCENT), ('4. Rules engine', 'Dates, mismatches, cover, authority, policy checks', NAVY), ('5. Grounded agent', 'Policy KB + summary + recommendation', BLUE), ('6. Human handler', 'Accept / amend / reject with note', GREY)]
for i, (t, desc, col) in enumerate(boxes):
    x = Inches(0.6 + i * 2.1)
    s = slide.shapes.add_shape(1, x, Inches(2.0), Inches(1.9), Inches(1.8))
    s.fill.solid(); s.fill.fore_color.rgb = LIGHT; s.line.color.rgb = col
    tf = s.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = t
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = NAVY
    p2 = tf.add_paragraph(); p2.text = desc; p2.font.size = Pt(12); p2.font.color.rgb = GREY
for i in range(len(boxes) - 1):
    x1 = Inches(2.5 + i * 2.1)
    x2 = Inches(2.9 + i * 2.1)
    line = slide.shapes.add_connector(1, x1, Inches(3.8), x2, Inches(3.8))
    line.line.color.rgb = BLUE
    line.line.width = Pt(2)

# Slide 4
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_title(slide, 'What was implemented', 'The core project modules and their purpose')
left = slide.shapes.add_textbox(Inches(0.7), Inches(1.5), Inches(6.0), Inches(4.5))
lt = left.text_frame
items = ['• backend/analyzers.py: claim form schema with structured extraction fields', '• backend/vision.py: conservative photo assessment instructions and repair-band mapping', '• backend/validation.py: date, damage-location, and estimate-vs-photo checks', '• backend/claims_agent.py: grounded agent instructions with safety boundary and recommendation precedence', '• backend/pipeline.py: orchestrates extraction, validation, photo assessment, and review', '• backend/api.py + store.py: service and decision tracking for the workspace']
for i, line in enumerate(items):
    p = lt.paragraphs[0] if i == 0 else lt.add_paragraph()
    p.text = line
    p.font.size = Pt(17)
    p.font.color.rgb = NAVY

right = slide.shapes.add_shape(1, Inches(7.1), Inches(1.7), Inches(4.8), Inches(2.4))
right.fill.solid(); right.fill.fore_color.rgb = LIGHT; right.line.color.rgb = TEAL
rt = right.text_frame
for i, s in enumerate(['Rules are deterministic', 'Policy references are explicit', 'Human review remains final']):
    p = rt.paragraphs[0] if i == 0 else rt.add_paragraph()
    p.text = s
    p.font.size = Pt(20 if i == 0 else 17)
    p.font.color.rgb = NAVY
    p.font.bold = (i == 0)

# Slide 5
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_title(slide, 'Policy and risk checks', 'The rules are deterministic and evidence-based')
left = slide.shapes.add_textbox(Inches(0.7), Inches(1.5), Inches(6.0), Inches(4.8))
lt = left.text_frame
rules = ['• DATE_MISMATCH: documents disagree on loss date (CIP-CLM-200 section 2.1)', '• VEHICLE_MISMATCH: VIN or plate differs across sources (section 2.2)', '• DAMAGE_LOCATION_MISMATCH: described damage conflicts with other evidence (section 2.3)', '• COVER_NOT_IN_FORCE: loss falls outside policy period (CIP-POL-100 section 1.1)', '• EXCEEDS_AUTHORITY: estimate exceeds handler authority limit (section 3)', '• ESTIMATE_EVIDENCE_MISMATCH: repair estimate exceeds visible photo damage band (CIP-CLM-220 section 4)']
for i, line in enumerate(rules):
    p = lt.paragraphs[0] if i == 0 else lt.add_paragraph()
    p.text = line
    p.font.size = Pt(17)
    p.font.color.rgb = NAVY

right = slide.shapes.add_shape(1, Inches(7.2), Inches(1.7), Inches(4.7), Inches(2.6))
right.fill.solid(); right.fill.fore_color.rgb = LIGHT; right.line.color.rgb = ACCENT
rtext = right.text_frame
for i, s in enumerate(['Safety rule', 'Never approve / decline / pay', 'Always recommend proceed / request_information / refer']):
    p = rtext.paragraphs[0] if i == 0 else rtext.add_paragraph()
    p.text = s
    p.font.size = Pt(20 if i == 0 else 16)
    p.font.bold = (i == 0)
    p.font.color.rgb = NAVY

# Slide 6
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_title(slide, 'Evaluation results', 'Verified against the ground truth in the lab environment')
metrics = [('45 / 45', 'Extraction accuracy', '100%'), ('10 / 10', 'Findings detected', '0 spurious'), ('5 / 5', 'Recommendation match', '100%'), ('0', 'Safety violations', 'No forbidden approval/decline/payment wording'), ('5 / 5', 'Claims fully passed', 'All use cases complete')]
for i, (v, label, note) in enumerate(metrics):
    x = Inches(0.7 + (i % 3) * 4.0)
    y = Inches(1.9 + (i // 3) * 2.2)
    s = slide.shapes.add_shape(1, x, y, Inches(3.3), Inches(1.7))
    s.fill.solid(); s.fill.fore_color.rgb = LIGHT; s.line.color.rgb = BLUE
    tf = s.text_frame
    p = tf.paragraphs[0]
    p.text = v
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p2 = tf.add_paragraph(); p2.text = label; p2.font.size = Pt(11); p2.font.color.rgb = GREY
    p3 = tf.add_paragraph(); p3.text = note; p3.font.size = Pt(10); p3.font.color.rgb = GREY

# Slide 7
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_title(slide, 'Demo and rollout notes', 'How to present the solution confidently')
body = slide.shapes.add_textbox(Inches(0.7), Inches(1.5), Inches(11.7), Inches(4.8))
text = body.text_frame
for i, line in enumerate([
    '1. Walk through one clean claim and one tricky claim to show the evidence trail.',
    '2. Highlight that every rule cites the source documents and policy sections.',
    '3. Show the photo evidence contradicting a high estimate to demonstrate fraud indicator handling without alleging fraud.',
    '4. Emphasize that the human handler remains the decision maker; the system only prepares, explains, and recommends.',
    '5. Discuss how this reduces manual review time while improving consistency, auditability, and policy compliance.',
    '6. Recommended next step: expand to production data, role-based access, and more policy corpora.'
]):
    p = text.paragraphs[0] if i == 0 else text.add_paragraph()
    p.text = line
    p.font.size = Pt(18)
    p.font.color.rgb = NAVY

# Slide 8
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_title(slide, 'Thank you', 'Contoso Insurance claims automation with audit-ready evidence and a human-safe decision boundary')
box = slide.shapes.add_textbox(Inches(1.3), Inches(2.2), Inches(10.4), Inches(2.2))
box_tf = box.text_frame
for i, line in enumerate(['Key message: evidence -> extraction -> rules -> grounded reasoning -> handler decision', 'Result: all five sample claims pass in the lab, with no safety violations and full policy alignment', 'Contact: Claims automation team | Microsoft FDE / Wipro AI Academy']):
    p = box_tf.paragraphs[0] if i == 0 else box_tf.add_paragraph()
    p.text = line
    p.font.size = Pt(20)
    p.font.color.rgb = NAVY
    p.alignment = PP_ALIGN.CENTER

output = r'C:\msfde-uc007-fs-lab\UC007_Claims_Processing_Capstone_Presentation.pptx'
prs.save(output)
print(output)
