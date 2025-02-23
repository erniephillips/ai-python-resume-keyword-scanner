from flask import Flask, request, jsonify
from resume_parser import extract_text_from_pdf, extract_text_from_docx
from job_parser import extract_text_from_txt, extract_text_from_url
from text_cleaner import clean_text
from keyword_matcher import find_missing_keywords
from flask_cors import CORS
import os

app = Flask(__name__)

# Allowed origins: your deployed Streamlit URL and localhost for testing.
allowed_origins = [
    "https://ernie-hillips-ai-python-resume-keyword-scanner.streamlit.app",
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
        return jsonify({"error": "Please provide a job description as a file (TXT or DOCX) or as a URL."}), 400

    resume_file = request.files["resume"]
    resume_path = os.path.join(UPLOAD_FOLDER, resume_file.filename)
    resume_file.save(resume_path)

    # Decide how to extract resume text based on file extension
    resume_filename = resume_file.filename.lower()
    if resume_filename.endswith(".pdf"):
        resume_text = extract_text_from_pdf(resume_path)
    elif resume_filename.endswith(".docx"):
        resume_text = extract_text_from_docx(resume_path)
    else:
        return jsonify({"error": "Unsupported resume file format. Use PDF or DOCX."}), 400

    resume_text = clean_text(resume_text)

    # Extract job description text
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
        else:
            return jsonify({"error": "Unsupported job description file format. Use TXT or DOCX."}), 400

    job_text = clean_text(job_text)

    # Find missing keywords between the resume and job description texts
    missing_keywords = find_missing_keywords(resume_text, job_text)

    return jsonify({
        "missing_keywords": list(missing_keywords)
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
