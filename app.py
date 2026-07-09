import streamlit as st
import json
import random

st.set_page_config(page_title="🩺 Multi-Agent Medical Diagnosis", layout="wide")
st.title("🩺 Multi-Agent Medical Diagnosis Platform")
st.markdown("A panel of specialist AI agents collaborates to reach a diagnosis consensus.")

st.sidebar.header("📋 Patient Case Input")
age = st.sidebar.slider("Age", 1, 100, 45)
fever = st.sidebar.checkbox("Fever")
cough = st.sidebar.checkbox("Persistent Cough")
chest_pain = st.sidebar.checkbox("Chest Pain")
fatigue = st.sidebar.checkbox("Fatigue")
imaging_abnormal = st.sidebar.checkbox("Imaging shows abnormality (simulated)")
wbc_high = st.sidebar.checkbox("Elevated WBC count (simulated lab)")
crp_high = st.sidebar.checkbox("Elevated CRP (simulated lab)")

def gp_agent():
    score = 0
    reasoning = []
    if fever: score += 0.25; reasoning.append("Fever present (+0.25)")
    if cough: score += 0.2; reasoning.append("Persistent cough (+0.2)")
    if chest_pain: score += 0.3; reasoning.append("Chest pain (+0.3)")
    if fatigue: score += 0.1; reasoning.append("Fatigue (+0.1)")
    if age > 60: score += 0.15; reasoning.append("Age >60 raises risk (+0.15)")
    return min(score, 1.0), reasoning

def radiologist_agent():
    score = 0.8 if imaging_abnormal else 0.1
    reasoning = ["Imaging abnormality detected (+0.8)"] if imaging_abnormal else ["No imaging abnormality (+0.1 baseline)"]
    return score, reasoning

def pathologist_agent():
    score = 0
    reasoning = []
    if wbc_high: score += 0.5; reasoning.append("Elevated WBC suggests infection/inflammation (+0.5)")
    if crp_high: score += 0.4; reasoning.append("Elevated CRP suggests active inflammation (+0.4)")
    return min(score, 1.0), reasoning

def coordinator_agent(gp, rad, path):
    gp_score, gp_r = gp
    rad_score, rad_r = rad
    path_score, path_r = path
    weights = {"gp": 0.35, "rad": 0.35, "path": 0.30}
    final = gp_score*weights["gp"] + rad_score*weights["rad"] + path_score*weights["path"]
    disagreement = max(gp_score, rad_score, path_score) - min(gp_score, rad_score, path_score)
    return final, disagreement, gp_r + rad_r + path_r

if st.button("🔬 Run Multi-Agent Diagnosis"):
    gp = gp_agent()
    rad = radiologist_agent()
    path = pathologist_agent()
    final_score, disagreement, log = coordinator_agent(gp, rad, path)

    col1, col2, col3 = st.columns(3)
    col1.metric("👨‍⚕️ GP Agent", f"{gp[0]:.0%}")
    col2.metric("🩻 Radiologist Agent", f"{rad[0]:.0%}")
    col3.metric("🧪 Pathologist Agent", f"{path[0]:.0%}")

    st.markdown("### 🧭 Coordinator Final Verdict")
    if final_score > 0.6:
        st.error(f"⚠️ High likelihood of significant condition — Consensus Score: {final_score:.0%}")
    elif final_score > 0.35:
        st.warning(f"🟡 Moderate likelihood — Consensus Score: {final_score:.0%}")
    else:
        st.success(f"✅ Low likelihood — Consensus Score: {final_score:.0%}")

    if disagreement > 0.4:
        st.warning(f"🚩 Agents disagree significantly (spread {disagreement:.0%}) — flagged for human review")

    with st.expander("🧾 Full Reasoning Trail"):
        for r in log:
            st.write("- " + r)

st.markdown("---")
st.caption("Demo uses rule-based agents for transparency. Swap in an LLM (OpenAI/Claude) per agent for production use.")
