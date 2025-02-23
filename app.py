from flask import Flask, request, jsonify
from resume_parser import extract_text_from_pdf, extract_text_from_docx
from job_parser import extract_text_from_txt, extract_text_from_url
from text_cleaner import clean_text
from similarity_matcher import compute_similarity, find_missing_keywords
from flask_cors import CORS
import os

app = Flask(__name__)

# Allowed origins: your deployed Streamlit URL and localhost for testing.
allowed_origins = [
    "https://ernie-phillips-ai-python-resume-keyword-scanner.streamlit.app",
    "http://localhost:8501"  # Adjust the port if needed.
]
CORS(app, resources={r"/upload": {"origins": allowed_origins}})

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/upload", methods=["POST"])
def upload_files():
    # Check for resume file
    if "resume" not in request.files:
        return jsonify({"error": "Please upload a resume file (PDF or DOCX)."}), 400

    # For job description, allow either a file or a URL parameter.
    has_job_file = "job_description" in request.files
    has_job_url = "job_description_url" in request.form

    if not (has_job_file or has_job_url):
        return jsonify({"error": "Please provide a job description as a file (PDF, DOCX, or TXT) or as a URL."}), 400

    # Process Resume
    resume_file = request.files["resume"]
    resume_path = os.path.join(UPLOAD_FOLDER, resume_file.filename)
    resume_file.save(resume_path)

    resume_filename = resume_file.filename.lower()
    if resume_filename.endswith(".pdf"):
        resume_text = extract_text_from_pdf(resume_path)
    elif resume_filename.endswith(".docx"):
        resume_text = extract_text_from_docx(resume_path)
    else:
        return jsonify({"error": "Unsupported resume file format. Use PDF or DOCX."}), 400

    resume_text = clean_text(resume_text)

    # Process Job Description
    if has_job_url:
        job_url = request.form.get("job_description_url")
        try:
            job_text = extract_text_from_url(job_url)
        except Exception as e:
            return jsonify({"error": "Failed to fetch job description from URL", "details": str(e)}), 400
    else:
        job_file = request.files["job_description"]
        job_path = os.path.join(UPLOAD_FOLDER, job_file.filename)
        job_file.save(job_path)
        job_filename = job_file.filename.lower()
        if job_filename.endswith(".txt"):
            job_text = extract_text_from_txt(job_path)
        elif job_filename.endswith(".docx"):
            job_text = extract_text_from_docx(job_path)
        elif job_filename.endswith(".pdf"):
            job_text = extract_text_from_pdf(job_path)
        else:
            return jsonify({"error": "Unsupported job description file format. Use PDF, DOCX, or TXT."}), 400

    job_text = clean_text(job_text)

    # Compute similarity percentage and missing keywords
    similarity_percentage = compute_similarity(resume_text, job_text)
    missing_keywords = find_missing_keywords(resume_text, job_text)

    # Define status thresholds
    if similarity_percentage >= 70:
        status = "Close Match"
    elif similarity_percentage >= 50:
        status = "Moderate Match"
    else:
        status = "Not Close"

    return jsonify({
        "match_percentage": similarity_percentage,
        "match_status": status,
        "missing_keywords": missing_keywords
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
