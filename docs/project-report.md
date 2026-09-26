# Project Report: Contoso Claims Workspace

## 1. Executive Summary

This capstone project delivers a realistic AI-assisted motor claims review workflow for an insurance operations environment. The solution integrates a Python backend, a FastAPI service layer, and a React-based dashboard to ingest claim evidence, validate extracted facts, assess risk indicators, and support human decision-making in a transparent and auditable manner.

The business problem addressed is the operational burden of reviewing materially complex motor claims that may contain incomplete, inconsistent, or potentially suspicious evidence. The system supports this process by automatically structuring evidence, applying validation rules, comparing findings against policy documents, and generating a recommendation for a human handler.

The application follows a clear operational flow:

- evidence is collected from the claim folder and associated documents
- facts are extracted and structured for validation
- photographs and estimates are assessed for consistency
- policy and fraud indicators are checked
- the claim is assigned a recommendation for human review
- a handler makes the final decision using the system as decision support

This project demonstrates how responsible AI, operational controls, and a human-in-the-loop review model can be applied in a regulated insurance context.

## 2. Problem Statement and Objectives

### 2.1 Problem Statement

Insurance claim review involves multiple evidence sources, inconsistent documentation quality, and significant operational pressure. Manual handling of these claims is time-intensive and can lead to inconsistency, missed anomalies, and slower response times.

### 2.2 Objectives

The project aims to:

- automate the intake and structuring of claim evidence
- extract claim facts from mixed document sources
- validate extracted facts against policy and operational rules
- identify fraud and risk indicators using structured checks
- support claim handlers with explainable recommendations
- preserve accountability by keeping the human reviewer responsible for the final decision

## 3. Project Purpose and Business Context

The project addresses a common insurance operation challenge: reviewing motor claims that include multiple forms of evidence from different sources, such as:

- claim forms
- police reports
- repair estimates
- customer statements
- policy schedules
- photographs

The main goal is to reduce manual effort while improving consistency and decision traceability. Instead of simply returning a yes/no answer, the system attempts to show:

- what evidence was available
- what facts were extracted
- what validation checks failed or passed
- what the policy reasoning suggests
- how a human reviewer can make the final decision

This aligns with a controlled review model in which AI supports, but does not replace, human decision-making.

## 4. Functional Overview

The project enables a full claims workflow:

1. Claim evidence folders are stored under the data repository.
2. The backend API exposes claim and health endpoints.
3. The frontend lists available claims and shows claim details.
4. Claim processing can be triggered from the dashboard.
5. The backend runs claim-processing logic and stores results.
6. Human handlers can record a final decision.

The app is intentionally designed for educational and demonstration purposes and uses fictional claims, policies, and entities from a training environment.

## 5. System Architecture

The architecture follows a simple three-layer pattern:

### 4.1 Frontend Layer

Technology: React + Vite

Primary responsibilities:

- display the list of claims
- allow claim selection
- show claim detail information
- trigger processing requests
- allow handler decision recording

Relevant files:

- frontend/src/App.jsx
- frontend/src/components/ClaimList.jsx
- frontend/src/components/ClaimDetail.jsx
- frontend/src/styles.css

### 4.2 Backend Layer

Technology: Python + FastAPI

Primary responsibilities:

- expose REST API endpoints
- manage claim files and evidence lookup
- run processing jobs in the background
- store processed claim results
- support human decision updates

Relevant files:

- backend/api.py
- backend/pipeline.py
- backend/store.py
- backend/config.py
- backend/validation.py
- backend/analyzers.py
- backend/vision.py
- backend/claims_agent.py

### 4.3 Data and Reference Layer

The project relies on:

- data/claims/ for claim evidence folders
- reference/policies/ for policy documents
- data/ground-truth.json for evaluation expectations
- eval/evaluate.py for testing the pipeline output against expected results

## 6. Key Project Components

### 5.1 API Service

The backend exposes endpoints such as:

- GET /api/health
- GET /api/claims
- GET /api/claims/{claim_id}
- GET /api/claims/{claim_id}/evidence
- GET /api/claims/{claim_id}/file/{name}
- POST /api/claims/{claim_id}/process
- POST /api/claims/{claim_id}/decision

This API is the main integration layer between the frontend and the processing logic.

### 5.2 Processing Pipeline

The processing pipeline orchestrates the claim lifecycle. The project design suggests the following stages:

- evidence discovery
- extraction from documents and forms
- image analysis of photographs
- rule validation
- policy-grounded reasoning
- summary generation
- storing results for frontend review

#### 5.2.1 End-to-End Claim Processing Flow

The system follows a clear, step-by-step operational flow so every claim can be reviewed in a consistent and explainable way:

