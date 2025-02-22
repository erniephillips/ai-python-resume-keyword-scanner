import streamlit as st
import requests

st.title("Resume Keyword Scanner")

uploaded_resume = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
upload_job_desc = st.file_uploader("Upload Job Description (TXT)", type=["txt"])

if st.button("Analyze"):
    if uploaded_resume and upload_job_desc:
        files = {
            "resume": uploaded_resume,
            "job_description": upload_job_desc,
        }
        response = requests.post("http://127.0.0.1:5000/upload", files=files)

        if response.status_code == 200:
            missing_keywords = response.json()["missing_keywords"]
            st.subheader("🔍 Missing Keywords:")
            st.write(", ".join(missing_keywords) if missing_keywords else "✅ No missing keywords found!")
        else:
            st.error("Error analyzing the resume. Try again.")

    else:
        st.error("Please upload both files before clicking analyze.")

