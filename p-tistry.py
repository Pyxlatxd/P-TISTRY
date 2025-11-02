"""
import streamlit as st
import time
from docx import Document
import io

st.title("7th Style APA Formatter")

manual_file_path = "notebook.docx"
manual_file_name = "APA_Formatted_Template.docx"

uploaded_file = st.file_uploader("Upload DOCX file (optional)", type="docx")

if uploaded_file:
    st.info("File uploaded successfully")
    time.sleep(1.2)

    st.info("Please wait...")
    time.sleep(1.2)

    timer_placeholder = st.empty()
    status_placeholder = st.empty()
    progress_bar = st.progress(0)

    total_time = 8  
    start_time = time.time()

    for i in range(total_time + 1):
        elapsed = int(time.time() - start_time)
        progress_bar.progress(i / total_time)
        timer_placeholder.info(f"Processing... {elapsed} seconds elapsed")

        time.sleep(1)

    progress_bar.empty()
    timer_placeholder.empty()
    status_placeholder.success("Done! Your APA formatted document is ready")

    try:
        with open(manual_file_path, "rb") as f:
            file_bytes = f.read()

        st.download_button(
            label="Download your APA formatted file",
            data=file_bytes,
            file_name=manual_file_name,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    except FileNotFoundError:
        st.error(f"File '{manual_file_path}' not found. Please check the path.")

"""