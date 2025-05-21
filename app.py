import streamlit as st
import os
import tempfile
from ranker import rank_resumes  # Import your AI function

st.set_page_config(page_title="AI Resume Ranker", layout="wide")

st.title("🤖 AI Resume Ranker")
st.markdown("Upload multiple resumes and a job description. The app will rank resumes based on relevance using NLP.")

# --- Job Description Input ---
st.subheader("📄 Job Description")
job_desc = st.text_area("Paste the job description here", height=200)

# --- Upload Resumes ---
st.subheader("📤 Upload Resumes")
uploaded_files = st.file_uploader(
    "Upload resume PDF files", type=["pdf"], accept_multiple_files=True
)

# --- Rank Button ---
if st.button("🚀 Rank Resumes"):
    if not job_desc:
        st.warning("Please paste the job description.")
    elif not uploaded_files:
        st.warning("Please upload at least one resume.")
    else:
        with st.spinner("Analyzing resumes..."):
            # Save uploaded files temporarily
            temp_dir = tempfile.mkdtemp()
            resume_paths = []

            for uploaded_file in uploaded_files:
                file_path = os.path.join(temp_dir, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.read())
                resume_paths.append(file_path)

            # Call your AI ranker
            ranked = rank_resumes(job_desc, resume_paths)

            # --- Show Results ---
            st.success("✅ Done! Here are the ranked resumes:")
            st.write("---")
            for i, (filename, score) in enumerate(ranked, start=1):
                st.markdown(f"**{i}. {os.path.basename(filename)}** — Score: `{score:.2f}`")
