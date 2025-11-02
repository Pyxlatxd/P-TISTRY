import os
from docx import Document

# Path to the input .docx file
DOCX_PATH = r"/home/codespace/P-TISTRY/zey.docx"
EXTRACTED_TEXT_PATH = "extracted_text.txt"

def extract_text_from_docx(doc_path):
    """Extracts text from a .docx file and saves it to a text file."""
    try:
        doc = Document(doc_path)
        paragraphs = [p.text for p in doc.paragraphs]
        with open(EXTRACTED_TEXT_PATH, "w", encoding="utf-8") as f:
            f.write("\n".join(paragraphs))
        print("Text extraction complete. Run italics.py next.")
    except Exception as e:
        print(f"Error reading .docx: {e}")

if __name__ == "__main__":
    print("Extracting text from document...")
    extract_text_from_docx(DOCX_PATH)