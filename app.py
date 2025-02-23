from flask import Flask, request, jsonify
from resume_parser import extract_text_from_pdf
from job_parser import extract_text_from_txt
from text_cleaner import clean_text
from keyword_matcher import find_missing_keywords
from deep_learning_utils import get_text_embedding, compute_similarity
import os
import numpy as np

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/upload", methods=["POST"])
def upload_files():
    if "resume" not in request.files or "job_description" not in request.files:
        return jsonify({"error": "Please upload both resume (PDF) and job description (TXT)."}), 400

    resume_file = request.files["resume"]
    job_file = request.files["job_description"]

    resume_path = os.path.join(UPLOAD_FOLDER, resume_file.filename)
    job_path = os.path.join(UPLOAD_FOLDER, job_file.filename)

    resume_file.save(resume_path)
    job_file.save(job_path)

    # Extract and clean text
    resume_text = clean_text(extract_text_from_pdf(resume_path))
    job_text = clean_text(extract_text_from_txt(job_path))

    # Deep Learning Comparison with error handling
    try:
        resume_embedding = get_text_embedding(resume_text)
        job_embedding = get_text_embedding(job_text)
        similarity_score = compute_similarity(resume_embedding, job_embedding)
        status = "good match" if similarity_score >= 0.7 else "needs improvement"
    except Exception as e:
        # Log the error if possible, and provide fallback values
        print("Deep learning error:", e)
        similarity_score = None
        status = None

    # Run keyword matching as well
    missing_keywords = find_missing_keywords(resume_text, job_text)

    result = {
        "similarity_score": float(np.round(similarity_score, 3)) if similarity_score is not None else None,
        "status": status,
        "missing_keywords": list(missing_keywords)
    }
    return jsonify(result)

if __name__ == "__main__":
    # In production, you may want to use gunicorn rather than app.run()
    app.run(debug=True)
