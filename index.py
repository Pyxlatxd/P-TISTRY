# index.py
import streamlit as st
from docx import Document
from features.doc import build_apa_document
import io

st.title("📄 APA Formatter")

# Dropdown with APA-approved font options
font_options = {
    "Times New Roman (12 pt)": ("Times New Roman", 12),
    "Georgia (11 pt)": ("Georgia", 11),
    "Computer Modern (10 pt)": ("CMU Serif", 10),  # Fallback name for Computer Modern
    "Calibri (11 pt)": ("Calibri", 11),
    "Arial (11 pt)": ("Arial", 11),
    "Lucida Sans Unicode (10 pt)": ("Lucida Sans Unicode", 10),
}

font_choice = st.selectbox("Select APA-approved font", list(font_options.keys()))
font_name, font_size = font_options[font_choice]

# --- Format Selection ---
format_type = st.radio(
    "Select Format",
    ("Student", "Professional"),
    horizontal=True,
)

uploaded_file = st.file_uploader("Upload DOCX file", type="docx")

if uploaded_file:
    doc = Document(uploaded_file)

    # Pass font choice into builder
    doc = build_apa_document(doc, font_name=font_name, font_size=font_size, format_type=format_type)

    # Save updated doc to buffer
    output = io.BytesIO()
    doc.save(output)
    output.seek(0)

    st.success(f"✅ Document formatted with APA compliance using {font_name} ({font_size}pt)")
    st.download_button(
        "⬇️ Download formatted DOCX",
        data=output,
        file_name="formatted.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )






