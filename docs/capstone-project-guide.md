# Capstone Project Guide: AI-Powered Motor Claims Review

## 1. Project Summary

This capstone project is a realistic insurance operations demo built around a motor claims review workflow. It simulates how a modern claims team can use AI, structured extraction, validation rules, and business policy review to support faster and more consistent claim handling.

The project takes mixed evidence such as:
- claim forms
- police reports
- repair estimates
- customer statements
- policy schedules
- photographs

It then:
- extracts key claim facts
- checks them for inconsistencies or missing information
- compares the claim to policy requirements
- looks for fraud or suspicious patterns
- generates a recommendation for human review
- supports a handler decision workflow

This project is intentionally designed for training, business demo, and operational learning. All claims, policies, and entities are fictional and are used only for demonstration.

---

## 2. Business Problem and Use Case

Insurance companies receive large numbers of motor claims, and many contain incomplete, inconsistent, or ambiguous information. A claim may include multiple documents, different versions of the same fact, and photographs that need interpretation.

Without a structured workflow, a handler must manually inspect each file and compare it with policy rules. This is time-consuming, inconsistent, and difficult to scale.

### Primary use cases

1. Claim triage support
   - Review incoming evidence and identify missing information quickly.

2. Fraud and anomaly detection
   - Detect inflated repair estimates, mismatched vehicle details, suspicious loss timings, and unusual claim patterns.

3. Policy compliance review
   - Compare claim facts with policy conditions and coverage rules.

4. Explainable decision support
   - Show why a recommendation was made using evidence, rule checks, and policy reasoning.

5. Human-in-the-loop operations
   - Let a claim handler assess and finalize the decision instead of letting an AI system fully determine the outcome.

### Business value

- reduces manual review effort
- improves standardization across claim handlers
- makes the decision path traceable and explainable
- helps surface unusual or risky claims earlier
- supports faster escalation of claims that need payment or fraud review

---

## 3. Expected Outcomes of the Capstone

By the end of this project, the expected result is a working demo that demonstrates the following:

### Functional outcomes
- evidence is ingested and processed from the claim folder
- claim facts are extracted from documents and forms
- vehicle, date, estimate, and damage information are evaluated
- missing or contradictory evidence is highlighted
- policy-based recommendations are generated
- suspicious or irregular claims are flagged
- the system recommends either proceed, request information, or refer

### Safety and governance outcomes
- the system never auto-approves, auto-declines, or auto-pays a claim
- recommendations remain advisory and human-reviewed
- evidence-backed findings are shown to the user
- the decision path is grounded in policy and validation logic

### Demo outcomes
- a claim can be selected from the dashboard
- the dataset can be processed in a few steps
- findings and recommendations can be shown in a clear UI
- the reviewer can see risk signals and policy reasoning in one place

---

## 4. Architecture and Core Components

The capstone combines a backend and frontend to simulate a claims workflow.

### Backend
The backend is built in Python and includes:
- extraction logic for claim information
- image and damage assessment
- validation rules for inconsistent data and suspicious patterns
- policy-grounded reasoning for claim review
- FastAPI endpoints for claim processing and decision storage

Main files:
- backend/pipeline.py
- backend/validation.py
- backend/claims_agent.py
- backend/api.py
- backend/store.py

### Frontend
The frontend is built with React and Vite and displays:
- claim list
- claim detail view
- evidence summary
- findings and recommendations
- decision panel for human review

Main files:
- frontend/src/App.jsx
- frontend/src/components/ClaimList.jsx
- frontend/src/components/ClaimDetail.jsx
- frontend/src/components/DecisionPanel.jsx

### Data and reference layer
- data/claims/ contains sample claim evidence
- reference/policies/ contains policy documents
- data/ground-truth.json contains expected evaluation results
- eval/evaluate.py checks whether the pipeline performs correctly

---

## 5. What the Demo Shows

The demo is meant to illustrate a real insurer workflow where a claim is reviewed by an AI-assisted decision platform, not by a fully automated system.

The sample claims include:
- CLM-2026-0431: valid claim with consistent evidence
- CLM-2026-0432: missing evidence
- CLM-2026-0433: contradictory facts across documents
- CLM-2026-0434: policy exception or authority issue
- CLM-2026-0435: fraud-like pattern with suspicious estimate behavior

These scenarios demonstrate how the project handles normal, incomplete, contradictory, and high-risk claims.

---

