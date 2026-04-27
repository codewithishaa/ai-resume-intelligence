from dotenv import load_dotenv
import streamlit as st
import os
import re
import requests

from utils.qa_chain import generate_analysis
from utils.pdf_loader import load_pdf_text
from utils.report_generator import create_pdf_bytes

# ---------------- LOAD ENV ----------------
load_dotenv()

# ---------------- VISITOR COUNTER ----------------
import requests

import requests
def get_visitor_count():
    file = "counter.txt"

    # Create file if not exists
    if not os.path.exists(file):
        with open(file, "w") as f:
            f.write("0")

    # Read current count
    with open(file, "r") as f:
        count = int(f.read())

    # Increment
    count += 1

    # Save updated count
    with open(file, "w") as f:
        f.write(str(count))

    return count
    
# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Resume Intelligence Platform", layout="wide")

# ---------------- CSS ----------------
css_path = "styles.css"
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<h1 style='text-align:center;'>AI Resume Intelligence Platform</h1>
<p style='text-align:center; color:gray;'>
ATS Scoring • JD Matching • Recruiter Insights • Career Intelligence
</p>
""", unsafe_allow_html=True)

# ---------------- FUNCTIONS ----------------

def show_score_dashboard(result):
    score_10 = re.search(r"Score:\s*(\d+\.?\d*)/10", result)
    score_percent = re.search(r"Score:\s*(\d+\.?\d*)%", result)

    if score_10:
        score = float(score_10.group(1))
        st.metric("📊 Overall Score", f"{score}/10")
        st.progress(int(score * 10))

    elif score_percent:
        score = float(score_percent.group(1))
        st.metric("📊 Match Score", f"{score}%")
        st.progress(int(score))


def show_final_decision(result):
    decision = re.search(r"Decision:\s*(.*)", result)
    if decision:
        decision_text = decision.group(1).strip()

        if "Strong" in decision_text or "Hire" in decision_text:
            st.success(f"✅ Final Decision: {decision_text}")
        elif "Consider" in decision_text:
            st.warning(f"⚠️ Final Decision: {decision_text}")
        else:
            st.error(f"❌ Final Decision: {decision_text}")


def show_jd_visuals(result):
    matched = re.findall(r"Matched Skills\n((?:- .*\n)+)", result, re.IGNORECASE)
    missing = re.findall(r"Missing Skills\n((?:- .*\n)+)", result, re.IGNORECASE)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✅ Matched Skills")
        if matched:
            for line in matched[0].split("\n"):
                if line.strip():
                    st.success(line.replace("-", "").strip())
        else:
            st.info("No matched skills found")

    with col2:
        st.markdown("### ❌ Missing Skills")
        if missing:
            for line in missing[0].split("\n"):
                if line.strip():
                    st.error(line.replace("-", "").strip())
        else:
            st.info("No missing skills found")


# ---------------- UPLOAD ----------------
uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

if uploaded_file:

    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.read())

    st.success("Resume uploaded successfully ✅")

    with st.spinner("Extracting resume..."):
        resume_text = load_pdf_text("temp_resume.pdf")

    if len(resume_text.strip()) < 100:
        st.error("⚠️ Could not extract proper text. Upload a valid PDF.")
        st.stop()

    st.markdown("### 📌 Job Description Matching")
    jd_text = st.text_area("Paste Job Description here")

    user_type = st.radio(
        "Select Mode",
        ["🎓 Student View", "💼 Recruiter View"],
        horizontal=True
    )

    result = None

    # ===================== STUDENT =====================
    if user_type == "🎓 Student View":

        st.markdown("## 🎓 Student Dashboard")

        col1, col2, col3 = st.columns(3)
        col4, col5, col6 = st.columns(3)
        col7, col8, col9 = st.columns(3)

        with col1:
            overview_btn = st.button("📊 Resume Score", use_container_width=True)
        with col2:
            summary_btn = st.button("📄 Summary", use_container_width=True)
        with col3:
            skills_btn = st.button("🛠 Skills", use_container_width=True)
        with col4:
            exp_btn = st.button("💼 Experience", use_container_width=True)
        with col5:
            roles_btn = st.button("🎯 Roles", use_container_width=True)
        with col6:
            gaps_btn = st.button("📉 Gaps", use_container_width=True)
        with col7:
            interview_btn = st.button("🧠 Interview", use_container_width=True)
        with col8:
            jd_btn = st.button("📌 JD Match", use_container_width=True)
        with col9:
            overall_btn = st.button("🧾 Overall Summary", use_container_width=True)

        if overview_btn:
            result = generate_analysis(resume_text, "student_resume_score")

        elif summary_btn:
            result = generate_analysis(resume_text, "student_profile_summary")

        elif skills_btn:
            result = generate_analysis(resume_text, "student_skills")

        elif exp_btn:
            result = generate_analysis(resume_text, "student_experience")

        elif roles_btn:
            result = generate_analysis(resume_text, "student_roles")

        elif gaps_btn:
            result = generate_analysis(resume_text, "student_gaps")

        elif interview_btn:
            result = generate_analysis(resume_text, "student_interview")

        elif jd_btn:
            if not jd_text.strip():
                st.warning("Please paste Job Description first.")
            else:
                result = generate_analysis(resume_text, "jd_match", jd_text)
                st.markdown("### 📊 JD Match Dashboard")
                show_score_dashboard(result)
                show_jd_visuals(result)

        elif overall_btn:
            result = generate_analysis(resume_text, "student_overall")

    # ===================== RECRUITER =====================
    else:

        st.markdown("## 💼 Recruiter Dashboard")

        col1, col2, col3 = st.columns(3)
        col4, col5, col6 = st.columns(3)
        col7, col8, col9 = st.columns(3)

        with col1:
            snapshot_btn = st.button("📌 Snapshot", use_container_width=True)
        with col2:
            score_btn = st.button("📊 Score", use_container_width=True)
        with col3:
            tech_btn = st.button("🛠 Skills", use_container_width=True)
        with col4:
            exp_sum_btn = st.button("💼 Experience", use_container_width=True)
        with col5:
            fit_btn = st.button("🎯 Fit", use_container_width=True)
        with col6:
            risk_btn = st.button("⚠️ Risks", use_container_width=True)
        with col7:
            hire_btn = st.button("✅ Hiring", use_container_width=True)
        with col8:
            jd_btn_r = st.button("📌 JD Match", use_container_width=True)
        with col9:
            overall_btn_r = st.button("🧾 Overall Candidate Summary", use_container_width=True)

        if snapshot_btn:
            result = generate_analysis(resume_text, "recruiter_snapshot")

        elif score_btn:
            result = generate_analysis(resume_text, "recruiter_score")

        elif tech_btn:
            result = generate_analysis(resume_text, "recruiter_skills")

        elif exp_sum_btn:
            result = generate_analysis(resume_text, "recruiter_experience")

        elif fit_btn:
            result = generate_analysis(resume_text, "recruiter_fit")

        elif risk_btn:
            result = generate_analysis(resume_text, "recruiter_risks")

        elif hire_btn:
            result = generate_analysis(resume_text, "recruiter_hiring")

        elif jd_btn_r:
            if not jd_text.strip():
                st.warning("Please paste Job Description first.")
            else:
                result = generate_analysis(resume_text, "jd_match", jd_text)
                st.markdown("### 📊 JD Match Dashboard")
                show_score_dashboard(result)
                show_jd_visuals(result)

        elif overall_btn_r:
            result = generate_analysis(resume_text, "recruiter_overall")

    # ===================== RESULT =====================
    if result:
        st.markdown("---")

        show_score_dashboard(result)
        show_final_decision(result)

        with st.expander("📄 View Full Analysis", expanded=True):
            st.markdown(result)

        pdf_data = create_pdf_bytes(result)

        st.download_button(
            label="📥 Download Professional Report",
            data=pdf_data,
            file_name="resume_report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

else:
    st.info("Upload a resume to begin 🚀")

# ===================== VISITOR COUNTER (ALWAYS VISIBLE) =====================
st.markdown("---")

count = get_visitor_count()

st.markdown(
    f"""
    <div style='text-align:center; color:gray; font-size:14px; margin-top:10px;'>
         Total Visitors: <b>{count}</b>
    </div>
    """,
    unsafe_allow_html=True
)