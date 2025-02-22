def find_missing_keywords(resume_text, job_description_text):
    """Finds keywords present in job description but missing in resume."""
    resume_words = set(resume_text.split())
    job_description_words = set(job_description_text.split())

    missing_keywords = job_description_words - resume_words
    return missing_keywords