## 5.1 Detailed End-to-End Pipeline Flow

The project uses a structured end-to-end claims workflow that is easy to understand and explain in a demo. The flow is:

1. Claim evidence collection
   - The system reads the claim folder and identifies all files for a specific case.
   - Evidence may include forms, statements, repair estimates, policy schedules, reports, and photographs.

2. Evidence classification
   - Each file is mapped to a document type so the correct extraction logic can be applied.
   - This ensures that the right fields are read from the right source document.

3. Fact extraction
   - Structured values are extracted from the claim evidence, including claim date, policy number, VIN, vehicle details, estimate total, and claimant identity.
   - These extracted facts are then compared across multiple sources.

4. Image and visual assessment
   - Damage photographs are reviewed to understand the visible condition and estimate reasonableness.
   - This helps identify whether the estimate matches the visible defect or appears unusually high.

5. Rule validation and anomaly detection
   - The validation layer checks for missing required documents, mismatched dates, VIN contradictions, damage-location inconsistencies, and estimate-to-photo mismatches.
   - It also checks policy coverage period and authority thresholds.

6. Policy-grounded review
   - The claims agent compares the findings against the policy reference documents and business rules.
   - It decides whether the claim is safe to proceed, needs more information, or should be referred.

7. Recommendation and summary generation
   - The system writes a summary that explains what happened, what evidence was used, what issues were identified, and why a recommendation was given.

8. Frontend presentation and human decision support
   - The claim is shown in the dashboard with findings and recommendations.
   - A human handler reviews the result and records the final operational decision.

9. Governance and safety guardrails
   - The system never finalises payment or claims approval automatically.
   - The workflow remains advisor-only and keeps the final responsibility with the reviewer.

This pipeline makes the system explainable, auditable, and suitable for a real insurance operations scenario.

---

## 6. Demo Flow: How to Present the Project

Use the following demo flow for a live presentation or oral explanation.

### Step 1: Introduce the business problem
Explain that the project addresses a real insurance problem: claims are evidence-heavy, complex, and often contain mismatches or missing information. Manual review is slow and inconsistent.

### Step 2: Show the claims dashboard
Open the web app and point out:
- claim list
- claim overview counts
- selected claim detail
- recommendation and findings panel

### Step 3: Select a claim
Pick a sample claim such as:
- CLM-2026-0435 for a higher-risk scenario

This is useful because it highlights:
- estimated repair cost concerns
- suspicious patterns
- validation findings
- a refer recommendation

### Step 4: Explain the evidence pipeline
Walk through how the system ingests the claim and reviews:
- documents
- photographs
- policy references
- validation logic

### Step 5: Show extracted facts and findings
Demonstrate the key output:
- claim date
- damage details
- estimate amount
- vehicle identifiers
- coverage or authority mismatch
- missing evidence indicators

### Step 6: Highlight the decision recommendation
Explain that the assistant does not auto-pay, auto-decline, or auto-reject the claim. Instead, it recommends a safe action such as:
- proceed
- request_information
- refer

This shows governance and safety in a claims workflow.

### Step 7: Show the human-in-the-loop decision
Show the decision panel and explain that a claim handler reviews the case and makes the final call. This is the operational model the project is designed to support.

### Step 8: Conclude the demo with business impact
Summarize the value:
- less manual review effort
- better claim consistency
- faster detection of exceptions and risk
- more explainable decision support

---

## 7. How to Start the Application

Follow these steps from the project root.

### 1. Open a terminal in the project folder
Use PowerShell in the workspace root:

```powershell
cd c:\msfde-uc007-fs-lab
```

### 2. Activate the Python environment
The workspace includes a virtual environment. Activate it with:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### 3. Start the backend API
From the project root or backend folder:

```powershell
cd backend
uvicorn api:app --port 8000
```

You should then have the API running locally on:
- http://localhost:8000

### 4. Start the frontend
Open a second terminal and run:

```powershell
cd frontend
npm install
npm run dev
```

The frontend runs by default on:
- http://localhost:5173

### 5. Open the app in a browser
Go to:
- http://localhost:5173

You can now review sample claims and trigger claim processing through the web UI.

---

## 8. Running the Full Workflow

### Option A: Run the full claim processing pipeline
From the backend folder:

```powershell
cd backend
python pipeline.py --all
```

This runs the claim-processing workflow end-to-end.

### Option B: Run a single claim
```powershell
cd backend
python pipeline.py --claim CLM-2026-0435
```

