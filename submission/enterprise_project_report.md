# UC007 Claims Processing Agent

## AI-Assisted Motor Claims Review and Decision Support

**Capstone project report**
Microsoft FDE / Wipro AI Academy
**Prepared by:** Manoj Deepak | FDE user 42 | bolleddu.deepak@wipro.com
**Document status:** Detailed project submission
**Environment:** Fictional training and demonstration data only

> **Important boundary.** Contoso Insurance, its people, policies, claim records, repairers, and police references are fictional. This prototype is not a production claims platform, does not provide legal or coverage advice, and must not be used to make real claims decisions.

## 1. Executive Summary

The UC007 Claims Processing Agent is an AI-assisted motor claims workspace that prepares evidence-heavy claims for review by an authorised human handler. It brings documents, photographs, deterministic validation findings, policy references, and a structured recommendation into one workflow.

The project addresses a practical operations problem: a claim may contain a form, policy schedule, repair estimate, customer statement, police report, claims history, and photographs. Facts can be absent or conflict across sources; repair costs may not align with visible damage; policy dates and authority limits matter. Manually locating and comparing this evidence is repetitive and makes consistent handoffs harder.

The application combines a React/Vite review interface with a Python/FastAPI service. Azure Content Understanding analyzers extract structured document fields; an Azure OpenAI vision path assesses visible damage; deterministic Python rules identify evidence gaps and inconsistencies; and a claims agent retrieves from the fictional policy corpus through an Azure AI Search knowledge base over MCP. Prepared results and named handler actions are stored in Azure Table Storage.

The system is advisory. It returns one of `proceed`, `request_information`, or `refer`; it does not approve, decline, or pay claims. A named handler reviews the preparation and records whether it is accepted, amended, or rejected. Coverage and final claim actions remain with authorised staff.

The submission records a prior evaluation result of **45/45 extraction matches, 11/11 expected findings, 5/5 recommendation matches, zero safety-language violations, and 5/5 claims passed**. The current checkout does not contain the evaluator's `out/` result files, so those figures are reported from the submission record rather than independently reproduced here. The sample is small and synthetic; it demonstrates the workflow, not production accuracy or business impact.

## 2. Business Context and Problem

### 2.1 Operational problem

Motor claim handlers must reconcile multiple evidence sources under service and authority constraints. Common sources include claim forms, policy schedules, repair estimates, customer statements, police reports, claims histories, and damage photographs. Each source may use different wording or carry a different version of a key fact.

Without a structured preparation workflow, the handler must find the documents, transcribe facts, compare identifiers and dates, verify coverage context, interpret repair evidence, and record the rationale for the next action. This creates avoidable search effort and increases the chance that a missing item or contradiction is overlooked.

### 2.2 Project objectives

- Consolidate a claim's available evidence into a single review workflow.
- Extract important facts into structured fields, retaining confidence information.
- Identify missing documents and material cross-document contradictions using repeatable rules.
- Compare visible photo evidence with repair-estimate bands as a triage signal, not a valuation.
- Ground policy explanations in the provided fictional reference corpus.
- Present a concise, auditable preparation and a safe next-step recommendation.
- Preserve named human review and an explicit boundary against automated claim outcomes.

### 2.3 Scope and non-goals

**In scope:** five fictional motor-claim scenarios; PDF evidence extraction; image assessment; deterministic validation; policy-grounded summaries; a local review dashboard; API endpoints for claim processing and handler preparation decisions; and a ground-truth evaluation harness.

**Not in scope:** production deployment, live policyholder communication, payment or settlement, final coverage adjudication, a production fraud decision, enterprise identity and role enforcement, a durable distributed job queue, a real SIU case-management integration, or measured savings on a representative claims portfolio.

## 3. Users and Operational Outcomes

### 3.1 Primary users

