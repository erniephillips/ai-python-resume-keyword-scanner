import streamlit as st
import requests

# Use your deployed API URL (or toggle for local testing)
API_URL = "https://ai-python-resume-keyword-scanner.onrender.com/upload"
#API_URL = "http://127.0.0.1:10000/upload"

st.sidebar.write(f"🌍 API URL: {API_URL}")
st.title("📄 AI-Based Resume Keyword Scanner")

st.info(
    "Disclaimer: The URL functionality is experimental. The web scraper now uses boilerpy3 to extract the main content from job posting URLs. "
    "This filters out menus, headers, and other extraneous text. However, some websites (e.g., Indeed) may block automated scraping, in which case "
    "please provide the job description as a file instead."
)

uploaded_resume = st.file_uploader("Upload your Resume (PDF or DOCX)", type=["pdf", "docx"])

job_desc_option = st.radio("Provide Job Description via:", ("Upload File", "Enter URL"))
if job_desc_option == "Upload File":
    uploaded_job_desc = st.file_uploader("Upload Job Description (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])
    job_desc_url = ""
else:
    uploaded_job_desc = None
    job_desc_url = st.text_input("Enter URL of Job Posting:")

if st.button("Analyze"):
    if uploaded_resume and (uploaded_job_desc or job_desc_url):
        uploaded_resume.seek(0)
        files = {"resume": (uploaded_resume.name, uploaded_resume, uploaded_resume.type)}
        data = {}
        if uploaded_job_desc:
            uploaded_job_desc.seek(0)
            files["job_description"] = (uploaded_job_desc.name, uploaded_job_desc, uploaded_job_desc.type)
        elif job_desc_url:
            data["job_description_url"] = job_desc_url.strip()

        try:
            response = requests.post(API_URL, files=files, data=data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                match_percentage = result.get("match_percentage", "N/A")
                status = result.get("status", "N/A")
                missing_keywords = result.get("missing_keywords", [])

                st.subheader("📊 Resume Analysis Results")
                st.write(f"**Match Percentage:** {match_percentage}%")
                st.write(f"**Status:** {status}")
                st.subheader("🔍 Missing Keywords:")
                if missing_keywords:
                    for keyword in missing_keywords:
                        st.markdown(f"- {keyword}")
                else:
                    st.success("✅ No missing keywords found!")
            else:
                try:
                    error_result = response.json()
                    error_message = error_result.get("error", f"Status: {response.status_code}")
                    st.error(f"❌ Error analyzing the resume. {error_message}")
                except Exception:
                    st.error(f"❌ Error analyzing the resume. Status: {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error("❌ Connection Error: Unable to reach API. Check if Flask API is running.")
        except requests.exceptions.Timeout:
            st.error("❌ Request timed out. API may be slow or down.")
    else:
        st.error("Please upload your resume and provide a job description (file or URL).")

st.markdown("---")
col1, col2 = st.columns([2, 1])
with col2:
    st.markdown("Developed by **Ernie Phillips III**")
st.sidebar.write(f"🚀 Final API in use: {API_URL}")
