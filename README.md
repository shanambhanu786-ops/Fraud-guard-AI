# Fraud-guard-AI
# 🏦 FinGuard AI — Advanced Credit Risk & Default Prediction Engine

**Track:** Problem Statement 4: Default Prediction Model  
**Team Name:** Tech Girl  
**Team Leader:** Bhanu  

---

## 📌 Project Overview
FinGuard AI is an enterprise-grade, compliance-ready generative AI solution engineered for commercial loan underwriters evaluating MSME credit applications. 

Unstructured financial records (diverse ledger prints, messy tax statements, scattered balance sheets) traditionally present significant credit analysis bottlenecks. FinGuard AI leverages LLMs to ingest this raw data, run real-time stress-rate scenario models, and flag accounting mismatches. 

To bridge the gap between "black box" AI hallucinations and the strict auditability mandates of institutions like IDBI Bank, the entire system is actively monitored via **LangSmith Tracing** and bound by an adversarial **Reverse Prompt Engineering Audit** before executing system webhooks.

---

## 🛠️ Key Architectural Innovations

### 1. Advanced Prompt Frameworks (RTF + TCI + CoT)
To ensure output deterministic alignment, the baseline evaluation engine enforces a multi-layered prompt boundary:
*   **RTF (Role-Task-Format):** Restricts the model domain to a senior banking credit auditor and outputs rigorous, schema-validated JSON.
*   **TCI (Task-Context-Instruction):** Explicitly handles processing anomalies (e.g., zero-extrapolation limits, forcing explicit `NULL` handling on missing vectors).
*   **Chain-of-Thought (CoT):** Mandates clear, step-by-step arithmetic deductions for complex credit metrics before calculating final scores.

### 2. Reverse Prompt Engineering (RPE) Audit Loop
Instead of trusting the extracted metrics at face value, FinGuard AI introduces an adversarial verification firewall. A secondary forensic prompt attempts to reconstruct the original raw financial records using *only* the generated JSON memo. If the mathematical outputs or implied data constraints don't cross-validate perfectly against the ground truth, the pipeline automatically halts and generates an anomaly report.

### 3. Dynamic Scenario Planning & Stress-Rating
The engine dynamically stress-tests applicant profiles by applying variable shock thresholds across target operations (e.g., simulating a $+200\text{ bps}$ borrowing rate spike) to evaluate the stability of the Debt-Service Coverage Ratio (DSCR) across variable macro-economic states.

### 4. Real-Time Event Webhooks
Upon passing the reverse-engineering validation engine, the backend automatically triggers an asynchronous webhook payload broadcasting the `default_risk_tier` and structural audit metrics back to registered endpoints in IDBI's Core Banking Solution (CBS).

---

## 📂 Repository Layout

```text
finguard_app/
├── requirements.txt         # Core dependencies (FastAPI, Streamlit, LangChain, LangSmith)
├── main.py                 # FastAPI engine, RPE logic, and background webhook dispatcher
├── app.py                  # Underwriter UI dashboard built on Streamlit
├── prompts.json            # Centralized structural template manifest (RTF, TCI, CoT strings)
├── prompt_manager.py       # Injector component creating LangChain prompt templates
└── README.md               # Setup and project description index (This File)
