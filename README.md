# 🩺 Multi-Agent Medical Diagnosis Platform

A **multi-agent AI system** that simulates a panel of medical specialists collaborating to reach a diagnosis, instead of relying on a single black-box model.

## 🧠 How It Works
Three specialist agents independently analyze the same patient case, then a **Coordinator Agent** synthesizes their opinions into a final consensus diagnosis with confidence scores.

- **General Physician Agent** — reviews symptoms & history, flags red-flag combinations
- **Radiologist Agent** — analyzes imaging findings (simulated structured input)
- **Pathologist Agent** — reviews lab values and biomarkers
- **Coordinator Agent** — resolves disagreements, weighs specialist confidence, produces final diagnosis + reasoning trail

## 🛠️ Tech Stack
- Python, Streamlit (UI)
- Rule-based + LLM-style agent reasoning (pluggable with OpenAI/Claude API)
- Pandas for structured patient case data
- JSON-based agent debate log for full explainability

## 🚀 Getting Started
```bash
git clone https://github.com/Varshini487/multi-agent-medical-diagnosis-platform
cd multi-agent-medical-diagnosis-platform
pip install -r requirements.txt
streamlit run app.py
```

## 💡 Use Cases
- Clinical decision support systems
- Second-opinion tools for rural/under-resourced clinics
- Medical education (showing how specialists reason differently)
- Research into multi-agent consensus reliability

## 🎤 Interview Talking Points
1. **Why multi-agent instead of one model?** Different specialists weigh evidence differently (a radiologist trusts imaging, a pathologist trusts labs). A single model conflates these signals; separate agents keep reasoning traceable and let you audit *which* agent drove the diagnosis.
2. **Consensus & disagreement handling.** The Coordinator doesn't just average — it weights each agent's confidence and flags cases where agents disagree strongly as "needs human review," which is safer than silently averaging conflicting signals.
3. **Explainability by design.** Every agent logs its reasoning trail (symptoms considered, thresholds triggered). This produces an audit trail doctors can actually check, unlike a single opaque classifier.