1. Evidence intake and claim folder discovery
   - The system scans the claim folder under data/claims and identifies the available files, such as claim forms, police reports, repair estimates, customer statements, policy schedules, and photographs.
   - This creates the evidence set that will be processed for the specific claim.

2. Document classification and source mapping
   - Each file is categorized by type (claim form, policy schedule, estimate, photograph, statement, or report).
   - This allows the downstream modules to apply the correct extraction and validation logic.

3. Structured fact extraction
   - The backend extracts key values such as claimant name, vehicle details, date of loss, VIN, plate number, repair estimate amount, and coverage information.
   - These facts are stored with source traceability so the reviewer can trace a result back to the original document.

4. Damage and visual assessment
   - Photograph analysis evaluates visible damage, estimate reasonableness, and risk indicators from the vehicle images.
   - This stage helps compare what the photographs show against the repair estimate and claim narrative.

5. Rule-based validation
   - Validation rules check for missing evidence, date mismatches, VIN mismatches, vehicle or damage-location inconsistencies, estimate anomalies, and policy coverage issues.
   - Each finding is assigned a severity and tied to a specific rule or evidence gap.

6. Policy-grounded claim reasoning
   - The claims agent compares findings against the policy corpus and business guidance.
   - It determines whether the claim should proceed, request more information, or be referred for escalation.

7. Summary generation and recommendation output
   - The system creates a concise summary that explains the claim, the extracted facts, the key findings, and the recommendation.
   - This summary is designed for a human reviewer and supports explainability.

8. Storage and UI presentation
   - Prepared claim results are saved to the claims store and surfaced in the React dashboard.
   - The reviewer can inspect the claim detail view, findings, evidence, and the final recommendation before making the human decision.

9. Human-in-the-loop decision
   - The workflow never auto-authorises, declines, or pays a claim.
   - The final responsibility remains with the handler, who records the decision in the operational workflow.

This pipeline ensures that AI assists the process while preserving governance, safety, and accountability.

### 5.3 Claim Decision Flow

The claims dashboard supports the human workflow:

- claims are listed in the workspace
- a claim is selected for review
- the system loads final processed information
- the reviewer may accept, amend, or reject the claim
- the final decision is stored back into the system

### 5.4 Policy and Validation Logic

The project includes reference policy documents and validation modules intended to detect issues such as:

- missing evidence
- contradictions between claim facts
- damage-location mismatches
- estimate-to-photo inconsistencies
- missing coverage or policy exceptions
- suspicious fraud indicators

This is especially relevant for the sample claims in the repository.

## 7. Sample Claims Included in the Project

The project includes five sample claims:

- CLM-2026-0431 — Complete and consistent claim
- CLM-2026-0432 — Missing evidence
- CLM-2026-0433 — Contradictions among key details
- CLM-2026-0434 — Policy exception or authority issue
- CLM-2026-0435 — Fraud-indicator case with an inflated estimate

These claim scenarios help validate that the system is not only extracting data, but also reasoning about policy and risk.

## 8. Business Value

This project provides practical value in three major ways:

### 7.1 Operational Efficiency

It reduces manual claim triage time by streaming evidence into a centralized dashboard and automating repetitive analysis.

### 7.2 Consistency and Traceability

The system is intended to ground findings in evidence and to show where rules or policy checks were triggered, improving explainability.

### 7.3 Decision Support

Rather than fully replacing human reviewers, the platform supports them with evidence-backed recommendations and structured decision capture.

## 9. Technical Notes

### 8.1 Key Startup Commands

The repository documents the following commands:

- Backend:
  - python config.py
  - python pipeline.py --setup
  - python pipeline.py --claim CLM-2026-0431
  - python pipeline.py --all
  - uvicorn api:app --port 8000

- Frontend:
  - cd frontend
  - npm run dev

- Evaluation:
  - cd eval
  - python evaluate.py

### 8.2 Environment Configuration

The backend expects configuration values such as Azure/OpenAI settings and environment variables, which are stored in a local .env file.

## 10. Extension Work Completed

The project was extended beyond the core lab workflow to cover operation-focused claim review features and harder fraud detection logic.

### 9.1 Verification Queue and Operational Overview

The workspace now includes:

- a high-level claim overview for prepared claims
- recommendation mix counts across proceed, request-information, and refer states
- a verification queue that highlights low-confidence critical values requiring handler confirmation
- a claim detail view that surfaces those verification items before final review

This aligns the tool with a real operations workflow where the system supports, but does not replace, human review.

### 9.2 Fraud Indicator Hardening

The validation layer was extended to include a subtle unattended-vehicle fraud indicator based on the policy guidance. This catches cases where the claim description indicates parked or unattended damage with no witness, no note, and no police reference, while keeping the system within its decision boundary of recommending referral rather than alleging fraud.

### 9.3 Safety and Compliance Controls

