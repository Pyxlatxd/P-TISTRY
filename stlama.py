import streamlit as st
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import json
import io
from groq import Groq
from features.api import GROQ_API_KEY  # your API key

# --------------------------
# Groq client
# --------------------------
client = Groq(api_key=GROQ_API_KEY)

# --------------------------
# Helpers
# --------------------------
def get_alignment_enum(alignment_str):
    mapping = {
        "CENTER": WD_ALIGN_PARAGRAPH.CENTER,
        "LEFT": WD_ALIGN_PARAGRAPH.LEFT,
        "RIGHT": WD_ALIGN_PARAGRAPH.RIGHT,
        "JUSTIFY": WD_ALIGN_PARAGRAPH.JUSTIFY,
    }
    return mapping.get(alignment_str.upper(), WD_ALIGN_PARAGRAPH.LEFT)

def apply_format(paragraph, fmt):
    """Apply formatting dict to a paragraph"""
    if not paragraph.runs:
        run = paragraph.add_run(paragraph.text)
    else:
        run = paragraph.runs[0]

    run.bold = fmt.get("bold", False)
    run.italic = fmt.get("italic", False)
    run.underline = fmt.get("underline", False)
    run.font.name = fmt.get("font", "Times New Roman")
    run.font.size = Pt(fmt.get("size", 12))
    paragraph.alignment = get_alignment_enum(fmt.get("alignment", "LEFT"))

    #indent or without
    paragraph.paragraph_format.first_line_indent = Pt(fmt.get("indent", 0) * 72)

def get_indent_in_pt(paragraph):
    """Return first-line indent in points if any"""
    if paragraph.paragraph_format.first_line_indent:
        return paragraph.paragraph_format.first_line_indent.pt / 72
    return 0

# --------------------------
# Streamlit UI
# --------------------------
st.title("📄 APA Formatter with LLaMA 3 (with reasoning)")

uploaded_file = st.file_uploader("Upload a DOCX file", type="docx")

if uploaded_file:
    doc = Document(uploaded_file)

    # Extract paragraphs + formatting
    doc_paragraphs = []
    for para in doc.paragraphs:
        if not para.text.strip():
            continue
        run = para.runs[0] if para.runs else None
        para_fmt = {
            "text": para.text.strip(),
            "bold": run.bold if run else False,
            "italic": run.italic if run else False,
            "underline": run.underline if run else False,
            "font": run.font.name if run else "Times New Roman",
            "size": run.font.size.pt if run and run.font.size else 12,
            "alignment": para.alignment.name if para.alignment else "LEFT",
            "indent": get_indent_in_pt(para),
        }
        doc_paragraphs.append(para_fmt)

    # Prepare prompt
    llama_prompt = {
        "instruction": (
            "You are an APA formatting assistant. For each paragraph, analyze its text "
            "and formatting. Return **strict JSON only**, with a list of objects, each containing: "
            "`text` (original paragraph), `level` (1-5 for headings or null if body text), "
            "`reason` (why you assigned that level). "
            "Do NOT include any text outside of JSON."
        ),
        "apa_heading_rules": {
            1: "Centered, Bold, Title Case",
            2: "Left-aligned, Bold, Title Case, no indent",
            3: "Left-aligned, Bold, Italic, Title Case, no indent",
            4: "Left-aligned, Bold, Title Case, first-line, indent, ends with period",
            5: "Left-aligned, Bold, Italic, Title Case, first-line, indent, ends with period"
        },
        "paragraphs": doc_paragraphs
    }

    st.subheader("📤 Sent to LLaMA")
    st.json(llama_prompt)

    # Send to LLaMA
    if st.button("Format with LLaMA"):
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an APA formatting assistant."},
                {"role": "user", "content": json.dumps(llama_prompt)}
            ],
        )

        # Attempt to parse JSON safely
        try:
            llama_response = json.loads(completion.choices[0].message.content)
        except json.JSONDecodeError:
            st.error("❌ LLaMA did not return valid JSON.")
            st.text(completion.choices[0].message.content)
            st.stop()

        # Map heading levels to formatting
        heading_format = {
            1: {"bold": True, "italic": False, "alignment": "CENTER", "size": 12, "indent": 0},
            2: {"bold": True, "italic": False, "alignment": "LEFT", "size": 12, "indent": 0},
            3: {"bold": True, "italic": True, "alignment": "LEFT", "size": 12, "indent": 0},
            4: {"bold": True, "italic": False, "alignment": "LEFT", "size": 12, "indent": 0.5},
            5: {"bold": True, "italic": True, "alignment": "LEFT", "size": 12, "indent": 0.5},
        }

        # Apply formatting to document
        for para in doc.paragraphs:
            for item in llama_response:
                if para.text.strip() == item["text"]:
                    level = item.get("level")
                    if level is not None:
                        try:
                            lvl = int(level)
                            fmt = heading_format[lvl]

                            apply_format(para, fmt)
                        except (ValueError, KeyError):
                            continue

        # Append LLaMA reasoning at the end of the document
        doc.add_page_break()
        doc.add_paragraph("LLaMA Reasoning for Heading Levels", style="Heading 1")
        for item in llama_response:
            para = doc.add_paragraph()
            para.add_run(f"Text: {item['text']}\n")
            para.add_run(f"Level: {item['level']}\n")
            para.add_run(f"Reason: {item['reason']}\n")

        # Save updated doc to buffer
        output = io.BytesIO()
        doc.save(output)
        output.seek(0)

        st.success("✅ Document formatted with APA headings and reasoning!")
        st.download_button(
            "⬇️ Download formatted DOCX",
            data=output,
            file_name="formatted_output.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
