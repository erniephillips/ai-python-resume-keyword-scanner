import spacy

# Load the lightweight spaCy model. Make sure you have en_core_web_sm installed:
# python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")


def extract_keywords(text):
    """
    Extracts keywords from text using noun chunks.
    """
    doc = nlp(text)
    # Using noun chunks as candidate keywords; you could also add entities or other heuristics.
    keywords = {chunk.text.lower().strip() for chunk in doc.noun_chunks if len(chunk.text.split()) > 1}
    return list(keywords)


def find_missing_keywords(resume_text, job_description_text, threshold=0.70):
    """
    For each keyword extracted from the job description, calculates semantic similarity
    to the resume text. Keywords with similarity below the threshold are considered missing.
    Also returns the average similarity across all keywords.
    """
    resume_doc = nlp(resume_text)
    job_keywords = extract_keywords(job_description_text)

    missing = []
    similarities = []
    for kw in job_keywords:
        kw_doc = nlp(kw)
        sim = kw_doc.similarity(resume_doc)
        similarities.append(sim)
        if sim < threshold:
            missing.append(kw)

    avg_similarity = sum(similarities) / len(similarities) if similarities else 0.0
    return missing, avg_similarity


def get_status_descriptor(match_rating):
    """
    Returns a status descriptor based on the match rating (0.0 - 1.0).
    """
    if match_rating >= 0.85:
        return "Excellent Match"
    elif match_rating >= 0.70:
        return "Good Match"
    elif match_rating >= 0.55:
        return "Average Match"
    else:
        return "Poor Match"


def analyze_resume(resume_text, job_description_text):
    """
    Analyzes the resume versus the job description and returns:
    - match_percentage: overall similarity (0-100%)
    - status: a descriptor of how good the match is
    - missing_keywords: list of job description keywords that are not well represented in the resume
    """
    missing_keywords, avg_similarity = find_missing_keywords(resume_text, job_description_text)
    status = get_status_descriptor(avg_similarity)
    match_percentage = round(avg_similarity * 100, 2)
    return match_percentage, status, missing_keywords
