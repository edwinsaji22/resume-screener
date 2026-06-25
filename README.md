# 📄 Resume Screening & Job-Fit Scorer

An NLP-powered tool that analyzes how well a resume matches a job description, highlights missing skills, and provides actionable feedback to improve the match — built as a placement portfolio project.

## 🎯 Features

- **Single Resume Analysis** — upload a resume + paste a job description to get an instant fit score
- **Weighted Scoring** — combines skill keyword matching (60%) with semantic similarity from sentence embeddings (40%) for a more accurate, explainable score than similarity alone
- **Skill Gap Detection** — identifies exactly which skills from the job description are missing in the resume
- **Diagnostic Feedback** — when the score is low, the tool explains *why* (missing skills, thin content, no education detected, keyword mismatch) and suggests specific fixes
- **Bulk Resume Ranking** — upload multiple resumes against one job description and rank them by fit score (recruiter-facing use case)
- **Downloadable Reports** — export single analysis as `.txt` or bulk rankings as `.csv`

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Frontend/UI | Streamlit |
| PDF Parsing | pdfplumber |
| NLP / Entity Extraction | spaCy |
| Semantic Similarity | Sentence-Transformers (`all-MiniLM-L6-v2`) |
| Scoring Logic | scikit-learn (cosine similarity) |
| Data Handling | pandas |

## 📐 How the Scoring Works

Rather than relying on a single similarity number (which can be misleading — even a strong resume rarely scores 90%+ against a job description using raw text embeddings), this tool combines two signals:

1. **Skill Keyword Match (60% weight):** What % of the job's required skills appear in the resume — concrete and explainable
2. **Semantic Similarity (40% weight):** Overall meaning-level similarity between resume and JD text, computed via sentence embeddings — catches relevant experience that doesn't use exact keywords
Final Score = (0.6 × Skill Match %) + (0.4 × Semantic Similarity %)
## 🚀 Running Locally

```bash
git clone https://github.com/YOUR_USERNAME/resume-screener.git
cd resume-screener

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
python -m spacy download en_core_web_sm

streamlit run app.py
```

## 📂 Project Structure
resume-screener/

├── app.py

├── parser.py

├── extractor.py

├── scorer.py

├── skills_db.py

├── requirements.txt

└── sample_resumes/
## 👤 Author

**Edwin Saji**
MCA Student, Kristu Jayanti University