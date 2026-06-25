from parser import extract_text_from_pdf
from extractor import extract_skills, extract_education
from scorer import compute_similarity, missing_skills

with open("sample_resumes/sampleresume.pdf", "rb") as f:
    resume_text = extract_text_from_pdf(f)

jd_text = "Looking for a customer service representative with experience in retail and sports stores, good communication skills, reliable and hardworking."

resume_skills = extract_skills(resume_text)
jd_skills = extract_skills(jd_text)

score = compute_similarity(resume_text, jd_text)
missing = missing_skills(resume_skills, jd_skills)

print("FIT SCORE:", score, "%")
print("MISSING SKILLS:", missing)