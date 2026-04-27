import os
from openai import OpenAI
import streamlit as st



def _get_prompt(mode: str, context: str, jd_text: str = None) -> str:

    prompts = {

        # ---------------- STUDENT ----------------

        "student_overall": f"""
Return ONLY:

### Candidate Name
- Name: Extract full name from resume (if not found, write 'Not clearly mentioned')
- Email: Extract email from resume (if not found, write 'Not clearly mentioned')

### Candidate Summary
- 4 to 5 bullet points summarizing overall profile

### Strengths
- bullet points

### Weaknesses
- bullet points

### Best Fit Roles
- bullet points

### Final Hiring Signal
- Decision: Strong Hire / Hire / Consider / Reject
- Confidence: X%

Resume:
{context}
""",


        "student_resume_score": f"""
Return ONLY:

### Overall Score
- Score: X/10

### Score Breakdown
- Skills: X/10
- Experience: X/10
- Projects: X/10
- Clarity: X/10

### Final Hiring Signal
- Decision: Strong Hire / Hire / Consider / Reject
- Confidence: X%

Resume:
{context}
""",

        "student_profile_summary": f"""
Return ONLY:

### Candidate Snapshot
- Name:
- Experience Level:
- Primary Domain:
- Secondary Domain:
- Top Strength:
- Main Risk:

Resume:
{context}
""",

        "student_skills": f"""
Return ONLY:

### Skills Analysis
- Strong Skills:
- Moderate Skills:
- Weak / Missing Skills:

Resume:
{context}
""",

        "student_experience": f"""
Return ONLY:

### Experience Evaluation
- Experience Level:
- Industry Exposure:
- Relevance:

### Key Highlights
- bullet points

Resume:
{context}
""",

        "student_roles": f"""
Return ONLY:

### Role Fit Classification
- Strong Fit:
- Moderate Fit:
- Low Fit:

Resume:
{context}
""",

        "student_gaps": f"""
Return ONLY:

### Improvement Roadmap
- Priority 1
- Priority 2
- Priority 3

### Skill Gaps
- bullet points

Resume:
{context}
""",

        "student_interview": f"""
Return ONLY:

### Interview Readiness
- Score: X/10
- Level: Low / Medium / High

Resume:
{context}
""",

        # ---------------- RECRUITER ----------------

        "recruiter_overall": f"""
Return ONLY:

### Candidate Name
- Name: Extract full name from resume (if not found, write 'Not clearly mentioned')
- Email: Extract email from resume (if not found, write 'Not clearly mentioned')

### Candidate Snapshot
- Experience Level:
- Primary Domain:

### Strengths
- bullet points

### Risks
- bullet points

### Role Fit
- Strong / Moderate / Low

### Final Hiring Decision
- Decision: Strong Shortlist / Shortlist / Consider / Reject
- Confidence: X%

Resume:
{context}
""",

        "recruiter_snapshot": f"""
Return ONLY:

### Candidate Snapshot
- Name:
- Experience Level:
- Primary Domain:
- Secondary Domain:
- Top Strength:
- Main Risk:

Resume:
{context}
""",

        "recruiter_score": f"""
Return ONLY:

### Candidate Score
- Overall Score: X/10

### Final Hiring Signal
- Decision: Strong Shortlist / Shortlist / Consider / Reject
- Confidence: X%

Resume:
{context}
""",

        "recruiter_skills": f"""
Return ONLY:

### Skills & Tech Stack
- Core Skills:
- Supporting Skills:
- Missing Skills:

Resume:
{context}
""",

        "recruiter_experience": f"""
Return ONLY:

### Experience Summary
- Company / Role

### Contributions
- bullet points

Resume:
{context}
""",

        "recruiter_fit": f"""
Return ONLY:

### Role Fit
- Strong Fit:
- Moderate Fit:
- Low Fit:

Resume:
{context}
""",

        "recruiter_risks": f"""
Return ONLY:

### Risks / Concerns
- bullet points

Resume:
{context}
""",

        "recruiter_hiring": f"""
Return ONLY:

### Hiring Recommendation
- Decision: Strong Shortlist / Shortlist / Consider / Reject
- Confidence: X%

Resume:
{context}
""",

        # ---------------- JD MATCH ----------------

        "jd_match": f"""
Return ONLY:

### Match Score
- Score: X%

### Matched Skills
- bullet points

### Missing Skills
- bullet points

### Role Fit
- Strong / Moderate / Low

### Final Hiring Signal
- Decision: Strong Apply / Apply / Consider / Not Recommended
- Confidence: X%

Resume:
{context}

Job Description:
{jd_text}
"""
    }

    return prompts[mode]


def generate_analysis(context: str, mode: str, jd_text: str = None) -> str:
    api_key = os.getenv("OPENAI_API_KEY") or st.secrets["OPENAI_API_KEY"]

    if not api_key:
        raise ValueError("OPENAI_API_KEY not found")

    client = OpenAI(api_key=api_key)

    prompt = _get_prompt(mode, context, jd_text)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a precise ATS-style resume analyzer."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()