| User | Need | Workspace support |
|---|---|---|
| Claims handler | Quickly understand the evidence, gaps, and next step | Claim list, extracted facts, findings, recommendation, and preparation decision panel |
| Senior adjuster | Review policy or authority exceptions | Escalation indicators with evidence and policy references |
| Claims operations lead | See the shape of the prepared queue | Overview counts and recommendation mix for prepared claims |
| SIU reviewer | Receive a grounded indicator rather than an unsupported allegation | Evidence-based referral cues; no fraud conclusion |

### 3.2 Intended operational outcomes

The intended benefit is reduced evidence-search and comparison effort, more consistent triage, and a clearer handoff from automated preparation to accountable human review. These are design goals, not measured production outcomes. A live deployment would need a controlled pilot to measure handler time, rework, referral quality, customer outcomes, and fairness before claiming business impact.

## 4. Functional Workflow

The end-to-end flow is:

1. **Discover evidence.** The pipeline scans the selected claim folder and separates supported documents from damage photographs using filename-based classification.
2. **Extract document facts.** Document-specific Content Understanding analyzers extract claim, policy, repair, statement, and police-report fields. Values include confidence and a source object at the analyzer boundary.
3. **Assess photographs.** The vision path returns a structured description of visible damage, affected area, severity, and an indicative repair band. It is instructed not to infer cause or fault.
4. **Run deterministic checks.** Python rules check document completeness, date and vehicle consistency, damage location, cover period, handler authority, estimate/photo consistency, enhanced-review repairers, claim frequency, unattended-vehicle circumstances, and low-confidence fields.
5. **Prepare policy-grounded review.** A claims agent receives the extracted package and findings, retrieves relevant policy guidance through the configured knowledge base, and produces a structured summary, citations, outstanding items, next steps, and recommendation.
6. **Persist and present.** The API stores prepared results and exposes claim detail and evidence endpoints. The React workspace shows queue status and claim details; it polls while a claim is processing.
7. **Record human preparation review.** A named handler accepts, amends, or rejects the prepared package with an optional note. This is a decision on the preparation, not a claim settlement or coverage outcome.

### 4.1 Recommendation semantics

The deterministic recommendation values are intentionally limited to:

| Recommendation | Meaning in this prototype |
|---|---|
| `proceed` | No higher-priority rule finding blocks routine preparation; a human still reviews the claim |
| `request_information` | Required evidence or a resolvable date/vehicle discrepancy needs follow-up |
| `refer` | A policy, authority, damage, repairer, frequency, or circumstance indicator needs specialist or senior review |

The rule function gives missing-document findings precedence, then referral-trigger findings, then date/vehicle discrepancies, and otherwise returns `proceed`. The agent has its own recommendation instructions and is evaluated separately from the rule recommendation. Neither result is a final claims decision.

## 5. Solution Architecture

### 5.1 Logical view

```text
React + Vite workspace
  Claim list / overview / evidence / findings / recommendation / handler preparation action
                            │ REST API
                            ▼
Python + FastAPI service
  Claim orchestration ─ extraction ─ photo assessment ─ validation ─ grounded review
        │                     │              │             │              │
        ▼                     ▼              ▼             ▼              ▼
  Local claim files   Azure Content     Azure OpenAI   Python rules   Azure AI Search
                      Understanding      vision path                  knowledge base/MCP
                            │                                              │
                            └────────────── prepared result ──────────────┘
                                           │
                                           ▼
                                  Azure Table Storage
```

This is the prototype's logical architecture, not a production network or deployment diagram. Claim evidence is discovered from the repository's local `data/claims/` folders. Azure Table Storage holds prepared records and handler decisions; the code does not implement a production evidence-upload or blob-ingestion service.

### 5.2 Technology and component responsibilities

