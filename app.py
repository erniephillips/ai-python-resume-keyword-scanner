import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from resume_parser import extract_text_from_pdf, extract_text_from_docx
from job_parser import extract_text_from_url, extract_text_from_txt
from text_cleaner import clean_text
from keyword_matcher import analyze_resume

app = Flask(__name__)
CORS(app)


@app.route('/upload', methods=['POST'])
def upload():
    try:
        resume_text = ""
        job_description_text = ""

        # Process resume file
        if 'resume' in request.files:
            resume_file = request.files['resume']
            filename = resume_file.filename.lower()
            if filename.endswith('.pdf'):
                # Use .stream; the extract_text_from_pdf function now wraps in BytesIO internally.
                resume_text = extract_text_from_pdf(resume_file.stream)
            elif filename.endswith('.docx'):
                resume_text = extract_text_from_docx(resume_file.stream)
            else:
                resume_text = resume_file.read().decode("utf-8", errors="ignore")

        # Process job description
        if 'job_description' in request.files:
            job_file = request.files['job_description']
            filename = job_file.filename.lower()
            if filename.endswith('.pdf'):
                job_description_text = extract_text_from_pdf(job_file.stream)
            elif filename.endswith('.docx'):
                job_description_text = extract_text_from_docx(job_file.stream)
            elif filename.endswith('.txt'):
                job_description_text = extract_text_from_txt(job_file.stream)
            else:
                job_description_text = job_file.read().decode("utf-8", errors="ignore")
        elif request.form.get("job_description_url"):
            url = request.form.get("job_description_url")
            job_description_text = extract_text_from_url(url)

        # Check that texts were extracted
        if not resume_text or not job_description_text:
            return jsonify({"error": "Missing resume or job description content"}), 400

        # Clean texts
        resume_text_clean = clean_text(resume_text)
        job_description_text_clean = clean_text(job_description_text)

        # Analyze resume using the lightweight deep learning approach
        match_percentage, status, missing_keywords = analyze_resume(resume_text_clean, job_description_text_clean)

        return jsonify({
            "match_percentage": match_percentage,
            "status": status,
            "missing_keywords": missing_keywords
        })
    except Exception as e:
        # Return the full exception message as a JSON error
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