### Option C: Run setup for the environment
If you need to create analyzers or initialize configuration:

```powershell
cd backend
python config.py
python pipeline.py --setup
```

### Option D: Evaluate the system output
From the eval folder:

```powershell
cd eval
python evaluate.py
```

This checks whether the processed claims match the expected ground truth.

---

## 9. How to Verify the Output

Verification is critical because the project includes both application behavior and evaluation scoring.

### 9.1 Verify the backend is running
Open the API root or a health endpoint and check for a successful response.

Typical test:
```powershell
curl http://localhost:8000/api/health
```

Expected result:
- API responds successfully
- service is running without startup errors

### 9.2 Verify claim list and overview
Open the frontend and confirm that:
- claim cards appear
- claim count is visible
- each sample claim is listed
- the dashboard reflects processed claims or statuses

### 9.3 Verify a claim detail page
Select a claim and confirm that:
- evidence details are shown
- findings are displayed
- recommendation is visible
- human decision panel is available

### 9.4 Verify validation findings
For each sample claim, check that the output includes the expected risk or issue, such as:
- missing evidence
- date mismatch
- VIN mismatch
- damage location contradiction
- estimate-to-photo mismatch
- policy authority breach
- suspicious fraud indicator

### 9.5 Verify recommendation logic
The recommendation should match the scenario:
- complete claim -> proceed
- incomplete evidence -> request_information
- contradictions or policy issues -> refer

### 9.6 Run the official evaluation script
Execute:

```powershell
cd eval
python evaluate.py
```

This is the strongest validation step because it compares the output against expected ground-truth values.

### Example evaluation result
A successful run should show:
- extraction accuracy around 100%
- findings matched to expected values
- recommendation match close to or exactly 100%
- safety violations at 0
- claims fully passed at 5/5

This is the benchmark for a reliable project run.

---

## 10. Detailed Verification Checklist

Use this checklist during testing or a live demo.

### Backend verification
- [ ] Python environment is active
- [ ] backend API starts without errors
- [ ] claims API returns results
- [ ] processing endpoint works for a sample claim
- [ ] stored claim data includes recommendation and findings

### Frontend verification
- [ ] React app loads on localhost:5173
- [ ] claim list is visible
- [ ] selected claim details render properly
- [ ] validation findings are visible to the user
- [ ] decision panel can be used

### Logic verification
- [ ] missing evidence is identified
- [ ] contradictions are flagged
- [ ] estimate and photograph mismatch is detected
- [ ] recommendation is not auto-approval or auto-decline
- [ ] final decision remains with a human handler

### Evaluation verification
- [ ] all sample claims pass the evaluation script
- [ ] recommended options match expected output
- [ ] no safety violations are reported

---

## 11. Expected Demo Narrative

Here is a strong story you can say during presentation:

> This project demonstrates an AI-assisted claims review workflow for motor insurance. Instead of taking a single claim file and giving a final answer, the system ingests evidence from multiple sources, validates the facts, compares them to policy rules, and highlights risk indicators. It then supports a human reviewer with a clear recommendation and evidence trail, while keeping the final responsibility in the hands of the claim handler.
>
> In our demo, we show a realistic fraud-risk claim, explain the findings, and demonstrate how the system separates operational support from final decision-making.

---

## 12. Troubleshooting and Tips

### If the backend does not start
Check:
- the virtual environment is active
- required Python packages are installed
- the .env file exists and contains the expected values

### If the frontend does not load
Check:
- Node packages are installed
- npm install has completed
- the frontend dev server started successfully

### If evaluation fails
Review:
- extraction results
- findings count
- recommendation mapping
- safety rules

This often means the output is close but not aligned with the expected structured findings.

---

## 13. Final Outcome

This capstone project successfully demonstrates a practical AI use case in insurance operations:
- mixed-document claims review
- evidence extraction and validation
- automated rule-based risk checks
- policy-grounded recommendations
- human-in-the-loop decision support
- full-stack operational demo

The major goal is not to replace human claim handlers, but to help them work faster, make more consistent decisions, and understand the reasoning behind each recommendation.

---

## 14. Quick Command Summary

```powershell
cd c:\msfde-uc007-fs-lab
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1

cd backend
uvicorn api:app --port 8000

cd ..\frontend
npm install
npm run dev

cd ..\eval
python evaluate.py
```

This is the minimum path to start the project, run it, and verify the output.
