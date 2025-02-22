import streamlit as st
import requests
import socket

# Detect if running locally
def is_running_locally():
    try:
        # Get the hostname and check if it's a local machine
        host_name = socket.gethostname()
        local_ip = socket.gethostbyname(host_name)
        return local_ip.startswith("127.") or local_ip.startswith("192.") or local_ip == "localhost"
    except:
        return False

# Set API URL based on environment
LOCAL_API_URL = "http://127.0.0.1:5000/upload"
DEPLOYED_API_URL = "https://ai-python-resume-keyword-scanner.onrender.com/upload"
API_URL = LOCAL_API_URL if is_running_locally() else DEPLOYED_API_URL

# Streamlit UI
st.title("📄 Resume Keyword Scanner")

uploaded_resume = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
uploaded_job_desc = st.file_uploader("Upload Job Description (TXT)", type=["txt"])

if st.button("Analyze"):
    if uploaded_resume and uploaded_job_desc:
        files = {
            "resume": uploaded_resume,
            "job_description": uploaded_job_desc
        }
        response = requests.post(API_URL, files=files)

        if response.status_code == 200:
            missing_keywords = response.json().get("missing_keywords", [])
            st.subheader("🔍 Missing Keywords:")
            st.write(", ".join(missing_keywords) if missing_keywords else "✅ No missing keywords found!")
        else:
            st.error("Error analyzing the resume. Try again.")
    else:
        st.error("Please upload both files before clicking analyze.")

# Display the current API URL for debugging
st.sidebar.write(f"**API URL:** {API_URL}")
