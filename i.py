import streamlit as st
from docx import Document
import io
import os

# --- Feature modules ---
from features.api import GROQ_API_KEY
from features.font import rebuild_doc_with_apa
from features.margin import set_docx_margins
from features.page_no import add_page_number
from features.title import TITLE_PAGE_PROMPT  # used inside rebuild_doc_with_apa
from groq import Groq

client = Groq(api_key=GROQ_API_KEY)

# --- Streamlit UI ---
st.set_page_config(page_title="APA Formatter", page_icon="📄")
st.title("📘 APA Formatter")

APA_FONTS = {
    "Times New Roman": 12,
    "Georgia": 11,
    "Computer Modern": 10,
    "Calibri": 11,
    "Arial": 11,
    "Lucida Sans Unicode": 10,
}

font_choice = st.selectbox("Choose APA-approved font", list(APA_FONTS.keys()))
uploaded_file = st.file_uploader("Upload a .docx file", type="docx")

if uploaded_file:
    try:
        old_doc = Document(uploaded_file)

        # Step 1: Rebuild full APA document (title + content)
        doc = rebuild_doc_with_apa(old_doc, font_name=font_choice, font_size=APA_FONTS[font_choice])

        # Step 2: Apply margins
        doc = set_docx_margins(doc)

        # Step 3: Add page numbers
        doc = add_page_number(doc)

        # Step 4: Download
        output = io.BytesIO()
        doc.save(output)
        output.seek(0)

        st.success(f"✅ APA formatting applied with {font_choice} ({APA_FONTS[font_choice]}pt)")
        st.download_button(
            label="⬇️ Download formatted file",
            data=output,
            file_name="formatted_apa.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    except Exception as e:
        st.error(f"❌ Error: {e}")