| Layer | Technology / module | Responsibility |
|---|---|---|
| User interface | React, Vite | Queue overview, claim selection, claim detail, processing status, and handler preparation action |
| API | FastAPI in `backend/api.py` | Health, claims, overview, evidence, file, processing, and decision endpoints |
| Orchestration | `backend/pipeline.py` | File discovery, parallel extraction/photo calls, validation, agent invocation, result packaging, and timing/cost estimate |
| Document extraction | Azure Content Understanding; `backend/analyzers.py`, `backend/content_understanding.py` | Document-specific schemas and asynchronous analyzer calls; flatten returned fields |
| Photo assessment | Azure OpenAI vision; `backend/vision.py` | Structured visual description and indicative repair band |
| Rule validation | `backend/validation.py`, `backend/config.py` | Repeatable evidence, policy, authority, and risk-indicator checks |
| Policy reasoning | `backend/claims_agent.py` | Structured policy-grounded summary and recommendation using an MCP connection to the knowledge base |
| Persistence | Azure Table Storage; `backend/store.py` | Prepared-claim records, findings, extracted fields, review payload, and handler preparation decision |
| Evaluation | `eval/evaluate.py`, `data/ground-truth.json` | Compare extraction, findings, recommendations, safety language, and pass status with synthetic expected outcomes |

