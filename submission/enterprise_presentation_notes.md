# Presenter Notes — UC007 Claims Processing Agent

**Run time:** 8–10 minutes plus questions
**Audience:** Capstone assessors, insurance operations stakeholders, and technical reviewers
**Positioning:** An enterprise-oriented prototype; do not present it as production-ready or as a claim adjudication system.

## Slide 1 — AI-Assisted Motor Claims Review

Open with the operating boundary: the system prepares evidence and recommends a next step; authorised people make claim decisions. The Contoso claims and policy corpus are fictional.

## Slide 2 — Executive Snapshot

State the problem and outcome: mixed claim evidence makes manual comparison time-consuming, so the prototype structures the evidence and surfaces inconsistencies. The reported results are 45/45 extraction matches, 11/11 findings, 5/5 recommendation matches, and zero configured safety-phrase violations. Be explicit that raw evaluator output is absent from this checkout, so these reported figures could not be replayed here; five synthetic claims are not a production accuracy study.

## Slide 3 — End-to-End Preparation Flow

Walk from discovery through extraction, photo assessment, deterministic validation, policy-grounded explanation, and named handler review. Mention the underlying technologies: React/Vite, FastAPI/Python, Content Understanding, Azure OpenAI vision, Azure AI Search via MCP, and Azure Table Storage. Evidence is read from local folders in this prototype, so this is a logical view rather than production deployment architecture.

## Slide 4 — Policy and Validation Controls

Give a few examples: missing evidence; conflicting VIN/date; loss outside the policy period; estimate over the $5,000 handler authority; and photo/estimate inconsistency. The references are fictional training policies. Findings are signals for a handler, not coverage decisions or allegations.

## Slide 5 — Recommendation Boundary

Define `proceed`, `request_information`, and `refer` as workflow recommendations. The handler panel accepts, amends, or rejects the preparation package, not the insurance claim. The rule and agent recommendations are checked separately.

## Slide 6 — Five Scenarios

Use the table as a compact test matrix: a clean case, missing documents, conflicting evidence, an out-of-period loss with authority exceedance, and the multiple-indicator scenario. For CLM-2026-0435, describe the observation and referral recommendation; do not call the claim fraudulent.

## Slide 7 — Handler Experience

Point out that the manager overview now groups finding codes, missing documents, estimate bands, recommendation cohorts, preparation time, and verification work. Claim links let a manager inspect the cohort behind a metric. The Apex Collision Center item is a repeated-repairer observation based on three historical references, not an accusation. This slide is a schematic, not a captured production screenshot.

## Slide 8 — Evaluation Results

Explain what the evaluator checks and read the figures with their limits. It compares five synthetic outputs with a small ground truth and scans a limited list of forbidden phrases. Do not imply general accuracy, fairness, or measured business savings.

## Slide 9 — Responsible AI and Delivery Gates

Name current controls: structured output, constrained recommendation values, evidence-based rules, cautious fraud language, and a named handler review. Then explain the missing production controls: identity/access, secure evidence handling, privacy/retention, robust evaluation, and accountable operations. The four gates are evidence quality, secure foundation, reliable operations, and a controlled shadow-mode pilot. Do not use real claims data before the required approvals and protections.

## Slide 10 — Closing

Close with the central message: AI prepares and explains; people own consequential decisions. Invite questions about rule governance, evidence lineage, evaluation, or production readiness.

## Suggested Demo Sequence

1. Start on the claims overview and identify the five synthetic scenarios.
2. Open CLM-2026-0431 briefly to establish the normal path.
3. Open CLM-2026-0435 and show evidence, findings, recommendation, and verification items.
4. Explain the difference between the recommendation and the handler's preparation action.
5. Close with evaluation limits and the delivery gates; avoid real personal data.

## Q&A Anchors

- **Does the AI decide claims?** No. It prepares information and recommends proceed, request information, or refer.
- **Is fraud determined?** No. The rules surface indicators for human/specialist review and the agent is instructed not to allege fraud.
- **Are the results production-validated?** No. They are reported results on five synthetic cases; representative data and independent review are needed.
- **Is the app enterprise-ready?** No. Identity, authorization, secure evidence ingestion, durable orchestration, and operational controls remain roadmap work.
- **Can the result be audited?** Findings identify document/field and policy references, but end-to-end page/coordinate provenance is not retained in the current package.
