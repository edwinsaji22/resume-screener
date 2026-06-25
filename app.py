import streamlit as st
from parser import extract_text_from_pdf
from extractor import extract_skills, extract_education
from scorer import compute_weighted_score, missing_skills

st.set_page_config(page_title="Resume-JD Fit Scorer", page_icon="📄", layout="wide")

# ---- CUSTOM CSS ----
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

.main {
    background-color: #FFFFFF;
}

/* Fade-in animation for the whole page */
.main .block-container {
    animation: fadeIn 0.6s ease-in-out;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Hero header */
.hero {
    background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
    padding: 40px;
    border-radius: 16px;
    color: white;
    margin-bottom: 30px;
    animation: slideDown 0.5s ease-out;
}
@keyframes slideDown {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}
.hero h1 {
    font-size: 2.2rem;
    font-weight: 800;
    margin-bottom: 8px;
    color: white;
}
.hero p {
    font-size: 1.05rem;
    opacity: 0.9;
    color: #E0E7FF;
}

/* Card style */
.card {
    background-color: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 16px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(37, 99, 235, 0.15);
}

/* Buttons */
.stButton button {
    background-color: #2563EB;
    color: white;
    font-weight: 600;
    border-radius: 8px;
    padding: 10px 24px;
    border: none;
    transition: all 0.2s ease;
}
.stButton button:hover {
    background-color: #1D4ED8;
    color: white;
    transform: scale(1.03);
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0F172A;
}
[data-testid="stSidebar"] * {
    color: #F1F5F9 !important;
}

/* Section headers */
h2, h3 {
    color: #0F172A;
    font-weight: 700;
}

/* Smooth progress bar fill */
.stProgress > div > div {
    transition: width 1s ease-in-out;
}

/* Skill chips */
.chip {
    display: inline-block;
    background-color: #DBEAFE;
    color: #1E40AF;
    border-radius: 20px;
    padding: 6px 14px;
    margin: 4px;
    font-size: 0.85rem;
    font-weight: 600;
}
.chip-missing {
    display: inline-block;
    background-color: #FEE2E2;
    color: #991B1B;
    border-radius: 20px;
    padding: 6px 14px;
    margin: 4px;
    font-size: 0.85rem;
    font-weight: 600;
}
.chip-good {
    display: inline-block;
    background-color: #D1FAE5;
    color: #065F46;
    border-radius: 20px;
    padding: 6px 14px;
    margin: 4px;
    font-size: 0.85rem;
    font-weight: 600;
}
.chip-empty {
    color: #64748B;
    font-style: italic;
    font-size: 0.9rem;
}
.card-title {
    font-weight: 700;
    font-size: 1.05rem;
    color: #0F172A;
    margin-bottom: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---- SIDEBAR ----
with st.sidebar:
    st.markdown("### 📄 Resume Scorer")
    st.write("AI-powered resume and job-description matching tool.")
    st.markdown("---")
    st.write("**Built by:** Edwin Saji")
    st.write("**Tech Stack:**")
    st.write("- spaCy (NLP)")
    st.write("- Sentence-Transformers")
    st.write("- Streamlit")

# ---- HERO HEADER ----
st.markdown("""
<div class="hero">
    <h1>📄 Resume Screening & Job-Fit Scorer</h1>
    <p>Upload a resume and job description to get an instant AI-powered fit analysis</p>
</div>
""", unsafe_allow_html=True)

# ---- SINGLE RESUME ANALYSIS ----
st.markdown("## 🎯 Single Resume Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Upload Resume (PDF)")
    resume_file = st.file_uploader("Choose PDF", type="pdf")

with col2:
    st.subheader("Paste Job Description")
    jd_text = st.text_area("Job Description", height=250)

if st.button("Analyze Fit") and resume_file and jd_text:
    with st.spinner("🔍 Analyzing resume against job description..."):
        resume_text = extract_text_from_pdf(resume_file)

        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(jd_text)
        edu = extract_education(resume_text)

        score, semantic_score, skill_pct = compute_weighted_score(resume_text, jd_text, resume_skills, jd_skills)
        missing = missing_skills(resume_skills, jd_skills)

    st.markdown("---")
    st.markdown("## 📊 Results")

    if score >= 70:
        badge_color, badge_bg, badge_label = "#065F46", "#D1FAE5", "✅ Strong Match"
    elif score >= 40:
        badge_color, badge_bg, badge_label = "#92400E", "#FEF3C7", "⚠️ Moderate Match"
    else:
        badge_color, badge_bg, badge_label = "#991B1B", "#FEE2E2", "❌ Weak Match"

    st.markdown(f"""
    <div style="background-color:{badge_bg}; color:{badge_color}; border-radius:12px; padding:20px 28px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:1.1rem; font-weight:700;">{badge_label}</span>
        <span style="font-size:1.8rem; font-weight:800;">{score}%</span>
    </div>
    <p style="color:#64748B; font-size:0.85rem; margin-bottom:18px;">
        Based on: Skill Keyword Match ({skill_pct if skill_pct is not None else 'N/A'}%) + Semantic Similarity ({semantic_score}%)
    </p>
    """, unsafe_allow_html=True)

    st.progress(int(score) / 100)

    # ---- DIAGNOSTIC FEEDBACK ----
    if score < 70:
        st.markdown("### 🔧 What's Holding Back Your Score & What To Do")
        reasons = []

        if missing:
            reasons.append(
                f"<li><b>Missing {len(missing)} skill(s) the job asks for:</b> "
                f"{', '.join(missing)}. Add these to your resume if you have relevant experience, "
                f"projects, or coursework — even a small project counts.</li>"
            )

        if len(resume_skills) < 5:
            reasons.append(
                "<li><b>Very few technical skills detected overall.</b> "
                "Add a clear, dedicated 'Skills' section listing your tools, languages, and technologies "
                "so they're easy to find — both for this scanner and for real recruiters/ATS systems.</li>"
            )

        if not edu:
            reasons.append(
                "<li><b>No education details detected.</b> "
                "Make sure your degree, college name, and graduation year are clearly written, "
                "not just embedded inside a paragraph.</li>"
            )

        word_count = len(resume_text.split())
        if word_count < 150:
            reasons.append(
                "<li><b>Resume content seems thin.</b> "
                "Add more detail about your projects, responsibilities, and measurable achievements "
                "(numbers, scale, impact) — this also improves the semantic similarity score.</li>"
            )

        if skill_pct is not None and skill_pct < 50 and semantic_score >= 50:
            reasons.append(
                "<li><b>Your overall writing style matches the job description, but specific skill keywords don't line up.</b> "
                "Try using the exact terms from the job posting (e.g. write 'AWS' instead of just 'cloud computing') "
                "since scanners and recruiters often search for exact keywords.</li>"
            )

        if not reasons:
            reasons.append(
                "<li>No major gaps detected — the score may simply reflect that this particular job description "
                "is broader or more senior-focused than your current resume. Try testing against a role closer to your experience level.</li>"
            )

        st.markdown(f"""
        <div class="card" style="border-left: 4px solid #F59E0B;">
            <ul style="margin:0; padding-left:20px; color:#334155;">{''.join(reasons)}</ul>
        </div>
        """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        skills_html = "".join([f'<span class="chip">{s}</span>' for s in resume_skills]) if resume_skills else '<span class="chip-empty">None detected</span>'
        edu_html = "".join([f'<span class="chip-good">{e}</span>' for e in edu]) if edu else '<span class="chip-empty">None detected</span>'

        st.markdown(f"""
        <div class="card">
            <div class="card-title">🛠️ Skills Found in Resume</div>
            <div>{skills_html}</div>
            <div class="card-title" style="margin-top:18px;">🎓 Education Detected</div>
            <div>{edu_html}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        total_required = len(jd_skills)
        matched_count = total_required - len(missing)

        if total_required == 0:
            subtitle = "No specific technical skills were detected in the job description text."
        else:
            subtitle = f"Matched {matched_count} out of {total_required} required skills"

        st.markdown(f"""
        <div class="card">
            <div class="card-title">⚠️ Skills the Job Description Asks For (Missing in Resume)</div>
            <p style="color:#475569; margin-bottom:10px;">{subtitle}</p>
        """, unsafe_allow_html=True)

        if total_required == 0:
            st.markdown('<div class="chip-empty">Try pasting a more detailed job description that lists specific tools or technologies.</div></div>', unsafe_allow_html=True)
        elif missing:
            missing_html = "".join([f'<span class="chip-missing">{s}</span>' for s in missing])
            st.markdown(f"<div>{missing_html}</div></div>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="chip-good" style="display:block;">✅ All required skills present!</div></div>', unsafe_allow_html=True)

    # ---- DOWNLOADABLE REPORT ----
    report = f"""RESUME — JOB FIT REPORT
========================
Fit Score (Weighted): {score}%
Match Level: {badge_label}

Score Breakdown:
- Skill Keyword Match: {skill_pct if skill_pct is not None else 'N/A'}%
- Semantic Similarity: {semantic_score}%

Skills Found in Resume:
{', '.join(resume_skills) if resume_skills else 'None detected'}

Education Detected:
{', '.join(edu) if edu else 'None detected'}

Skills Required by Job Description: {total_required if total_required > 0 else 'None detected — try a more detailed job description'}
Skills Matched: {matched_count if total_required > 0 else 'N/A'}
Missing Skills:
{', '.join(missing) if missing else 'None — all required skills present!'}
"""
    st.download_button(
        label="📥 Download Report",
        data=report,
        file_name="resume_fit_report.txt",
        mime="text/plain"
    )

# ---- BULK RANKING ----
st.markdown("---")
st.markdown("## 🔁 Bulk Ranking")
st.caption("Rank multiple resumes against one job description")

jd_text_bulk = st.text_area("Job Description", height=150, key="bulk_jd")
resumes = st.file_uploader("Upload Multiple Resumes", type="pdf", accept_multiple_files=True, key="bulk_resumes")

if st.button("Rank Resumes") and resumes and jd_text_bulk:
    with st.spinner("🔍 Ranking resumes..."):
        results = []
        jd_skills_bulk = extract_skills(jd_text_bulk)
        for r in resumes:
            text = extract_text_from_pdf(r)
            text_skills = extract_skills(text)
            score, _, _ = compute_weighted_score(text, jd_text_bulk, text_skills, jd_skills_bulk)
            results.append({"Resume": r.name, "Score": score})

        results.sort(key=lambda x: x["Score"], reverse=True)

    st.table(results)

    import pandas as pd
    df = pd.DataFrame(results)
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Ranking as CSV",
        data=csv,
        file_name="resume_ranking.csv",
        mime="text/csv"
    )