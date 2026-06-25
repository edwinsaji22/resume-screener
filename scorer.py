from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')  # small, fast, good enough

def compute_similarity(resume_text, jd_text):
    embeddings = model.encode([resume_text, jd_text])
    score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return round(float(score) * 100, 2)  # percentage

def missing_skills(resume_skills, jd_skills):
    return list(set(jd_skills) - set(resume_skills))

def compute_weighted_score(resume_text, jd_text, resume_skills, jd_skills):
    """
    Combines two signals into one final score:
    - skill_pct: % of JD's required skills found in the resume (concrete, explainable)
    - semantic_score: overall text similarity (catches things keyword matching misses)

    Weighted 60% skills / 40% semantic, since skill match is the more reliable signal.
    """
    semantic_score = compute_similarity(resume_text, jd_text)

    if jd_skills:
        matched = len(set(resume_skills) & set(jd_skills))
        skill_pct = round((matched / len(jd_skills)) * 100, 2)
        weighted = round(0.6 * skill_pct + 0.4 * semantic_score, 2)
    else:
        # No skills detected in JD text at all - fall back to semantic score alone
        skill_pct = None
        weighted = semantic_score

    return weighted, semantic_score, skill_pct
