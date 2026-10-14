import os
import tempfile
import streamlit as st
from auditor_engine import MultimodalCodeAuditor

st.set_page_config(page_title="Multimodal Code Auditor", page_icon="🎥", layout="wide")

st.title("Multimodal Video Code Auditor and Explainer")
st.caption("Upload screen recordings or video walkthrough of bugs & code demos for automated AI Auditing & PR Generation.")

auditor= MultimodalCodeAuditor()

uploaded_files= st.file_uploader("Upload Videl Walkthrough (.mp4, .webm, .mov)", type=["mp4", "webm", "mov"])

if uploaded_files is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
        tmp_file.write(uploaded_files.read())
        video_path= tmp_file.name

    col1, col2= st.columns([1,1])

    with col1:
        st.subheader("Video Player")
        st.video(uploaded_files)

    with col2:
        st.subheader("Automated Multimodal Audit")
        if st.button("Run Multimodal Audit", type="primary"):
            with st.spinner("Processing video frames and audio stream via Gemini 2.0"):
                try:
                    audit_result= auditor.analyse_video_walkthrough(video_path)
                    st.markdown(audit_result)
                except Exception as e:
                    st.error(f"Error during audit: {e}")

            if os.path.exists(video_path):
                os.remove(video_path)