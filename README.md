# AI Resume Intelligence Platform

An AI-powered resume analysis platform that helps students, job seekers, and recruiters evaluate resumes with ATS-style scoring, job description matching, recruiter insights, skill gap analysis, and downloadable professional reports.

## Live Demo

🔗 https://ai-resume-intelligence-byisha.streamlit.app/

## Project Overview

AI Resume Intelligence Platform is built to analyse resumes intelligently and provide structured feedback similar to how an ATS or recruiter reviews a candidate profile. Users can upload a PDF resume, paste a job description, and receive AI-generated insights such as resume score, matched skills, missing skills, role fit, interview readiness, strengths, risks, and final hiring recommendation.

The platform includes two modes:

- **Student View** – helps candidates improve resumes, identify gaps, prepare for interviews, and understand suitable job roles.
- **Recruiter View** – helps recruiters quickly evaluate candidate fit, risks, skills, experience, and hiring signals.

## Key Features

- PDF resume upload and text extraction
- ATS-style resume scoring
- Job description matching
- Matched and missing skills analysis
- Student-focused resume improvement dashboard
- Recruiter-focused candidate evaluation dashboard
- Role fit classification
- Interview readiness analysis
- Final hiring / shortlist recommendation
- AI-generated resume insights using OpenAI
- Downloadable professional PDF report
- Clean Streamlit-based interactive UI
- Visitor counter integration

## Technologies Used

- **Python** – Core application logic
- **Streamlit** – Frontend and interactive web application
- **OpenAI API / GPT-4o-mini** – AI-powered resume analysis and feedback generation
- **LangChain Community** – PDF document loading support
- **PyPDF / PyPDFLoader** – Resume PDF text extraction
- **ReportLab** – Professional PDF report generation
- **Python-dotenv** – Environment variable management
- **Regular Expressions** – Text parsing, score extraction, and result formatting
- **HTML/CSS** – Custom UI styling
- **Shell Script** – App startup support
- **Claude Code AI** – Used as an AI coding assistant for development, debugging, code structuring, and improving implementation quality

## Tech Stack Summary

```text
Frontend/UI: Streamlit, HTML, CSS
Backend Logic: Python
AI/LLM: OpenAI API, GPT-4o-mini
PDF Processing: LangChain PyPDFLoader, PyPDF
Report Generation: ReportLab
Environment Management: python-dotenv
AI Development Support: Claude Code AI
Deployment: Streamlit Cloud
