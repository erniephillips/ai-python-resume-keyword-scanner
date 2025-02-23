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

    try:
        # Extract and clean text
        resume_text = clean_text(extract_text_from_pdf(resume_path))
        job_text = clean_text(extract_text_from_txt(job_path))

        # Deep Learning Comparison
        resume_embedding = get_text_embedding(resume_text)
        job_embedding = get_text_embedding(job_text)
        similarity_score = compute_similarity(resume_embedding, job_embedding)
    except Exception as e:
        # Log the error details (you can also print to stdout for Render logs)
        return jsonify({"error": "Deep learning analysis failed", "details": str(e)}), 500

    # Determine match status based on a threshold (0.7 in this case)
    status = "good match" if similarity_score >= 0.7 else "needs improvement"

    # Run keyword matching
    missing_keywords = find_missing_keywords(resume_text, job_text)

    result = {
        "similarity_score": float(np.round(similarity_score, 3)),
        "status": status,
        "missing_keywords": list(missing_keywords)
    }
    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)