The agent output was also hardened to avoid unsafe language such as approving, declining, or paying a claim. The review remains constrained to the allowed recommendation states of proceed, request_information, or refer, and the system clearly communicates that the final claims decision remains with authorised human staff.

## 11. Verification Evidence

The project was validated with the built-in evaluation and a frontend build check.

### 10.1 Evaluation Result

Command executed:

- cd eval
- python evaluate.py

Result:

- extraction accuracy: 45/45 (100%)
- findings detected: 11/11
- recommendation match: 5/5
- safety violations: 0
- claims fully passed: 5/5

### 10.2 Frontend Build Result

Command executed:

- cd frontend
- npm run build

Result:

- Vite production build succeeded without errors.

## 12. Challenges and Risks

Some of the main challenges for this kind of solution include:

- inconsistent or incomplete evidence
- noisy document extraction results
- model hallucination when reasoning without proper constraints
- policy interpretation uncertainty
- high sensitivity of claims decisions

This is why the application emphasizes validation and human review instead of automated claim approval.

## 13. Suggested Screenshots to Add in the Project Document

To make the project report visually strong and easy to understand, the following screenshots should be included:

### 12.1 Dashboard / Claim List Screen

Purpose: show the overall claims workspace.

What to capture:

- claim list with multiple claims
- claim status indicators
- selection view
- overall dashboard layout

Why it matters:

This gives the reader a high-level view of the application and shows the central monitoring capability.

### 12.2 Health / API Status Screen

Purpose: confirm the backend is running and the app is connected.

What to capture:

- backend health response
- alias and prepared-claim counts
- API status indicator

Why it matters:

This validates system readiness and helps show the app is online and connected.

### 12.3 Claim Detail Page

Purpose: show the deep review view for a selected claim.

What to capture:

- claim summary
- processed findings
- evidence-related metadata
- recommendation or decision summary

Why it matters:

This is the core business functionality and should be central to the project documentation.

### 12.4 Evidence / File Listing View

Purpose: show what documents and files are attached to a claim.

What to capture:

- claim evidence folder listing
- multiple file types
- file names and metadata

Why it matters:

This demonstrates how raw evidence is organized and accessed.

### 12.5 Processing Status Screen

Purpose: show a claim currently being processed.

What to capture:

- status change from not processed to processing
- loading indicator or polling behavior

Why it matters:

It visually shows the asynchronous workflow and end-to-end background execution.

### 12.6 Decision Panel / Handler Decision Screen

Purpose: show the final human review action.

What to capture:

- Accept / Amend / Reject options
- handler name field
- note/comment box

Why it matters:

This demonstrates a human-in-the-loop final decision model and is a central business feature.

### 12.7 Claims Comparison Example

Purpose: depict different claim outcomes across multiple claims.

What to capture:

- a few sample claim records side by side
- one valid claim, one inconsistent claim, one fraud-risk claim

Why it matters:

This highlights the model’s ability to distinguish claim quality and fraud risk scenarios.

### 12.8 Evaluation / Validation Result Output

Purpose: show the model evaluation results.

What to capture:

- scoreboard or comparison summary
- claim-by-claim evaluation output

Why it matters:

This adds measurable proof of project quality and demonstrates benchmarking.

## 14. Recommended Screenshot Order for the Report

To build a professional report, the screenshots should appear in this order:

1. Project landing/dashboard view
2. API health status
3. Claim list overview
4. Claim detail with processed findings
5. Evidence and file panel
6. Processing state demonstration
7. Human decision panel
8. Evaluation results summary

This sequence tells a clear story from setup to decision-making to validation.

## 15. Final Conclusion

This project is a strong example of an AI-assisted insurance claims workflow that combines evidence ingestion, validation logic, policy reasoning, and a user-friendly review interface. It demonstrates both technical integration and business relevance, especially in highly regulated and decision-sensitive domains.

The project’s value lies not only in automation, but in explainability, traceability, and human oversight. That makes it an excellent demonstration of responsible AI usage in insurance operations.

## 16. Optional Add-on Section for Presentation Use

If this report is being used for a class presentation or academic submission, the following slide titles would work well:

- Overview of the Claims Processing System
- Architecture and Workflow
- AI and Policy Validation in Insurance
- Frontend Dashboard and User Experience
- Sample Claims and Risk Scenarios
- Final Decision Support Model
- Evaluation and Business Impact

## 17. Suggested Short Summary for Final Submission

The Contoso Claims Workspace is an AI-driven insurance claims review application that helps process motor-claim evidence, validate extracted facts against policy rules, and support human decision-making through an interactive dashboard. Built using Python and FastAPI for the backend and React for the frontend, the project combines evidence management, policy-aware reasoning, and a decision workflow that models realistic insurance operations.