### 5.3 API surface

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/health` | GET | Service status, participant alias, agent/table identifiers, and stored-record counts |
| `/api/claims` | GET | Evidence folders combined with stored processing status |
| `/api/claims/overview` | GET | Prepared-queue recommendation mix and verification counts |
| `/api/claims/{claim_id}` | GET | Full prepared claim detail |
| `/api/claims/{claim_id}/evidence` | GET | Evidence filenames, inferred type, and size |
| `/api/claims/{claim_id}/file/{name}` | GET | Stream an evidence file after path validation |
| `/api/claims/{claim_id}/process` | POST | Enqueue processing as a FastAPI background task |
| `/api/claims/{claim_id}/decision` | POST | Record named accept/amend/reject preparation outcome and note |

Processing uses an in-process FastAPI background task and an in-memory active-claim set. This is suitable for a lab workflow, but is not a durable job queue or a multi-instance coordination mechanism.

## 6. Evidence, Data, and Traceability

### 6.1 Evidence types

The sample set includes PDFs and photographs. The five analyzer schemas cover claim forms, police reports, repair estimates, customer statements, and policy schedules. Claims-history PDFs are parsed for claim references. Images are sent to a vision model after resizing. Other files are classified as unknown and do not receive a dedicated extraction schema.

### 6.2 Provenance and confidence

The extraction adapter flattens fields to value, confidence, and source. The pipeline's persisted claim package keeps the value and confidence but omits the source object. Findings identify the document and field used; the current UI/API does not expose a page-and-coordinate citation experience. The report therefore describes document/field-level traceability, not complete source-span auditability. End-to-end source-span retention is a production-readiness item.

Low-confidence critical values can enter a verification queue. The queue currently uses a fixed threshold and is bounded to eight items. Informational low-confidence findings do not independently change the rule recommendation.

### 6.3 Data classification

All bundled entities and claims are fictional, and image origin metadata is recorded in `data/photo-credits.json`. A real implementation would process sensitive personal, vehicle, policy, and potentially special-category data. It would require approved data handling, purpose limitation, retention schedules, access logging, encryption, residency review, and vendor/model governance before any real data is introduced.

## 7. Deterministic Validation and Policy Controls

The rule layer is designed to be repeatable: a finding includes a code, severity, message, and evidence references. Policy identifiers below refer only to the fictional training corpus.

| Rule | What it checks | Typical next step | Reference |
|---|---|---|---|
| `MISSING_DOCUMENT` | Required evidence by loss type | Request information | CIP-CLM-200 §1 |
| `DATE_MISMATCH` | Loss dates across claim form, police report, and statement | Request information unless a higher-priority referral applies | CIP-CLM-200 §2.1 |
| `VEHICLE_MISMATCH` | VIN/plate differences across supported documents | Request information unless a higher-priority referral applies | CIP-CLM-200 §2.2 |
| `DAMAGE_LOCATION_MISMATCH` | Damage area across form, estimate, statement, and available photo | Refer | CIP-CLM-200 §2.3; CIP-CLM-210 §2.1 |
| `COVER_NOT_IN_FORCE` | Loss date against schedule dates | Refer to authorised adjuster; system does not decide coverage | CIP-POL-100 §1.1; CIP-CLM-200 §3.2 |
| `EXCEEDS_AUTHORITY` | Estimate over the configured $5,000 handler threshold | Refer upward | CIP-CLM-200 §3 |
| `ESTIMATE_EVIDENCE_MISMATCH` | Estimate against the highest available photo repair-band ceiling, with 20% tolerance | Refer for line-by-line review | CIP-CLM-220 §4; CIP-CLM-210 §2.1 |
| `REPAIRER_ENHANCED_REVIEW` | Repairer on configured enhanced-review list | Refer for estimate review | CIP-CLM-220 §2; CIP-CLM-210 §2.3 |
| `CLAIM_FREQUENCY` | At least three parsed references in the supplied claims history | Refer for pattern review | CIP-CLM-210 §2.3 |
| `CIRCUMSTANCE_INDICATOR_UNATTENDED_VEHICLE` | Unattended vehicle plus no-note/no-witness language and no police reference | Refer as an indicator, not an allegation | CIP-CLM-210 §2.2 and §4 |
| `LOW_CONFIDENCE_FIELD` | Extracted field confidence below the configured rule threshold | Verify with handler; informational | CIP-CLM-200 §5.4 |

The configured required-document mapping is intentionally simpler than the full policy table; loss-type normalization and required-document coverage need broader testing before production use. Rule findings are triage cues and do not determine fraud, coverage, liability, or settlement.

## 8. Sample Claims and Demonstrated Scenarios

| Claim | Scenario | Main exercise | Expected recommendation |
|---|---|---|---|
| CLM-2026-0431 | Complete and consistent | Baseline evidence extraction and routine preparation | `proceed` |
| CLM-2026-0432 | Missing evidence | Required-document gap and consolidated follow-up | `request_information` |
| CLM-2026-0433 | Cross-document inconsistency | Date, VIN, and damage-location contradiction | `refer` |
| CLM-2026-0434 | Policy/authority exception | Loss date precedes cover start; estimate exceeds handler authority | `refer` |
| CLM-2026-0435 | Multiple risk indicators | $6,940 estimate for visually described light scuff; enhanced-review repairer; claim history and circumstance indicators | `refer` |

The examples are constructed scenarios, not a representative sample of real claim traffic. A risk indicator is an observation that warrants review; it is not evidence that a customer committed fraud.

## 9. Evaluation and Evidence

### 9.1 Evaluation design

`eval/evaluate.py` reads prepared JSON output from `out/` and compares it with `data/ground-truth.json`. It measures normalized field matches for the configured extraction field map; distinct non-informational finding codes per claim; agent and deterministic recommendation matches; forbidden phrases in the agent review; and a combined pass flag.

### 9.2 Reported result

| Measure | Reported result | Interpretation |
|---|---:|---|
| Extraction fields | 45/45 (100%) | Matched fields among those available in the five prepared sample results |
| Expected findings | 11/11, zero spurious | Distinct expected non-informational codes in the evaluator comparison |
| Agent recommendations | 5/5 | Exact match to synthetic expected recommendation for each sample |
| Rule recommendations | 5/5 | Exact match to synthetic expected recommendation for each sample |
| Safety phrase checks | 0 violations | No configured forbidden phrase in the serialized agent review |
| Claims fully passed | 5/5 | All evaluator conditions passed for all five results |

These figures are reported in the existing submission record. The current workspace has no `msfde-capstone/out/` directory, so the prior run cannot be independently replayed from its raw result JSON in this checkout. The evaluator is a useful regression check, not a statistical performance study: it uses five synthetic claims, a limited field map, exact expected labels, and a small forbidden-phrase list. It does not measure precision/recall on production claims, calibration, subgroup fairness, reviewer time, or customer outcomes.

### 9.3 Verification procedure

With Azure resources, credentials, and environment configuration available:

```powershell
cd backend
python pipeline.py --all
cd ..\eval
python evaluate.py --verbose
```

The frontend production build can be checked from `frontend/` with `npm run build`. Evaluation requires the full pipeline results in `out/`; it cannot be run against this checkout until those results are generated.

## 10. Dashboard and Evaluation Screenshots

Use the spaces below for screenshots captured from the running dashboard and the `eval/evaluate.py` output. Keep claim data fictional and remove any local aliases or endpoint details before sharing the report.

### 10.1 UI dashboard page

Paste a screenshot of the claims workspace overview here. Prefer a view that shows the queue metrics, recommendation mix, and cross-claim patterns.

[[SCREENSHOT: UI dashboard page | 2.5]]

*Figure 1. Claims operations dashboard. Insert the captured UI screenshot in the framed area above.*

### 10.2 Evaluation results

Paste a screenshot of the complete `python evaluate.py --verbose` output here after running the pipeline. Include the summary totals and claim-level pass results when available.

[[SCREENSHOT: eval/evaluate.py results | 2.5]]

*Figure 2. Evaluation output. Insert the captured evaluator screenshot in the framed area above.*

## 11. Responsible AI, Security, and Governance

### 10.1 Controls present in the prototype

- The agent uses a strict structured response schema and a constrained recommendation enum.
- Agent instructions prohibit final claim outcomes and unsupported fraud allegations.
- A post-response sanitizer rewrites configured forbidden phrases.
- Deterministic findings cite documents/fields and policy sections in their messages.
- Missing or low-confidence facts are to be stated as unknown, not inferred.
- The handler action requires a non-empty handler name and records an optional note.
- The API validates claim IDs and constrains file paths to the evidence folder.
- The data and policy corpus are fictional training materials.

These controls are helpful but not a complete safety or security case. Phrase replacement is not a substitute for semantic review, and the evaluator checks a limited list of exact phrases.

### 10.2 Current security posture and gaps

The sample uses Azure CLI credentials for service calls and has localhost-oriented CORS settings. The shown code does not implement end-user authentication, application authorization, role-based permissions, production secret management, per-claim access controls, or an immutable audit log. Evidence files are read from the local repository. No production SLA, threat model, penetration test, data-retention policy, or disaster-recovery objective is established by this capstone.

Before real data or users, establish Entra ID authentication and least-privilege authorization; managed identities and secretless service access; private network paths and approved service endpoints; encryption and retention controls; secure evidence ingestion; audit events; abuse and prompt-injection testing; model/policy versioning; and documented human escalation procedures.

## 12. Limitations and Risks

| Area | Prototype limitation | Operational implication |
|---|---|---|
| Classification | Document type is inferred from filename, not document content | Renamed or novel files may be missed or misclassified |
| Extraction | Evaluated only on five synthetic claims and selected fields | Reported match rate is not a general accuracy guarantee |
| Evidence lineage | Source objects are dropped before persistence; UI does not show page spans | Handlers may need to reopen documents to verify values |
| Vision | Photo-based repair bands are indicative and sensitive to image quality/framing | They must not be treated as estimates, valuations, or final evidence of damage extent |
| Rules | Thresholds and required-document mappings are code/config values with limited sample coverage | Policy changes require governed updates and regression tests |
| Agent | Retrieval and generated explanations can still be incomplete or wrong | Citations and every material statement require human verification |
| Processing | FastAPI background task and in-memory processing set are not durable/distributed | Process restart or horizontal scaling can lose coordination/state |
| Persistence | Table Storage access and query patterns are prototype-level | Production partitioning, concurrency, retention, and audit semantics need design |
| Security | End-user authentication/authorization is not shown | Not suitable for exposure to real users or sensitive claims data |
| Economics | Cost figure in the pipeline is a fixed estimate formula | It is not measured billing or a finance-grade unit cost |

## 13. Enterprise Readiness Roadmap

### Phase 1: Evidence and decision quality

- Preserve source spans and document version/hash from extraction through API and UI.
- Expand the ground truth with independently authored edge cases and ambiguous documents.
- Add tests for policy-date boundaries, loss-type normalization, missing fields, multi-photo disagreement, prompt injection, and recommendation precedence.
- Track extraction confidence, abstentions, rule hits, agent/rule disagreements, and human amendments.
- Version analyzer schemas, rules, prompts, policy indexes, and model deployments; make each prepared result reproducible.

### Phase 2: Secure application foundation

- Add Entra ID sign-in, role-based access, claim-level authorization, and audited handler identity.
- Replace local evidence-folder access with a governed upload and storage service, malware scanning, metadata validation, encryption, and retention controls.
- Use managed identity, least-privilege role assignments, private networking where required, and managed secret handling.
- Add API rate limits, request validation, content-size limits, secure headers, and a formal threat model.

### Phase 3: Reliable operations

- Move processing to a durable queue/worker model with idempotency, retries, timeouts, dead-letter handling, and cancellation.
- Add structured logs, distributed traces, service/model latency, per-claim cost, failure rates, and alerting without leaking personal data.
- Define SLOs, backup/restore, regional recovery, capacity, and operational runbooks.
- Integrate referrals and outstanding-information requests with authorised downstream systems while keeping policyholder communication controlled.

### Phase 4: Controlled pilot and governance

- Conduct privacy, legal, security, accessibility, and model-risk reviews.
- Run a shadow-mode pilot with representative, approved data before any workflow influence.
- Compare recommendations with expert review; test for disparate error rates and monitor drift.
- Require handler acknowledgement, sample audits, clear contest/escalation paths, and documented ownership for rules and models.
- Expand only after operational evidence demonstrates safety, quality, reliability, and measurable user benefit.

## 14. Local Demonstration Guide

The project is an Azure-connected lab, not an offline demo. A local run requires the project-specific Azure endpoints/resources, Azure CLI sign-in, a configured `backend/.env`, Python dependencies, and the frontend dependencies. Do not place real claim data or credentials in the repository.

Typical sequence from the project root:

```powershell
cd backend
python config.py
python pipeline.py --setup
uvicorn api:app --reload --port 8000
```

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

For an evaluation run, process all sample claims and then run the evaluator as described in Section 9.3. Use the environment handout and `docs/lab-guide.md` for resource-specific configuration; endpoint values are not included in this submission.

## 15. Repository Guide

| Path | Role |
|---|---|
| `backend/pipeline.py` | Orchestrates evidence processing and result packaging |
| `backend/analyzers.py` | Document schemas and filename classification |
| `backend/content_understanding.py` | Content Understanding REST client and field flattening |
| `backend/vision.py` | Structured photo assessment |
| `backend/validation.py` | Deterministic findings and recommendation mapping |
| `backend/claims_agent.py` | Policy-grounded structured review and output guardrails |
| `backend/api.py` | FastAPI endpoints and background processing |
| `backend/store.py` | Azure Table Storage prepared-claim and handler records |
| `frontend/src/` | React workspace and review components |
| `data/claims/` | Fictional claim evidence |
| `data/ground-truth.json` | Synthetic expected facts, findings, and recommendations |
| `reference/policies/` | Fictional policy and operations reference corpus |
| `eval/evaluate.py` | Ground-truth evaluation harness |
| `extensions/` | Optional capstone extension challenges |

## 16. Conclusion

The UC007 capstone demonstrates a credible pattern for AI-assisted claim preparation: combine document and image analysis with deterministic validation, policy-grounded explanation, and a named human review step. Its strongest contribution is the explicit boundary between preparing a claim and making a claim decision.

The prototype is not production-ready, and the five-claim evaluation is not evidence of general performance. Its value is as a working architecture and governance demonstration that makes the next engineering questions concrete: preserve end-to-end evidence provenance, secure access to sensitive records, make processing durable, evaluate on representative data, and measure real operational outcomes before deployment.
