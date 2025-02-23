import streamlit as st
import requests

# Detect if running on localhost by checking Streamlit's page URL
if st.query_params.get("is_local") == "true":
    API_URL = "http://127.0.0.1:5000/upload"  # Local Flask API
else:
    API_URL = "https://ai-python-resume-keyword-scanner.onrender.com/upload"  # Deployed API

# Debug: Show API URL
st.sidebar.write(f"🌍 API URL: {API_URL}")

# Streamlit UI
st.title("📄 AI-Based Resume Keyword Scanner")

uploaded_resume = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
uploaded_job_desc = st.file_uploader("Upload Job Description (TXT)", type=["txt"])

if st.button("Analyze"):
    if uploaded_resume and uploaded_job_desc:
        files = {
            "resume": uploaded_resume,
            "job_description": uploaded_job_desc,
        }
        try:
            response = requests.post(API_URL, files=files, timeout=10)

            if response.status_code == 200:
                missing_keywords = response.json().get("missing_keywords", [])
                st.subheader("🔍 Missing Keywords:")
                st.write(", ".join(missing_keywords) if missing_keywords else "✅ No missing keywords found!")
            else:
                st.error(f"❌ Error analyzing the resume. Status: {response.status_code}")

        except requests.exceptions.ConnectionError:
            st.error("❌ Connection Error: Unable to reach API. Check if Flask API is running.")
        except requests.exceptions.Timeout:
            st.error("❌ Request timed out. API may be slow or down.")

st.markdown("---")  # horizontal line for separation

col1, col2 = st.columns([2, 1])  # Adjusts spacing (2 parts empty, 1 part text)
with col2:
    st.markdown("Developed by **Ernie Phillips III**", unsafe_allow_html=True)

st.sidebar.write(f"🚀 Final API in use: {API_URL}")
