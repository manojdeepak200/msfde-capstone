# Capstone Project Presentation Notes

## Slide 1 – Title
"Good morning everyone. This project is an AI-powered motor claims review system designed to support insurance operations by reviewing mixed evidence and helping claim handlers make safer, more consistent decisions."

## Slide 2 – Problem Statement and Objectives
"The core problem is that motor claims often contain incomplete, conflicting, or suspicious information across several documents and photos. Reviewing those claims manually is time-consuming and inconsistent. Our objective was to build an AI-assisted workflow that extracts facts, validates them, checks policy conditions, identifies risk indicators, and recommends a safe next action while keeping the final human decision in the loop."

## Slide 3 – Methodology
"Our methodology followed a structured pipeline. We started by collecting claim evidence from the case folder, then extracted key facts from claim forms, repair estimates, policy schedules, customer statements, and photos. We then ran validation rules to compare dates, VINs, damage locations, and estimates. Finally, a policy-grounded reasoning layer produced a recommendation such as proceed, request information, or refer."

## Slide 4 – Implementation: Framework and Data Flow
"The solution uses a Python backend with FastAPI, a React frontend dashboard, and structured data storage for prepared claims. The detailed data flow is as follows: claim evidence is loaded from the case folder, files are classified by type, extraction modules read the relevant fields, visual assessment checks the photographs, validation rules compare dates, VINs, damage locations and estimate values, policy-grounded reasoning decides the outcome, and the final recommendation is shown to the human reviewer in the dashboard. The workflow ends with a handler making the final decision, ensuring that AI supports the process without taking ownership of the claim."

## Slide 5 – Results and Discussion
"The model performed strongly across all five sample claims. We achieved 45 out of 45 extraction matches, 11 out of 11 findings detected, and 5 out of 5 recommendation matches. There were zero safety violations, and all five claims passed evaluation. This demonstrates that the workflow can correctly distinguish between valid claims, incomplete claims, contradictory claims, policy exceptions, and fraud-like scenarios."

## Slide 6 – Conclusion
"In conclusion, this project shows a realistic, governance-safe use of AI in insurance operations. It reduces manual review effort, increases consistency, and delivers explainable decisions grounded in evidence and policy. The result is an operationally relevant prototype that supports the claims handler rather than replacing them."

## Closing Statement
"Thank you for your time. This project demonstrates how AI can support safer, faster, and more explainable claims decision-making in a real-world insurance workflow."
