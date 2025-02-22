import streamlit as st
import requests
import socket


# Detect if running locally
def is_running_locally():
    try:
        host_name = socket.gethostname()
        local_ip = socket.gethostbyname(host_name)
        # Debug: Print detected IP
        st.sidebar.write(f"🖥️ Detected Local IP: {local_ip}")
        return local_ip.startswith("127.") or local_ip.startswith("192.") or "localhost" in host_name
    except:
        return False


# Set API URL based on environment
LOCAL_API_URL = "http://127.0.0.1:5000/upload"
DEPLOYED_API_URL = "https://ai-python-resume-keyword-scanner.onrender.com/upload"

API_URL = DEPLOYED_API_URL  # Default to deployed URL

if is_running_locally():
    API_URL = LOCAL_API_URL

# Debug: Print API selection
st.sidebar.write(f"🌍 API URL: {API_URL}")

# Streamlit UI
st.title("📄 Resume Keyword Scanner")

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

# Debug: Show the API URL for verification
st.sidebar.write(f"🚀 Using API: {API_URL}")
