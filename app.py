from flask import Flask, request, jsonify
from resume_parser import extract_text_from_pdf
from job_parser import extract_text_from_txt
from text_cleaner import clean_text
from keyword_matcher import find_missing_keywords
import os

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

    # Find missing keywords
    missing_keywords = find_missing_keywords(resume_text, job_text)

    return jsonify({
        "missing_keywords": list(missing_keywords)
    })

if __name__ == "__main__":
    app.run(debug=True)

# RUN COMMAND: python app.py
# CURL COMMAND: curl -X POST -F "resume=@CPhillips_Resume20250217.pdf" -F "job_description=@Customer Service Representative.txt" http://127.0.0.1:5000/upload